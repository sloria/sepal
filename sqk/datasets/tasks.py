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
                    f = None
                    if j == dataset.label_col:
                        # Create or get label name
                        if Feature.objects.filter(
                            name=feature_name.lower(),
                            is_label_name=True).count() == 0:
                            f = Feature.objects.create(
                                name=feature_name.lower(),
                                is_label_name=True)
                        else:
                            f = Feature.objects.filter(is_label_name=True).get(
                                name=feature_name.lower())
                    else:
                        # Create or get regular feature
                        if Feature.objects.filter(
                            name=feature_name.lower(),
                            is_label_name=False).count() == 0:
                            f = Feature.objects.create(
                                name=feature_name.lower(),
                                is_label_name=False)
                        else:
                            f = Feature.objects.filter(is_label_name=False).get(
                                name=feature_name.lower())
                    dataset.features.add(f)
                dataset.save()
            # Parse data
            else:
                # Create instance and add it to dataset
                # TODO: Improve. format should be inst0001
                instance_name = '%s%s' % (dataset.name[:4].lower(),
                                            instance_idx)
                unlabel, created = Label.objects.get_or_create(
                    label='unlabeled',
                    )
                inst = Instance.objects.create(
                    dataset=dataset, 
                    name=instance_name,
                    label=unlabel)
                for feature in dataset.features.all():
                    inst.features.add(feature)
                inst.save()
                instance_idx +=1
                for v, value_str in enumerate(row):
                    # Process label
                    if v == dataset.label_col:
                        l, created = Label.objects.get_or_create(
                            label=value_str.lower())
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
                        feature = None
                        feature = dataset.features.get(name=features[v])
                        v = Value.objects.create(value=val, 
                                feature=feature,
                                instance=inst)
