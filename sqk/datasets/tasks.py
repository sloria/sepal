from celery import task
import csv

# TODO
@task()
def read_datasource(source, label_col=None, feature_row=0):
    '''Parse a datasource (csv) and saves data to the database.
    '''
    with open(source, 'r') as s:
        data = csv.reader(s)
        features = []
        instance_idx = 0 
        for i, row in enumerate(data):
            if i == feature_row:
                for feature_name in row:
                    features.append(feature_name)
                    print 'Save Feature:'
                    print '\tinstance:'
                    print '\tname: %s' % feature_name
            else:
                print 'Save Instance:'
                print '\tindex: %d' % instance_idx
                instance_idx +=1
                for v, value_str in enumerate(row):
                    label = None
                    if v == label_col:
                        label = value_str
                    else:
                        try:
                            value = float(value_str)
                        except ValueError:
                            # Ignore non-numerical data
                            continue
                    print 'Save Value:'
                    print '\tfeature: %s' % features[v]
                    print '\tinstance:'
                    if label_col != None:
                        print '\tlabel: %s' % label
                    print '\tvalue: %f' % value
