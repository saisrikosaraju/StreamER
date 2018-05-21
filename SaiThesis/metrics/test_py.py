import sys
import numpy
import pandas as pd

data = [['Alex',10],['Bob',12],['Clarke',13],['Alex',20]]
datas = []
df1 = pd.DataFrame(datas,columns=['Name','Age'])

data = [['Alex',20]]
df = pd.DataFrame(data,columns=['Name','Age'])

t =  []
df2 = pd.DataFrame(t,columns=['Name','Age'])

d=pd.Series('Alexa')
df2['Name'] = d.values
d=pd.Series('12')
df2['Age'] = d.values

print df2

df = df.append(df2);

print df

#print df['Age'].isin(df1[df1['Name'].isin(df['Name'])]['Age'])
#print df1[df1['Name'].isin(df['Name'])]['Age'].isin(df['Age'])
#print df1[df1['Name'].isin(df['Name'])]['Age'].index.tolist()

if (len(df1[df1['Name'].isin(df['Name'])]) >= 0):
    print 'Bello'


index = df1[df1['Name'].isin(df['Name'])]['Age'].index.tolist()

for i in index:
    if (df1.iloc[i]['Age'] == df.iloc[0]['Age']):
        df1.loc[i, 'Age'] += 1

print 'test', 10.1%2
