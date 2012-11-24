from celery import task
import csv

from models import Feature, Instance, Label, Value

@task()
def read_datasource(dataset, source_path):
    '''Parse a datasource (csv) and saves data to the database.
    '''
    with open(source_path, 'r') as s:
        data = csv.reader(s)
        instance_idx = 1
        features = []
        for i, row in enumerate(data):
            # Parse header
            if i == dataset.feature_row:
                for j, feature_name in enumerate(row):
                    # Create feature if it doesn't exist
                    features.append(feature_name.lower())
                    if j == dataset.label_col:
                        label_name, created =  LabelName.objects.get_or_create(
                            name=feature_name.lower())
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
                # TODO: Improve. format should be inst0001
                instance_name = '%s%s' % (dataset.name[:4].lower(),
                                            instance_idx)
                unlabel, created = LabelValue.objects.get_or_create(
                    value='unlabeled',
                    label_name=LabelName.objects.get(pk=1))
                inst = Instance.objects.create(
                    dataset=dataset, 
                    name=instance_name,
                    value=unlabel)
                for feature in dataset.features.all():
                    inst.features.add(
                        Feature.objects.get(name=feature.name.lower()))
                inst.save()
                instance_idx +=1
                for v, value_str in enumerate(row):
                    label = None
                    # Process label
                    if v == dataset.label_col:
                        l, created = LabelValue.objects.get_or_create(
                            value=value_str.lower(), label_name=LabelName.objects.get(pk=1))
                        l.instances.add(inst)
                        inst.label = l
                        inst.save()
                        l.save()
                    # Process datum
                    else:
                        try:
                            val = float(value_str)
                        except ValueError:
                            # Ignore non-numerical data
                            # TODO: Eventually accept non-numeric data
                            continue
                        feature = Feature.objects.get(name=features[v])
                        v = Value.objects.create(value=val, 
                                feature=feature,
                                instance=inst)
