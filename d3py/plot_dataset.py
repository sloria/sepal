import pandas
import d3py
from sqk.datasets.models import Dataset
import numpy as np


d = Dataset.objects.all()[0]
feature_objects = d.sorted_features(
                        ).exclude(
                        name='duration').exclude(
                        name='sample_rate')

features = [str(f.name) for f in feature_objects]
data = np.array(d.values_as_list())
value_means = []

for i in range(len(data[0])):
    value_means.append(data[:,i].mean())

df = pandas.DataFrame({
    "value" : value_means,
    "feature" : features
})

p = d3py.Figure(df, width=500, height=300)
p += d3py.Bar(x = "feature", y = "value", fill = "MediumAquamarine")
p += d3py.xAxis(x = "feature", label='feature')
p += d3py.yAxis(y = "value", label='value')
p.show()