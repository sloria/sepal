import os
from django.conf import settings

import yaafelib as yf
import wave
import contextlib
from celery import task

from sqk.datasets.models import *
from sqk.datasets.utils import filter_by_key, find_dict_by_item


@task()
def handle_uploaded_file(f):
    '''Saves an uploaded data source to MEDIA_ROOT/data_sources
    '''
    with open(os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return destination
        

@task()
def extract_features(dataset_id, instance_id, audiofile_path):
    dataset = Dataset.objects.get(pk=dataset_id)
    inst = Instance.objects.get(pk=instance_id)
    
    n_frames, sample_rate, duration = 0, 0, 0
    # Calculate the sample rate and duration
    with contextlib.closing(wave.open(audiofile_path, 'r')) as audiofile:
        n_frames = audiofile.getnframes()
        sample_rate = audiofile.getframerate()
        duration = n_frames / float(sample_rate)

    # Format - {'Display name': 'name: Definition'}

    FEATURES = [
                    {'display_name': 'Spectral Shape Characteristics',
                    'yaafe_name':  'sss',
                    'yaafe_definition': 'SpectralShapeStatistics',
                    'subfeatures': ['Spectral centroid', 'Spectral spread', 'Spectral kurtosis', 'Spectral skewness'] 
                    },

                    {'display_name': 'Temporal Shape Characteristics',
                    'yaafe_name':  'tss',
                    'yaafe_definition': 'TemporalShapeStatistics',
                    'subfeatures': ['Temporal centroid', 'Temporal spread', 'Temporal kurtosis', 'Temporal skewness'] 
                    },

                    {'display_name': 'ZCR',
                    'yaafe_name':  'zcr',
                    'yaafe_definition': 'ZCR',
                    'unit': 'Hz'
                    },

                    {'display_name': 'Energy',
                    'yaafe_name':  'energy',
                    'yaafe_definition': 'Energy',
                    },

                    {'display_name': 'Loudness',
                    'yaafe_name':  'loudness',
                    'yaafe_definition': 'Loudness',
                    },

                    {'display_name': 'Spectral rolloff',
                    'yaafe_name':  'spectral_rolloff',
                    'yaafe_definition': 'SpectralRolloff',
                    },

                    {'display_name': 'Perceptual sharpness',
                    'yaafe_name':  'perceptual_sharpness',
                    'yaafe_definition': 'PerceptualSharpness',
                    },

                    {'display_name': 'Perceptual spread',
                    'yaafe_name': 'perceptual_spread',
                    'yaafe_definition': 'PerceptualSpread',
                    },

                    {'display_name': 'Duration',
                    'unit': 's',
                    },

                    {'display_name': 'Sample rate',
                    'unit': 'Hz',
                    },

                    {'display_name': 'Spectral decrease',
                    'yaafe_name': 'spectral_decrease',
                    'yaafe_definition': 'SpectralDecrease',
                    },

                    {'display_name': "Spectral flatness",
                    'yaafe_name': 'spectral_flatness',
                    'yaafe_definition': 'SpectralFlatness',
                    },

                    # {'display_name': "Spectral flux",
                    # 'yaafe_name': 'spectral_flux',
                    # 'yaafe_definition': 'SpectralFlux',
                    # },

                    {'display_name': "Spectral slope",
                    'yaafe_name': 'spectral_slope',
                    'yaafe_definition': 'SpectralSlope',
                    },

                    # {'display_name': "Spectral variation",
                    # 'yaafe_name': 'spectral_variation',
                    # 'yaafe_definition': 'SpectralVariation',
                    # }

                ]

    # Add features to extract
    feature_plan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)

    for feature in FEATURES:
        if 'yaafe_definition' in feature:
            # YAAFE feature plans take definitions of the form: 'zcr: ZCR'
            full_definition = feature['yaafe_name'] + ': ' + feature['yaafe_definition']
            # Add the feature to the feature plan to be extracted
            feature_plan.addFeature(full_definition)
    
    # Configure an Engine
    engine = yf.Engine()
    engine.load(feature_plan.getDataFlow())
    
    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile_path)
    # outputs dict format - {'Spectral centroid': [[2.33], [4.34],...[2.55]]}
    outputs = {}

    # Read and store output arrays to outputs dict
    for feature in FEATURES:
        if 'yaafe_definition' in feature:  # Exclude duration and sample rate
            output_name = feature['yaafe_name']
            # If the feature has subfeatures, e.g. Spec shape stats
            if 'subfeatures' in feature:
                full_output = engine.readOutput(output_name)
                for i, subfeature_display_name in enumerate(feature['subfeatures']):
                    outputs[subfeature_display_name] = full_output[:, i]
            # If the feature has only 1 dimension(1 X T array)
            else:
                display_name = feature['display_name']
                a = engine.readOutput(output_name)  # 2D array
                # Transpose data to make it a 1D array
                outputs[display_name] = a.transpose()[0]


    # Create YAAFE feature objects
    feature_obj_list = []
    for display_name in outputs.keys():
        feature = find_dict_by_item(('display_name', display_name), FEATURES)
        f, created = Feature.objects.get_or_create(
                        name=display_name.lower(), 
                        display_name=display_name
                    )
        if feature and ('unit' in feature):
            f.unit = feature['unit']
            f.save()
        feature_obj_list.append(f)

    # Create Sample rate and Duration objects
    rate_obj, created = Feature.objects.get_or_create(name='sample rate')
    if not rate_obj.unit:
        rate_obj.unit = 'Hz'
        rate_obj.save()
    feature_obj_list.append(rate_obj)
    duration_obj, created = Feature.objects.get_or_create(name='duration')
    if not duration_obj.unit:
        duration_obj.unit = 's'
        duration_obj.save()
    feature_obj_list.append(duration_obj)

    # Associate features with instance
    # for feature in feature_obj_list:
    #     inst.features.add(feature)

    # If dataset has labels
    if dataset.labels():
        # NOTE: This assumes there's only one label name per dataset.
        # Just indexes the first label name
        label_name = dataset.labels()[0]
    else:
        # attach a placeholder LabelName called 'variable'
        filtered = LabelName.objects.filter(name='variable')
        # make sure that 'get' doesn't return an error if there are more than 1 
        # LabelName called 'variable'
        if len(filtered) <= 1:
            label_name, c = LabelName.objects.get_or_create(name='variable')
        else:
            label_name = filtered[0]

    # Add a placeholder label value called "none" to instance
    # This is necessary in order for plotting to work
    filtered = LabelValue.objects.filter(value="none", label_name=label_name)
    if len(filtered) <= 1:
        no_label, c = LabelValue.objects.get_or_create(value="none",
                                                    label_name=label_name)
    else:
        no_label = filtered[0]
        
    inst.label_values.add(no_label)
    inst.save()

    # Save output data and associate it with inst
    for display_name, output in outputs.iteritems():
        if output.size > 0:  # Avoid empty data
            for i in range(output[0].size):
                output_mean = output[i].mean()
                FeatureValue.objects.create(value=output_mean,
                    feature=Feature.objects.get(name__iexact=display_name.lower()),
                    instance=inst)

    # Save sample_rate and duration data
    FeatureValue.objects.create(value=sample_rate,
        feature=Feature.objects.get(name='sample rate'),
        instance=inst)

    FeatureValue.objects.create(value=duration,
        feature=Feature.objects.get(name='duration'),
        instance=inst)
