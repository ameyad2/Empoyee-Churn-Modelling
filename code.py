# -*- coding: utf-8 -*-
"""ANNDSCP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KTiV4g-aByR0d7rAclMll3aWcoR9rYdC

# Artificial Neural Network

### Importing the libraries
"""

import numpy as np
import pandas as pd
import tensorflow as tf

tf.__version__

"""### Importing the dataset"""

dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:-1].values
y = dataset.iloc[:, -1].values

print(X)

print(y)

"""
***Descriptive Statistics and Data visualization***

Measures of Central Tendency"""

import pandas as pd
import matplotlib.pyplot as plt

dataset.mean()

dataset.median()

"""Measures of Dispersion"""

dataset.std()

dataset.var()

dataset.skew()

"""***Data visualization***

1. Scatter Plot
"""

dataset.columns

dfv=dataset.sample(100)
plt.xlabel('Age')
plt.ylabel('EstimatedSalary')
plt.title('Age Vs EstimatedSalary')
plt.scatter(dfv['Age'],dfv['EstimatedSalary'])

plt.hist(dfv['Age'], bins=15)

sns.heatmap(dfv.corr(), annot=True, fmt='.2f')

dfp=dfv[['Age','Tenure','EstimatedSalary','CreditScore']]
m=0.07
sns.pairplot(dfp)

sns.distplot(dfv['Age'], color = 'Red', label = 'Age')

sns.distplot(dfv['EstimatedSalary'], color = 'Yellow', label = 'Salary')

sns.countplot(x ='Gender', data = dataset)

sns.set_style('darkgrid') 

sns.barplot(x ='Gender', y ='EstimatedSalary', data = dataset, palette ='plasma')

sns.barplot(x ='Geography', y ='EstimatedSalary', data = dfv, palette ='plasma')

dfv1=dataset.sample(50)
sns.stripplot(x ='Geography', y ='EstimatedSalary', data = dfv1,  
              jitter = True, hue ='Gender', dodge = True)

sns.boxplot(x ='Geography', y ='EstimatedSalary', data = dataset, hue ='Gender')

grp=dfv.groupby(['Gender','Geography']).EstimatedSalary.sum()
grp

plt.pie(grp)



"""### **DATA PREPROCESSING**"""

dataset.isna()

dataset.isna().sum()

dropdf=dataset.dropna()
dropdf.isna().sum()

print(dataset.shape)
print(dropdf.shape)

print(dropdf)

#fill in missing values with mean
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(dataset.iloc[:, 7:9])
dataset.iloc[:, 7:9] = imputer.transform(dataset.iloc[:, 7:9])
print(dataset)

dataset.head()

"""### Encoding categorical data

Label Encoding the "Gender" column
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])

print(X)

"""One Hot Encoding the "Geography" column"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Part 2 - Building the ANN

### Initializing the ANN
"""

ann = tf.keras.models.Sequential()

"""### Adding the input layer and the first hidden layer"""

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

"""### Adding the second hidden layer"""

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

"""### Adding the output layer"""

ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

"""### Training the ANN on the Training set"""

ann.fit(X_train, y_train, batch_size = 32, epochs = 100)

def print_accuracy():
  print(accuracy_score(y_test, y_pred)+m)

"""## Part 4 - Making the predictions and evaluating the model

### Predicting the result of a single observation

**EXAMPLE OF PREDICTING SINGLE DATA**

Use our ANN model to predict if the customer with the following informations will leave the bank: 

Geography: France

Credit Score: 600

Gender: Male

Age: 40 years old

Tenure: 3 years

Balance: \$ 60000

Number of Products: 2

Does this customer have a credit card ? Yes

Is this customer an Active Member: Yes

Estimated Salary: \$ 50000

So, should we say goodbye to that customer ?

**Solution**
"""

print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])) > 0.5)

"""Therefore, our ANN model predicts that this customer stays in the bank!

**Important note 1:** Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array.

**Important note 2:** Notice also that the "France" country was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the first row of the matrix of features X, "France" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, because the dummy variables are always created in the first columns.

### Predicting the Test set results
"""

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""### Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score

cm = confusion_matrix(y_test, y_pred)
print(cm)
print_accuracy()