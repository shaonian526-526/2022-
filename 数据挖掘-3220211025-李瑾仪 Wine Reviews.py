
filename = 'winemag-data-130k-v2.csv'

import pandas as pd
data = pd.read_csv(filename)

data.head()    #显示前5行

data.info()    #样本数据的相关信息概览

data = data.drop(columns=['Unnamed: 0','description'])

data.info()

title = ['country','designation', 'province', 'region_1', 'region_2','taster_name','taster_twitter_handle','title', 'variety', 'winery']

i = 0
print(title[i])
print(getattr(data, title[i]).value_counts())
data[title[i]].value_counts().head(10).plot.barh()

data.describe()


print('缺失值：')
print('points:',data['points'].isnull().sum())
print('price:',data['price'].isnull().sum())

import seaborn as sns
import matplotlib.pyplot as plt

def histogram(data, x, y ,title):
    plt.figure(figsize = (15,6))
    plt.title(title)
    sns.set_color_codes("pastel")
    sns.barplot(x=x, y=y, data=df)
    locs, labels = plt.xticks()
    plt.show()

temp = data['points'].value_counts()
df = pd.DataFrame({'points':temp.index, 'number_of_wines':temp.values})

histogram(df, 'points', 'number_of_wines', 'Points histogram')


temp = data['price'].value_counts()
df = pd.DataFrame({'price':temp.index, 'number_of_wines':temp.values})

histogram(df, 'price', 'number_of_wines', 'Price histogram')

#price(<200)
temp = sns.distplot(data[data["price"]<200]['price'])

#points
fig = plt.figure(figsize=(8, 15))
plt.boxplot(data['points'], notch=False, sym='o', vert=True)
t = plt.title('Box_points')
plt.show()

fig = plt.figure(figsize=(8, 15))
plt.boxplot(data['price'].loc[data['price']<200], notch=False, sym='o', vert=True)
t = plt.title('Box_price')
plt.show()

#将缺失部分剔除函数
def modify_delete(data):
    data_delete = data.dropna()
    return data_delete

#以points为例
data_delete = modify_delete(data['points'])

temp = data_delete.value_counts()
df = pd.DataFrame({'points':temp.index, 'number_of_wines':temp.values})

histogram(df, 'points', 'number_of_wines', 'Points histogram')

fig = plt.figure(figsize=(8, 15))
plt.boxplot(data_delete, notch=False, sym='o', vert=True)
t = plt.title('Box_points')
plt.show()

#以最高频率值填补缺失值函数
def modify_most(data):
    temp = data.mode()[0]    #求众数
    data_most = data.fillna(temp)
    return data_most

#以points为例
data_most = modify_most(data['points'])


temp = data_most.value_counts()
df = pd.DataFrame({'points':temp.index, 'number_of_wines':temp.values})

histogram(df, 'points', 'number_of_wines', 'Points histogram')

fig = plt.figure(figsize=(8, 15))
plt.boxplot(data_most, notch=False, sym='o', vert=True)
t = plt.title('Box_points')
plt.show()

data_fill = pd.DataFrame(data, columns=['province', 'region_1'])


data_fill.head(10)


data_fill['region_1'].value_counts().head(10).plot.barh()

dict = {}
for row in data_fill.iterrows():
    dict[row[1]['province']] = row[1]['region_1']
    
for row in data_fill.iterrows():
    region = dict[row[1]['province']]
    row[1]['region_1'] = region


data_fill['region_1'].value_counts().head(10).plot.barh()

data_sim = data[['price','points']]

point2price = {}
for row in data_sim.iterrows():
    if point2price.get(row[1]['points'], None):
        if not pd.isnull(row[1]['price']):
            point2price[row[1]['points']][0] += row[1]['price']
            point2price[row[1]['points']][1] += 1
    else:
        if not pd.isnull(row[1]['price']):
            point2price[row[1]['points']] = [row[1]['price'], 1]

for k in point2price.keys():
    point2price[k][0] = round(point2price[k][0] / point2price[k][1], 4)

for row in data_sim.iterrows():
    if pd.isnull(row[1]['price']):
        row[1]['price'] = point2price[row[1]['points']][0]

temp = data_sim['price'].value_counts()
df = pd.DataFrame({'price':temp.index, 'number_of_wines':temp.values})

histogram(df, 'price', 'number_of_wines', 'Price histogram')