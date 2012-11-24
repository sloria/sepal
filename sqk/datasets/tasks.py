from celery import task
import csv

from models import Feature, Instance, Label, Value

@task()
def read_datasource(dataset, source_file, label_col=None, feature_row=0):
    '''Parse a datasource (csv) and saves data to the database.
    '''
    with open(source_file, 'r') as s:
        data = csv.reader(s)
        instance_idx = 1
        features = []
        for i, row in enumerate(data):
            # Parse header
            if i == feature_row:
                for j, feature_name in enumerate(row):
                    # Create feature if it doesn't exist
                    features.append(feature_name.lower())
                    if j == label_col:
                        f, created = Feature.objects.get_or_create(
                            name=feature_name.lower(),
                            is_label_name=True)
                    else:
                        f, created = Feature.objects.get_or_create(
                            name=feature_name.lower())
                    f.datasets.add(dataset)
                    f.save()
                    dataset.features.add(f)
                dataset.save()
            # Parse data
            else:
                # Create instance and add it to dataset
                instance_name = '%s%s' % (dataset.name[:4].lower(),
                                            instance_idx)
                label, created = Label.objects.get_or_create(
                    label='unlabeled')
                if created:
                    label.save()
                inst = Instance.objects.create(
                    dataset=dataset, 
                    name=instance_name,
                    label=label)
                for feature in dataset.features.all():
                    inst.features.add(
                        Feature.objects.get(name=feature.name.lower()))
                inst.save()
                instance_idx +=1
                for v, value_str in enumerate(row):
                    label = None
                    # Process label
                    if v == label_col:
                        label, created = Label.objects.get_or_create(
                            label=value_str.lower())
                        label.instances.add(inst)
                        label.save()
                    # Process datum
                    else:
                        try:
                            val = float(value_str)
                            feature = Feature.objects.get(name=features[v]) # FIXME
                            v = Value.objects.create(value=val, 
                                feature=feature,
                                instance=inst)
                            v.save()
                        except ValueError:
                            # Ignore non-numerical data
                            continue
