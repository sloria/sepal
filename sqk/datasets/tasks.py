import csv
import os
from django.conf import settings
from django.shortcuts import get_object_or_404

import yaafelib as yf
import wave
import contextlib
from celery import task

from models import *

@task()
def update_label_values(dataset, label_name_id, new_label_name_id):
    '''Updates the label name column of each instance in dataset.
    Used when updating a label name.
    '''
    # TODO:
    # Create new label_values with same values but new label name
    # Then Update each instance with the newly created label_values
    label_values = LabelValue.objects.filter(label_name__id=label_name_id)
    new_label_name_obj = get_object_or_404(LabelName, pk=new_label_name_id)
    for label_value in label_values:
        new_label_value = LabelValue.objects.create(value=label_value.value,
                                    label_name=new_label_name_obj)
        # filtered_instances = instances in dataset with this label_value
        # for inst in filtered_instances:
        #   replace instance's label_value with new_label_value
        

@task()
def handle_uploaded_file(f):
    '''Saves an uploaded data source to MEDIA_ROOT/data_sources 
    '''
    with open(os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name ), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@task()
def read_datasource(dataset, source_path, feature_row=0):
    '''Parse a datasource (csv) and saves data to the database.

    IMPORTANT: As of now, this method is for demo purposes. It assumes
    that the the independent variable is in the last row.
    '''
    with open(source_path, 'r') as s:
        # TODO: file type handling
        data = csv.reader(s)
        features = [] # List of feature names
        feature_obj_list = [] # List of feature objects
        label_name = None
        for i, row in enumerate(data):
            # Parse header
            if i == feature_row:
                for j in range(len(row)-1):
                    features.append(row[j].lower())
                    f = None
                    # Create feature if it doesn't exist
                    if Feature.objects.filter(name=row[j].lower()).count() == 0:
                        f = Feature.objects.create(name=row[j].lower())
                    else:
                        f = Feature.objects.filter().get(
                            name=row[j].lower())
                    feature_obj_list.append(f)

                label_name= LabelName.objects.create(
                    name=row[-1])
            # Parse data
            else:
                # Create instance and add it to dataset
                inst = Instance.objects.create(
                    dataset=dataset,
                    species=dataset.species)
                for feature in feature_obj_list:
                    inst.features.add(feature)
                inst.save()
                for v, value_str in enumerate(row):
                    # Process datum
                    try:
                        val = float(value_str)
                    except ValueError:
                        # Ignore non-numerical data
                        # TODO: Eventually accept non-numeric data
                        continue
                    feature = None
                    feature = inst.features.get(name=features[v])
                    v = FeatureValue.objects.create(value=val, 
                            feature=feature,
                            instance=inst)

                print row[-1]
                # Create label value and add it to the label
                label_value_obj, created = LabelValue.objects.get_or_create(
                                            value=row[-1].lower(),
                                            label_name=label_name)
                inst.label_values.add(label_value_obj)
                inst.save()


@task()
def extract_features(dataset, audiofile_path):
    n_frames, sample_rate, duration = 0, 0, 0
    with contextlib.closing(wave.open(audiofile_path, 'r')) as audiofile:
        n_frames = audiofile.getnframes()
        sample_rate = audiofile.getframerate()
        duration = n_frames / float(sample_rate)

    # Format - {'Display name': 'name: Definition'}
    features = {'Spectral Shape Characteristics': 'sss: SpectralShapeStatistics',
                'ZCR': 'zcr: ZCR',
                'Duration': None,
                'Sample rate': None}

    # Add features to extract
    feature_plan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)
    for feature_definition in features.values():
        if feature_definition: # Exclude duration and sample rate
            feature_plan.addFeature(feature_definition)
    
    # Configure an Engine
    engine = yf.Engine()
    engine.load(feature_plan.getDataFlow())
    
    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile_path)
    # format - {'Spectral centroid': [[2.33], [4.34],...[2.55]]}
    outputs = {}
    
    # Read and store output arrays to outputs dict
    for display_name, definition in features.iteritems():
        if definition:
            # ex: 'loudness'
            output_name = definition.split(':')[0].strip()
            if output_name == 'sss': # Store separate spec shape stats
                spec_shape_stats = engine.readOutput(output_name)
                outputs['Spectral centroid'] = spec_shape_stats[:, 0]
                outputs['Spectral spread'] = spec_shape_stats[:, 1]
                outputs['Spectral skewness'] = spec_shape_stats[:, 2]
                outputs['Spectral kurtosis'] = spec_shape_stats[:, 3]
            else: # 1 dimensional data (1 X T array)
                a = engine.readOutput(output_name) # 2D array
                outputs[display_name] = a.transpose()[0]

    # Create features 
    feature_obj_list = []
    for display_name in outputs.keys():
        f, created = Feature.objects.get_or_create(name=display_name.lower())
        feature_obj_list.append(f)

    rate_obj, created = Feature.objects.get_or_create(name='sample rate')
    feature_obj_list.append(rate_obj)
    duration_obj, created = Feature.objects.get_or_create(name='duration')
    feature_obj_list.append(duration_obj)

    # Create instance
    inst = Instance.objects.create(
        dataset=dataset,
        species=dataset.species)
    for feature in feature_obj_list:
        inst.features.add(feature)
    
    # Add a placeholder label name and label value to instance
    # This is necessary in order for plotting to work
    no_label_name, c = LabelName.objects.get_or_create(name='none')
    no_label, c = LabelValue.objects.get_or_create(value="none",
                                                    label_name=no_label_name)
    inst.label_values.add(no_label)
    inst.save()

    for display_name, output in outputs.iteritems():
        if output.size > 0: # Avoid empty data
            # Save output data
            for i in range(output[0].size):
                output_mean = output[i].mean()
                print display_name
                v = FeatureValue.objects.create(value=output_mean,
                    feature=Feature.objects.get(name__iexact=display_name.lower()),
                    instance=inst)


    # Save sample_rate and duration data
    FeatureValue.objects.create(value=sample_rate,
        feature=Feature.objects.get(name='sample rate'),
        instance=inst)

    FeatureValue.objects.create(value=duration,
        feature=Feature.objects.get(name='duration'),
        instance=inst)



