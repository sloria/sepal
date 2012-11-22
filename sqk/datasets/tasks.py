from celery import task
import csv

from models import Feature, Instance, Label, Value

# TODO
@task()
def read_datasource(dataset, source_file, label_col=None, feature_row=0):
    '''Parse a datasource (csv) and saves data to the database.
    '''
    print 'opening'
    with open(source_file, 'r') as s:
        data = csv.reader(s)
        features = []
        instance_idx = 1
        for i, row in enumerate(data):
            # Parse header
            if i == feature_row:
                for feature_name in row:
                    features.append(feature_name)
                    # Create feature if it doesn't exist
                    f, created = Feature.objects.get_or_create(
                        name=feature_name)
                    if created:
                        f.save()
            # Parse data
            else:
                # Create instance and add it to dataset
                instance_name = 'inst%s' % instance_idx
                inst = Instance.objects.create(dataset=dataset, name=instance_name)
                inst.save()
                instance_idx +=1
                for v, value_str in enumerate(row):
                    label = None
                    # Process labellab
                    if v == label_col:
                        label, created = Label.objects.get_or_create(
                            label=value_str)
                        label.instances.add(inst)
                        label.save()
                    # Process datum
                    else:
                        try:
                            val = float(value_str)
                            feature = Feature.objects.get(name=features[v])
                            v = Value.objects.create(value=val, 
                                feature=feature,
                                instance=inst)
                            v.save()
                        except ValueError:
                            # Ignore non-numerical data
                            continue
