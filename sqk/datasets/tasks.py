from celery import task
import csv
import os
from django.conf import settings

from models import *

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
    '''
    with open(source_path, 'r') as s:
        # TODO: file type handling
        data = csv.reader(s)
        features = []
        for i, row in enumerate(data):
            # Parse header
            if i == feature_row:
                for j, feature_name in enumerate(row):
                    features.append(feature_name.lower())
                    f = None
                    # Create feature if it doesn't exist
                    if Feature.objects.filter(name=feature_name.lower()).count() == 0:
                        f = Feature.objects.create(name=feature_name.lower())
                    else:
                        f = Feature.objects.filter().get(
                            name=feature_name.lower())
                    dataset.features.add(f)
                dataset.save()
            # Parse data
            else:
                # Create instance and add it to dataset
                inst = Instance.objects.create(
                    dataset=dataset,
                    species=dataset.species)
                for feature in dataset.features.all():
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
                    feature = dataset.features.get(name=features[v])
                    v = Value.objects.create(value=val, 
                            feature=feature,
                            instance=inst)


@task()
def extract_features(dataset, audiofile_path):
    import yaafelib as yf
    import wave
    import contextlib
 
    n_frames, sample_rate, duration = 0, 0, 0
    with contextlib.closing(wave.open(audiofile_path, 'r')) as audiofile:
        n_frames = audiofile.getnframes()
        sample_rate = audiofile.getframerate()
        duration = n_frames / float(sample_rate)

    feature_names = ['energy_mean', 'zcr_mean', 'duration', 'sample_rate']
    # Add features to extract
    featplan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)
    featplan.addFeature('energy: Energy')
    featplan.addFeature('zcr: ZCR')
    
    # Configure an Engine
    engine = yf.Engine()
    engine.load(featplan.getDataFlow())
    
    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile_path)
    # 2D numpy arrays
    energy = engine.readOutput('energy')
    zcr = engine.readOutput('zcr')

    # Create features and add to dataset
    for feature in feature_names:
        f, created = Feature.objects.get_or_create(name=feature)
        if dataset.features.filter(name=feature).count() == 0:
            dataset.features.add(f)

    # Create instance
    inst = Instance.objects.create(
        dataset=dataset,
        species=dataset.species)
    for feature in dataset.features.all():
        inst.features.add(feature)
    inst.save()

    if energy.size > 0 and zcr.size > 0:
        # Save energy data
        for i in range(energy[0].size):
            energy_mean = energy[:, i].mean()
            v = Value.objects.create(value=energy_mean,
                feature=Feature.objects.get(name='energy_mean'),
                instance=inst)

        # Save energy data
        for i in range(zcr[0].size):
            zcr_mean = zcr[:, i].mean()
            v = Value.objects.create(value=zcr_mean,
                feature=Feature.objects.get(name='zcr_mean'),
                instance=inst)

    # Save sample_rate and duration data
    Value.objects.create(value=sample_rate,
        feature=Feature.objects.get(name='sample_rate'),
        instance=inst)

    Value.objects.create(value=duration,
        feature=Feature.objects.get(name='duration'),
        instance=inst)













