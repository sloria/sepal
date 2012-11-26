from celery import task
import csv
import os
from django.conf import settings

from models import Feature, Instance, Species, Value

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
