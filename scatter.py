from sqk.datasets.models import Dataset
import numpy as np

def scatterplot(dataset, features):
    '''
    Same thing, except with only 2D data.
    features - user-selected features
    
    all_feature = feature.objects.all()
    all_feature[0] get the first element in the features
    all_feature[0].name get value using table column name 
    
    a[:, 0]
    l = list()
    d.sorted_features().index(duration)
    
    import numpy as n
    e.g. [<Feature: f0>, <Feature: duration>]
    '''
    data = np.array(dataset.values_as_list) # all instance data as a 2D numpy array
    result = []
    axis_name = [f.name for f in features]
    x_axis = []
    y_axis = []
    
    x_feature_name = axis_name[0]
    index_x = list(dataset.sorted_features()).index(features[0])
    x_axis = data[:, index_x]
    # map(lambda i: i[index_x], dataset.sorted_features())
    
    y_feature_name = axis_name[1]
    index_y = list(dataset.sorted_features()).index(features[1])
    y_axis = data[:, index_y]
    # map(lambda i: i[index_y], dataset.sorted_features())
    
    for i in range(len(dataset.sorted_instances)):
        temp = {}
        temp.setdefault(x_feature_name, x_axis[i]);
        temp.setdefault(y_feature_name, y_axis[i]);
        result.append(temp)
        
    return result

d = Dataset.objects.all()[0]
feats = [d.sorted_features()[0], d.sorted_features()[1]]
print ' derp'
print scatterplot(d, feats)