# -*- coding: utf-8 -*-
"""proj.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IDYkI8BNLTu26vm5Nz5szcX_UXiPwyMX
"""

from google.colab import drive
drive.mount('/content/grive')

"""Importing necessaries Library"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.gridspec as gridspec
import os
from sklearn.model_selection import train_test_split
import seaborn as sns

import matplotlib.pyplot as plt
from sklearn import svm
import tensorflow as tf

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

"""Reading Dataset"""

data_df=pd.read_csv('/content/grive/MyDrive/Heart_Lung_Dataset/lung_cancer.csv')
data_df.head(10)

data_df.describe()

#estimating male and female patients
female = len(data_df[data_df.sex==0])
male = len(data_df[data_df.sex==1])

perc_female = female/len(data_df.sex)*100
perc_male = male/len(data_df.sex)*100
print('Distribution of females is {:.2f}%, while for males, it is {:.2f}%'.format(perc_female, perc_male))

sns.scatterplot(data_df.age[data_df.target==1], y=data_df.thalach[(data_df.target==1)], color='red')
sns.scatterplot(data_df.age[data_df.target==0], y=data_df.thalach[(data_df.target==0)], color='green')
plt.legend(["Disease", "Not Disease"])

x = data_df.drop('target',axis=1)
y = data_df['target']
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=5)
print('Training data : {},{} '.format(x_train.shape, y_train.shape))
print('Testing data : {},{} '.format(x_test.shape, y_test.shape))

"""Normalisation of Dataset"""

scale = StandardScaler()
x_train = scale.fit_transform(x_train)
x_test = scale.transform(x_test)
score=[]

print(x_train)

"""Logistic Regression"""

clf1=LogisticRegression()
clf1.fit(x_train,y_train)
pred1=clf1.predict(x_test)
print(clf1.coef_)
s1=accuracy_score(y_test,pred1)
score.append(s1*100)
print(s1)

"""K-Nearest Neighbor"""

knn = KNeighborsClassifier()
knn.fit(x_train,y_train)

y_true0 = knn.predict(x_test)
s2 = accuracy_score(y_test,y_true0)
score.append(s2*100)
print(s2)

"""Random Forest"""

rf = RandomForestClassifier()
rf.fit(x_train,y_train)

y_true1 = rf.predict(x_test)
s4 = accuracy_score(y_test,y_true1)
score.append(s4*100)
print(s4)

"""Support Vector Machine"""

svc = svm.SVC()
svc.fit(x_train,y_train)

y_true2 = svc.predict(x_test)
s5 = accuracy_score(y_test,y_true2)
score.append(s5*100)
print(s5)

"""ANN"""

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(6, activation='relu'))
ann.add(tf.keras.layers.Dense(6, activation='relu'))
ann.add(tf.keras.layers.Dense(1, activation='sigmoid'))

ann.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history = ann.fit(x_train, y_train, batch_size = 10, epochs=100)
print(history)

preds = ann.evaluate(x_test,y_test, batch_size=10,verbose=2)
print('Accuracy score : {}'.format(preds[1]))

pred_ann = ann.predict(x_test) 
pred_ann1 = np.argmax(pred_ann, axis = 1)
label = np.argmax(y_test)

pred_ann1[:5]

y_test[:5]

"""Data Visualization

The data includes 303 patient level features including if they have heart disease at the end or not. Features are like;

Age: Obvious one...
Sex:
0: Female
1: Male

Chest Pain Type:

0: Typical Angina

1: Atypical Angina

2: Non-Anginal Pain

3: Asymptomatic

Resting Blood Pressure: Person's resting blood pressure.


Cholesterol: Serum Cholesterol in mg/dl

Fasting Blood Sugar:

0:Less Than 120mg/ml

1: Greater Than 120mg/ml

Resting Electrocardiographic Measurement:

0: Normal

1: ST-T Wave Abnormality

2: Left Ventricular Hypertrophy

Max Heart Rate Achieved: Maximum Heart Rate Achieved

Exercise Induced Angina:

1: Yes

0: No

ST Depression: ST depression induced by exercise relative to rest.

Slope: Slope of the peak exercise ST segment:


0: Upsloping

1: Flat

2: Downsloping

Thalassemia: A blood disorder called 'Thalassemia':

0: Normal

1: Fixed Defect

2: Reversable Defect

Number of Major Vessels: Number of major vessels colored by fluoroscopy.
"""



cust_palt = [
    '#111d5e', '#c70039', '#f37121', '#ffbd69', '#ffc93c'
]

plt.style.use('ggplot')

train =pd.read_csv('/content/grive/MyDrive/Heart_Lung_Dataset/heart.csv')
train.head(5)

train.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved',
       'exercise_induced_angina', 'st_depression', 'st_slope', 'num_major_vessels', 'thalassemia', 'condition']

train['sex'] = train['sex'].map({0:'female',1:'male'})

train['chest_pain_type'] = train['chest_pain_type'].map({3:'asymptomatic', 1:'atypical_angina', 2:'non_anginal_pain', 0:'typical_angina'})

train['fasting_blood_sugar'] = train['fasting_blood_sugar'].map({0:'less_than_120mg/ml',1:'greater_than_120mg/ml'})

train['rest_ecg'] = train['rest_ecg'].map({0:'normal',1:'ST-T_wave_abnormality',2:'left_ventricular_hypertrophy'})

train['exercise_induced_angina'] = train['exercise_induced_angina'].map({0:'no',1:'yes'})

train['st_slope'] = train['st_slope'].map({0:'upsloping',1:'flat',2:'downsloping'})

train['thalassemia'] = train['thalassemia'].map({1:'fixed_defect',0:'normal',2:'reversable_defect'})

train['condition'] = train['condition'].map({0:'no_disease', 1:'has_disease'})

"""Visualisations"""

# Masks for easier selection in future:

categorical = [i for i in train.loc[:,train.nunique()<=10]]
continuous = [i for i in train.loc[:,train.nunique()>=10]]

def ctg_dist(df, cols, hue=None,rows=3, columns=3):
    
    '''A function for displaying cateorical distribution'''
    
    fig, axes = plt.subplots(rows, columns, figsize=(16, 12))
    axes = axes.flatten()

    for i, j in zip(df[cols].columns, axes):
        sns.countplot(x=i,
                    data=df,
                    palette=cust_palt,
                    hue=hue,
                    ax=j,
                    order=df[i].value_counts().index)
        j.tick_params(labelrotation=10)
        
        total = float(len(df[i]))
        
        j.set_title(f'{str(i).capitalize()} Distribution')
        
        
        for p in j.patches:
            height = p.get_height()
            j.text(p.get_x() + p.get_width() / 2.,
                    height + 2,
                    '{:1.2f}%'.format((height / total) * 100),
                    ha='center')
        
        plt.tight_layout()

# Display categorical data:

ctg_dist(train, categorical)

"""Categorical Data
Here we can do these observations:

Males on the dataset is more than double of the female observations.

Most common ches pain type is 'Asymptomatic' ones which is almost 50% of the data

85% of the patients has no high levels of fastin blood sugar.

Resing electrocardiographic observations are evenly distributed between normal and left ventricular hypertrophy with ST-T minority

67% of the patients had no exercise induced angina
Peak exercise slope seems mainly divided between upsloping and flat.
"""



# Displaying numeric distribution:

fig = plt.figure(constrained_layout=True, figsize=(16, 12))

grid = gridspec.GridSpec(ncols=6, nrows=3, figure=fig)

ax1 = fig.add_subplot(grid[0, :2])

ax1.set_title('Trestbps Distribution')

sns.distplot(train[continuous[1]],
                 hist_kws={
                 'rwidth': 0.85,
                 'edgecolor': 'black',
                 'alpha': 0.8},
                 color=cust_palt[0])

ax15 = fig.add_subplot(grid[0, 2:3])

ax15.set_title('Trestbps')

sns.boxplot(train[continuous[1]], orient='v', color=cust_palt[0])

ax2 = fig.add_subplot(grid[0, 3:5])

ax2.set_title('Chol Distribution')

sns.distplot(train[continuous[2]],
                 hist_kws={
                 'rwidth': 0.85,
                 'edgecolor': 'black',
                 'alpha': 0.8},
                 color=cust_palt[1])

ax25 = fig.add_subplot(grid[0, 5:])

ax25.set_title('Chol')

sns.boxplot(train[continuous[2]], orient='v', color=cust_palt[1])

ax3 = fig.add_subplot(grid[1, :2])

ax3.set_title('Thalach Distribution')

sns.distplot(train[continuous[3]],
                 hist_kws={
                 'rwidth': 0.85,
                 'edgecolor': 'black',
                 'alpha': 0.8},
                 color=cust_palt[2])

ax35 = fig.add_subplot(grid[1, 2:3])

ax35.set_title('Thalach')

sns.boxplot(train[continuous[3]], orient='v', color=cust_palt[2])

ax4 = fig.add_subplot(grid[1, 3:5])

ax4.set_title('Oldpeak Distribution')

sns.distplot(train[continuous[4]],
                 hist_kws={
                 'rwidth': 0.85,
                 'edgecolor': 'black',
                 'alpha': 0.8},
                 color=cust_palt[3])

ax45 = fig.add_subplot(grid[1, 5:])

ax45.set_title('Oldpeak')

sns.boxplot(train[continuous[4]], orient='v', color=cust_palt[3])

ax5 = fig.add_subplot(grid[2, :4])

ax5.set_title('Age Distribution')

sns.distplot(train[continuous[0]],
                 hist_kws={
                 'rwidth': 0.95,
                 'edgecolor': 'black',
                 'alpha': 0.8},
                 color=cust_palt[4])

ax55 = fig.add_subplot(grid[2, 4:])

ax55.set_title('Age')

sns.boxplot(train[continuous[0]], orient='h', color=cust_palt[4])

plt.show()

"""
Here we can do these observations:

Males are much more likely for heart diseases.

Chest pain type is very subjective and has no direct relation on the outcome, asymptomatic chest pains having highest disease outcome.

Blood sugar has no direct effect on the disease.

Rest ECG results showing no direct results but having normal ECG is pretty good sign. Even though it's pretty rare in the data, if you ST-T wave abnormality you are 3 times more likely to have heart disease.

Having exercise induced angina is pretty strong indicator for heart disease, patients are almost 3 times more likely to have disease if they have exercise induced angina. Meanwhile it's less than half for not having it.

Patients who had flat slope distribution are more likely to have disease.

Number of major vessels observed seems on similar levels for patients who have disease but 0 
observations is good sign for not having disease.

Having defected thalium test results is pretty strong indicator for heart disease."""








