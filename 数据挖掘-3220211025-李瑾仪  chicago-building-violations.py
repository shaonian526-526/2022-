
filename = 'building-violations.csv'

import pandas as pd

data = pd.read_csv(filename)

data.head()    #显示前5行




data.info()    #样本数据的相关信息概览



data = data.drop(columns=['ID', 'VIOLATION DESCRIPTION', 'VIOLATION INSPECTOR COMMENTS'])

data.info()

title = ['VIOLATION LAST MODIFIED DATE', 'VIOLATION DATE', 'VIOLATION CODE', 'VIOLATION STATUS', 'VIOLATION STATUS DATE', 'VIOLATION LOCATION', 'VIOLATION ORDINANCE', 'INSPECTOR ID', 'INSPECTION NUMBER', 'INSPECTION STATUS', 'INSPECTION WAIVED', 'INSPECTION CATEGORY', 'DEPARTMENT BUREAU', 'ADDRESS', 'STREET NUMBER', 'STREET DIRECTION', 'STREET NAME', 'STREET TYPE', 'PROPERTY GROUP', 'SSA', 'LOCATION', 'Community Areas','Zip Codes','Boundaries - ZIP Codes','Census Tracts']


i = 3
print(title[i])
print(getattr(data, title[i]).value_counts())
data[title[i]].value_counts().head(10).plot.barh()

data.describe()

print('缺失值：')
print('LONGITUDE:',data['LONGITUDE'].isnull().sum())

import seaborn as sns
import matplotlib.pyplot as plt

def histogram(data, x, y ,title):
    plt.figure(figsize = (15,6))
    plt.title(title)
    sns.set_color_codes("pastel")
    sns.barplot(x=x, y=y, data=df)
    locs, labels = plt.xticks()
    plt.show()

temp = data['SSA'].value_counts()
df = pd.DataFrame({'SSA':temp.index, 'number':temp.values})

histogram(df, 'SSA', 'number', 'SSA histogram')

fig = plt.figure(figsize=(8, 15))
plt.boxplot(data['SSA'].loc[data['SSA']<300], notch=False, sym='o', vert=True)
t = plt.title('Box_SSA')
plt.show()

def modify_delete(data):
    data_delete = data.dropna()
    return data_delete

data_delete = modify_delete(data['SSA'])

temp = data_delete.value_counts()
df = pd.DataFrame({'SSA':temp.index, 'number':temp.values})

histogram(df, 'SSA', 'number', 'SSA histogram')

def modify_most(data):
    temp = data.mode()[0]    #求众数
    data_most = data.fillna(temp)
    return data_most

data_most = modify_most(data['SSA'])

temp = data_most.value_counts()
df = pd.DataFrame({'SSA':temp.index, 'number':temp.values})

histogram(df, 'SSA', 'number', 'SSA histogram')

data_fill = pd.DataFrame(data, columns=['LATITUDE', 'LONGITUDE'])

data_fill.head(10)

data_fill['LONGITUDE'].value_counts().head(10).plot.barh()

dict = {}
for row in data_fill.iterrows():
    dict[row[1]['LATITUDE']] = row[1]['LONGITUDE']
    
for row in data_fill.iterrows():
    try:
        region = dict[row[1]['LATITUDE']]
    except:
        continue
    row[1]['LONGITUDE'] = region

data_fill['LONGITUDE'].value_counts().head(10).plot.barh()

data_sim = data[['LATITUDE','LONGITUDE']]

point2price = {}
for row in data_sim.iterrows():
    if point2price.get(row[1]['LONGITUDE'], None):
        if not pd.isnull(row[1]['LATITUDE']):
            point2price[row[1]['LONGITUDE']][0] += row[1]['LATITUDE']
            point2price[row[1]['LONGITUDE']][1] += 1
    else:
        if not pd.isnull(row[1]['LATITUDE']):
            point2price[row[1]['LONGITUDE']] = [row[1]['LATITUDE'], 1]

for k in point2price.keys():
    point2price[k][0] = round(point2price[k][0] / point2price[k][1], 4)

for row in data_sim.iterrows():
    if pd.isnull(row[1]['LATITUDE']):
        try:
            row[1]['LATITUDE'] = point2price[row[1]['LONGITUDE']][0]
        except:
            continue

temp = data_sim['LATITUDE'].value_counts()
df = pd.DataFrame({'LATITUDE':temp.index, 'number_of_wines':temp.values})

histogram(df, 'LATITUDE', 'number', 'LATITUDE histogram')