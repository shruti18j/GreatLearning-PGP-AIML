# -*- coding: utf-8 -*-
"""Project 2 - Supervised Learning_Banking.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ByrFpe-dB6zPG2GrIBN4O3q7oURR0_7s

# Project Description:
A project from Banking domain containing customer demographic information, the customer relationship with the bank and the customer response to the last personal loan campaign.

# Context:
This case is about a bank (Thera Bank) whose management wants to explore ways of converting its liability customers to personal loan customers (while retaining them as depositors). A campaign that the bank ran last year for liability customers showed a healthy conversion rate of 9% success. This has encouraged the retail marketing department to devise campaigns with better target marketing to increase the success ratio with minimal budget.

# Data Description:

The file **Bank_Personal_Loan_Modelling.csv** contains data on 5000 customers. The data include customer demographic information alongwith the customer's relationship with the bank and customer response to the last personal loan campaign. The various attributes are discussed as below:,
   
**ID:** This column contains the Customer ID. Each ID is specific to a customer.

**Age:** This column contains the age of the customer ranging from 23 to 67.

**Experience:** This column contains the data how much years of professional experience the customer have. The values ranges from -3 to 43.

**Income:** This column contains the annual income of the customer. It ranges from 8 thousand dollars to 224 thousand dollars.

**ZIP Code:** This column contains customer's home address ZIP code.


**Family:** It conatins the family size of the customer with value ranging from 1 to 4.

**CCAvg:** It contains the average spending on credit cards per month. It ranges from 0 thousand dollars to 10 thousand dollars.

**Education Level:** This column contains the education Level of the customers. Here only three level of education are considered - Undergrad (depicted by 1 in the file), Graduate (depicted by 2 in the file) and Advanced/ Professional (depicted by 3 in the file).

**Mortgage:** It contains the value of the house in mortgage (if any) with values ranging from 0 thousand dollars (indicating that the customer's house is 
not on mortgage) to 635 thousand dollars.

**Personal Loan:** This column contains the response of the customer whether it accepted the personal loan offered in the last campaign or not. The responses are stored as 0 (didn't accepted the loan when offered in the last campaign) and 1 (accepted the loan when offered in the last campaign).

**Securities Account:** This column contains the response whether the customer have a securities account with the bank or not. Here 0 indicates that the customer doesn't have a securities account and 1 indicates he does have.

**CD Account:** This column contains the response whether the customer have a certificate of deposit (CD) account with the bank or not. Here 0 indicates that the customer doesn't have a CD account and 1 indicates he does have.

**Online:** This column contains the response whether the customer avails internet banking facilities or not. Here 0 indicates that the customer doesn't uses internet banking facilities and 1 indicates he does uses.

**CreditCard:** This column contains information whether the customer uses a credit card issued by Universal Bank or not. Here 0 indicates that the customer doesn't uses a credit card and 1 indicates he does uses."

# Objective:
The classification goal is to predict the likelihood of a liability customer buying personal loans.

#### Import necessary libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive

drive.mount('/content/drive')

"""#### Read the csv file to form a dataframe"""

path = "/content/drive/MyDrive/Colab Notebooks/02. Supervised Machine Learning/Bank_Personal_Loan_Modelling.csv"

bank_data = pd.read_csv(path)
bank_data.head()

"""#### Shape of the data"""

bank_data.shape

"""The two-dimensional dataframe i.e., bank_data consists of 5000 rows and 14 columns.

#### Dataframe of each attribute
"""

bank_data.info()

"""All the attributes contains numerical values.

#### To check presence of missing values
"""

bank_data.isnull().sum()

"""None of the columns have null values.

### Data distribution in each attribute

#### Finding unique value in each attribute
"""

bank_data.apply(lambda x: len(x.unique()))

"""**ID** have 5000 unique values, thus signifying that each customer has a unique ID. Columns **Personal Loan**,**Securities Account**, **CD Account**, **Online**, **Credit Card** each have two values.

As attributes **ID** and **ZIP Code** are just numbers of series, so we can drop them from our further analysis.
"""

bank_data.drop('ID', axis = 1, inplace = True)
bank_data.drop('ZIP Code', axis = 1, inplace = True)
bank_data.head()

"""#### 5 point summary of numerical attributes"""

bank_data.describe().T

"""The numerical attributes are summarised in the following manner:

i. **Age:** There are 5000 records with a mean value of 45.3384 years old. The minimum and maximum age of the persons taken under observation is 23 and 67 years old respectively. 25% of people are below 35 years of age, 50% of people are below 45 years of age whereas 75% of people are under 55 years of age. Also, the observations differ from the mean value by 11.463166

ii. **Experience:** There are 5000 records with a mean value of 20.1046 years. The minimum and maximum years of the experience the customers have are -3 and 43 years respectively. 25% of people have experience below 10 years, 50% of people have below 20 years of experience and 75% of people have an experience less than 30 years. Also, the observations differ from the mean value by 11.467954 years

iii. **Income:** There are 5000 records with a mean earning of 73.7742 thousand dollars. The minimum and maximum income of the customers taken under observation are 8000 and 224,000 dollars respectively. 25% of people have earnings below 39000 dollars, 50% of people earns below 64000 dollars whereas 75% of people earns under 98,000 dollars. Also, the observations differ from the mean value by 46.033729 thousand dollars

iv. **Family:** There are 5000 records with a mean family size of 2.3964. The minimum and maximum family size of the persons taken under observation is 1 and 4 respectively

v. **CCAvg:** There are 5000 records with a mean credit card spending of 1.937938 thousand dollars. The credit card spendings by the persons taken under observation ranges from 0 to 10 thousand dollars. 25% of people spends below 0.7 thousand dollars, 50% of people spends below 1.5 thousand dollars whereas 75% of people spends under 2.5 thousand dollars. Also, the observations differ from the mean value by 1.747659 thousand dollars

vi. **Mortgage:** There are 5000 records with a mean mortgage value of 56.4988 thousand dollars. The amount of mortgage ranges from 0 to 635 thousand dollars. It is clear that there are huge number of customers that aren't having mortgage value on their home. Also, the observations differ from the mean value by 101.713802 thousand dollars.

Apart from these, there are attributes like **Education** which suggests that maximum number of customers had achieved Undergrad level of education. From attribute **Personal Loan, Securities Account and CD Account** it is clear that quite a small number of customers had accepted personal loans, have securities account and certificate of deposit account in the bank respectively. From attribute **Online** it can be inferred that the number of customers using internet banking facilties is slightly more than the ones not using it.

Since, from the above we can see that the attribute **Experience** have some negative values. So, lets replace the negative values with the median.
"""

# Finding the number of rows having negative Experience values:
bank_data[bank_data['Experience']<0]['Experience'].count()

# Replacing the negative value with the median of the column:
exp_med = bank_data.loc[:,'Experience'].median()
bank_data.loc[:,'Experience'].replace([-1, -2, -3], [exp_med, exp_med, exp_med], inplace = True)

# To check if there is any rows with negative values:
any(bank_data['Experience'] < 0)

"""Thus, there isn't any records having negative values for **Experience**.

#### 5 point summary after removing the negative values from **Experience**
"""

bank_data.describe().T

"""#### Univariate Analysis:"""

# plotting of 'Age':
sns.distplot(bank_data['Age'], rug = True)

"""From the above plot it seems that the curve is fairly symmetrical. A large chunk of the customers have their age in the range of 30-60 years."""

# measure of skewness of 'age':
bank_data['Age'].skew()

"""**Negative skew** refers to a longer or fatter tail on the left side of the distribution, while **positive skew** refers to a longer or fatter tail on the right. The mean of positively skewed data will be greater than the median.

A negative skewness value in the output indicates an asymmetry in the distribution and the tail is larger towards the left hand side of the distribution.

The curve is slightly **negatively skewed**.
"""

import pandas as pd

 

dataVal = [(10,20,30,40,50,60,70),

           (10,10,40,40,50,60,70),

           (10,20,30,50,50,60,80)]

dataFrame = pd.DataFrame(data=dataVal);

skewValue = dataFrame.skew(axis=1)

 

print("DataFrame:")

print(dataFrame)

 

print("Skew:")

print(skewValue)

"""https://pythontic.com/pandas/dataframe-computations/skew

A skewness value of 0 in the output denotes a symmetrical distribution of values in row 1.

A negative skewness value in the output indicates an asymmetry in the distribution corresponding to row 2 and the tail is larger towards the left hand side of the distribution.

A positive skewness value in the output indicates an asymmetry in the distribution corresponding to row 3 and the tail is larger towards the right hand side of the distribution.


https://www.investopedia.com/terms/s/skewness.asp
The **mean of positively skewed data will be greater than the median**. In a distribution that is negatively skewed, the exact opposite is the case: the m**ean of negatively skewed data will be less than the median**. If the data graphs symmetrically, the distribution has zero skewness, regardless of how long or fat the tails are.
"""

# presence of outliers in 'age':
sns.boxplot(bank_data['Age'])

"""From the above plot it is clear that the attribute **'Age'** doesn't have any outliers."""

# plotting of 'Experience':
sns.distplot(bank_data['Experience'], rug = True)

"""From the plot it is clear that the curve is fairly symmetrical. Very less people with higher experience exists."""

# measure of skewness of 'Experience':
bank_data['Experience'].skew()

"""The curve is slightly negatively skewed."""

# presence of outliers in 'Experience':
sns.boxplot(bank_data['Experience'])

"""From the above plot it is clear that **'Experience'** doesn't have any outliers."""

# plotting of 'Income':
sns.distplot(bank_data['Income'], rug = True)

"""From the graph it is clear that majority of the customers have income between 45,000 to 55,000 dollars."""

# measure of skewness of 'Income':
bank_data['Income'].skew()

"""A positive skewness value in the output indicates an asymmetry in the distribution and the tail is larger towards the right hand side of the distribution.

The curve is positively skewed.
"""

# presence of outliers in 'Income':
sns.boxplot(bank_data['Income'])

"""There are some outliers in **'Income'**. The number of outliers can be calculated as:"""

inc_25 = np.percentile(bank_data['Income'], 25)
inc_75 = np.percentile(bank_data['Income'], 75)
iqr_inc = inc_75 - inc_25
cutoff_inc = 1.5 * iqr_inc
low_lim_inc = inc_25 - cutoff_inc
upp_lim_inc = inc_75 + cutoff_inc

outlier_inc = [x for x in bank_data['Income'] if x < low_lim_inc or x > upp_lim_inc]
print("The number of outliers in 'Income' out off 5000 records are:", len(outlier_inc))

"""Thus, there are 96 customers having extreme Income."""

# plotting of 'Family':
sns.countplot(bank_data['Family'])

"""From the above plot it is clear that most of the customers are single. Whereas, the share of customers having family size of 3 is the least."""

# plotting of 'CCAvg':
sns.distplot(bank_data['CCAvg'], rug = True)

"""From the above plot, it is clear that most of the customers have an average spending of 0 to 2000 dollars per month on their credit card."""

# measure of skewness of 'CCAvg':
bank_data['CCAvg'].skew()

"""A positive skewness value in the output indicates an asymmetry in the distribution and the tail is larger towards the right hand side of the distribution.

The curve is positively skewed.
"""

# presence of outliers in 'CCAvg':
sns.boxplot(bank_data['CCAvg'])

"""There are a lot of outliers in 'CCAvg'. The number of outliers can be calculated as:"""

cc_25 = np.percentile(bank_data['CCAvg'], 25)
cc_75 = np.percentile(bank_data['CCAvg'], 75)
iqr_cc = cc_75 - cc_25
cutoff_cc = 1.5 * iqr_cc
low_lim_cc = cc_25 - cutoff_cc
upp_lim_cc = cc_75 + cutoff_cc

outlier_cc = [x for x in bank_data['CCAvg'] if x < low_lim_cc or x > upp_lim_cc]
print("The number of outliers in 'CCAvg' out off 5000 records are:", len(outlier_cc))

"""Thus, 325 customers have extreme spendings on their credit card."""

# plotting of 'Education':
sns.countplot(bank_data['Education'])

"""Maximum number of customers have completed education upto Undergrad level."""

# plotting of 'Mortgage':
sns.distplot(bank_data['Mortgage'], rug = True)

"""Most of the customers don't have mortgages on their homes."""

# measure of skewness of 'Mortgage':
bank_data['Mortgage'].skew()

"""The curve is highly positively skewed."""

# presence of outliers in 'Mortgage':
sns.boxplot(bank_data['Mortgage'])

"""outliers are present in 'Mortgage'. The number of outliers can be calculated as:"""

mort_25 = np.percentile(bank_data['Mortgage'], 25)
mort_75 = np.percentile(bank_data['Mortgage'], 75)
iqr_mort = mort_75 - mort_25
cutoff_mort = 1.5 * iqr_mort
low_lim_mort = mort_25 - cutoff_mort
upp_lim_mort = mort_75 + cutoff_mort

outlier_mort = [x for x in bank_data['Mortgage'] if x < low_lim_mort or x > upp_lim_mort]
print("The number of outliers in 'Mortgage' out off 5000 records are:", len(outlier_mort))

"""Thus, there are 291 customers that have extreme mortgage on their homes."""

# plotting of 'Securities Account':
sns.countplot(bank_data['Securities Account'])

"""Majority of the customers don't have securities account with the bank."""

# plotting of 'CD Account':
sns.countplot(bank_data['CD Account'])

"""Majority of the customers don't have CD account with the bank."""

# plotting of 'Online':
sns.countplot(bank_data['Online'])

"""Number of customers using internet banking facilities is more than the ones not using it."""

# plotting of 'CreditCard':
sns.countplot(bank_data['CreditCard'])

"""Majority of the customers don't use a credit card issued by UniversalBank.

#### Bivariate Analysis:
"""

# plotting of 'Age' and 'Experience':
sns.scatterplot(bank_data['Experience'], bank_data['Age'])

"""**Experience** increases **Age** also increases, thus somewhat signifying a positive linear relationship."""

# plotting of 'Experience' and 'Income':
plt.figure(figsize = (20,5))
sns.boxplot(x = 'Experience', y = 'Income', data = bank_data)

"""Customer having an **Experience** of 24 years earns most whereas customer having an **Experience** of 42 years earns the least among the observed customers."""

# plotting of 'Income' and 'Family':
sns.boxplot(x = 'Family', y = 'Income', data = bank_data)

"""The customer having a family size of 2 earns the most."""

# plotting of 'Income' and 'Education':
sns.boxplot(x = 'Education', y = 'Income', data = bank_data)

"""Highest Income is earned by the customer who has achieved Undergrad level of education."""

# plotting of 'Income' and 'Securities Account':
sns.boxplot(x = 'Securities Account', y = 'Income', data = bank_data)

"""Customer who has the highest annual Income doesn't have a Securities Account with the bank."""

# plotting of 'CD Account' and 'Income':
sns.boxplot(x = 'CD Account', y = 'Income', data = bank_data)

"""Customer who has the highest annual income doesn't have a CD Account with the bank."""

# plotting of 'CreditCard' and 'Income':
sns.boxplot(x = 'CreditCard', y = 'Income', data = bank_data)

"""Customer who has the highest annual Income doesn't uses a Credit Card issued by bank.

Multivariate Analysis:
"""

# pairplot
sns.pairplot(bank_data)

"""Most of the attributes (other than Age , Experience, CCAvg , income and Personal Loan) doesn't have any strong linear relationship between them.

## Get the target column distribution. Your comments. : Here, **Personal Loan** is the target variable.

#### Univariate Analysis
"""

# plotting of 'Personal Loan':
sns.countplot(bank_data['Personal Loan'])

"""Majority of the observed customers didn't opted for Personal Loan.

#### Bivariate Analysis
"""

# calculating the mean 'Age' of the customers buying 'Personal Loan' and those who don't:
bank_data.groupby('Personal Loan')['Age'].mean().plot(kind = 'bar')

"""There isn't any difference in the mean age of the customers availing personal loan and customers who didn't availed Personal Loan. The y axis represents the mean of **Age**"""

print(bank_data.groupby('Personal Loan')['Age'].min())
print(bank_data.groupby('Personal Loan')['Age'].max())

"""***customers who didn't availed Personal Loan :***

minimum age = 23 

maximum age = 67

***customers who availed Personal Loan :***

minimum age = 26
maximum age = 65 
"""

# calculation of mean value of 'Experience' of customers having 'Personal Loan' and not having it:
bank_data.groupby('Personal Loan')['Experience'].mean().plot(kind = 'bar')

"""Mean Experience of customers not availing Personal Loan is more than the customers that had availed Personal Loan"""

# calculating the mean value of 'Income' for the customers having 'Personal Loan' and those not having:
bank_data.groupby('Personal Loan')['Income'].mean().plot(kind = 'bar')

"""Mean annual income of the customers availing Personal Loan is much higher than the customers not availing Personal Loan. So,income can be a good indicator whether a customer will take Personal Loan or not, as high income suggests that a customer can avail Personal Loan. The same can be ascertained from the below graph:"""

sns.distplot(bank_data[bank_data['Personal Loan'] == 0]['Income'], color = 'r')
sns.distplot(bank_data[bank_data['Personal Loan'] == 1]['Income'], color = 'g')

# plotting of 'Personal Loan' and 'Family':
fam = pd.crosstab(bank_data['Family'], bank_data['Personal Loan'])
print('Cross tabulation can be given as: ','\n', fam)
sns.countplot(bank_data['Family'], hue = bank_data['Personal Loan'])

"""The number of family members doesn't affect the probability of a customer whether he/she will avail Personal Loan or not."""

# calculating the mean value of 'CCAvg' for customers buying 'Personal Loan' and those who don't:
bank_data.groupby('Personal Loan')['CCAvg'].mean().plot(kind = 'bar')

"""Mean average spending on Credit Card per month by the customers availing Personal Loan is much higher than the customers not availing Personal Loan. So, average spending on Credit Card per month can also be a good indicator whether a customer will avail Personal Loan or not, as higher spendings indicate that a customer can avail Personal Loan. The same can be ascertained from the below graph:"""

sns.distplot(bank_data[bank_data['Personal Loan'] == 0]['CCAvg'], color = 'r')
sns.distplot(bank_data[bank_data['Personal Loan'] == 1]['CCAvg'], color = 'g')

# plotting of 'Personal Loan' and 'Education':
edu = pd.crosstab(bank_data['Education'], bank_data['Personal Loan'])
print('Cross tabulation can be given as :', '\n', edu)
sns.countplot(bank_data['Education'], hue = bank_data['Personal Loan'])

"""Maximum customers who availed Personal Loan had achieved Advanced/Professional level of Education."""

# calculating the mean value of 'Mortgage' for customers buying 'Personal Loan' as compared to those who don't:
bank_data.groupby('Personal Loan')['Mortgage'].mean().plot(kind = 'bar')

"""Mean mortgage value of the customers availing Personal Loan is much higher than the customers not availing Personal Loan. --58
https://github.com/ramanks19/AIML-Projects/blob/main/02.%20Supervised%20Machine%20Learning/Project%202%20-%20Supervised%20Learning_Banking.ipynb

https://raw.githubusercontent.com/ramanks19/AIML-Projects/main/02.%20Supervised%20Machine%20Learning/Project%202%20-%20Supervised%20Learning_Banking.ipynb
"""

# plotting of 'Personal Loan' and 'Securities Account':
sec_acc = pd.crosstab(bank_data['Securities Account'], bank_data['Personal Loan'])
print('Cross tabulation is given as: ', '\n', sec_acc)
sns.countplot(bank_data['Securities Account'], hue = bank_data['Personal Loan'])

"""Majority of customers who had availed Personal Loan belong to the group who don't have Securities Account in the bank."""

# plotting of 'Personal Loan' and 'CD Account':
cd_acc = pd.crosstab(bank_data['CD Account'], bank_data['Personal Loan'])
print('Cross tabulation is given as: ', '\n', cd_acc)
sns.countplot(bank_data['CD Account'], hue = bank_data['Personal Loan'])

"""Majority of customers who had availed Personal Loan belong to the group who don't have CD Account in the bank."""

# plotting of 'Personal Loan' and 'Online':
online = pd.crosstab(bank_data['Online'], bank_data['Personal Loan'])
print('Cross tabulation is given as: ', '\n', online)
sns.countplot(bank_data['Online'], hue = bank_data['Personal Loan'])

"""Majority of customers who had availed Personal Loan belong to the group who use internet banking facilities."""

# plotting of 'Personal Loan' and 'CreditCard':
credit = pd.crosstab(bank_data['CreditCard'], bank_data['Personal Loan'])
print('Cross tabulation is given as: ', '\n', credit)
sns.countplot(bank_data['CreditCard'], hue = bank_data['Personal Loan'])

"""Majority of customers who had availed Personal Loan belong to the group who don't have a credit card issued by bank.

#### Multivariate Analysis:
"""

# plotting of 'Education', 'Age' and 'Personal Loan':
sns.boxplot(bank_data['Education'], bank_data['Age'], hue = bank_data['Personal Loan'])

"""Customer who availed Personal Loan have the same Age distribution irrespective of their Education."""

# plotting of 'Education', 'Income' and 'Personal Loan':
sns.boxplot(x = 'Education', y = 'Income', hue = 'Personal Loan', data = bank_data)

"""The boxplot reveals that Customers having Undergraduate Education have higher incomes. 

But customers who availed personal loans have the same income distribution irrespective of their Education.
"""

# plotting of 'Education', 'Mortgage' and 'Personal Loan':
sns.boxplot(x = 'Education', y = 'Mortgage', hue = 'Personal Loan', data = bank_data)

"""The boxplot reveals that customers having Undergraduate education have higher mortgage. 

It is also clear that maximum number of customers who availed Personal Loan have Undergraduate Education.
"""

# calculating the correlation coefficient
corr = bank_data.corr()
corr

# plotting a heatmap
plt.figure(figsize = (30,10))
ax = sns.heatmap(corr, annot = True, cmap = "ocean_r")
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

"""From the above heatmap it is clear that **Age** and **Experience** are highly linearly correlated. The same was also observed in the pairplot. 

**Income** and **CCAvg** also depicts a slightly positive correlation between them.

#### Preparation of data for models

Out of all the mentioned attributes in the data sheet, we can neglect the following attribute:

**Experience**: As Experience is highly correlated with **Age (?? = 0.98)**, so it can be neglected here.
"""

# dropping 'Experience' from the dataframe:
bank_data.drop('Experience', axis = 1, inplace = True)
bank_data.head()

"""### Splitting of Data into Training and Test Set in the ratio of 70:30 respectively"""

X = bank_data.drop('Personal Loan', axis = 1)
y = bank_data['Personal Loan']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)

"""Here, the independent variables are denoted by **'X'** and the predictor is represented by **'y'**.

### Using Different Classification models to predict the likelihood of a customer buying a personal loan. Also, print the Confusion Matrix.

### Logistic Regression
"""

LogReg_model = LogisticRegression()
LogReg_model.fit(X_train, y_train)

pred_log = LogReg_model.predict(X_test)
predictprob_log = LogReg_model.predict_proba(X_test)

# print classification report and accuracy score:
print('Classification report for the model is given as:', '\n', classification_report(y_test, pred_log))
print('Accuracy obtained from the given model is:', accuracy_score(y_test, pred_log))

"""The accuracy obtained from the model is 94%. Apart from this the, Precision of this model (i.e., the proportion of predicted positives that are really positives) is 0.94."""

# Confusion Matrix:
cm_log = confusion_matrix(y_test, pred_log)

class_label = ['Positive', 'Negative']
df_cm_log = pd.DataFrame(cm_log, index = class_label, columns = class_label)
ax = sns.heatmap(df_cm_log, annot = True, fmt = 'd')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.show()

"""From the above Classification Matrix it is clear that the model has predicted 1339 records Positive which were actually positive and 12 records which were marked Positive but where actually Negative. Also, the model had correctly identified 71 records as Negative. However, the model had predicted 78 records as Negative which were actually Positive.

Although, we had got quite a high percentage of Accuracy and Precision we would still like as to see as to how the models will behave when the data is Standardized.
"""

# standardization of the training and test data set
scaled_X_train = preprocessing.StandardScaler().fit_transform(X_train)
scaled_X_test = preprocessing.StandardScaler().fit_transform(X_test)

LogReg_model_scaled = LogisticRegression()
LogReg_model_scaled.fit(scaled_X_train, y_train)

pred_log_scaled = LogReg_model_scaled.predict(scaled_X_test)
predictprob_log_scaled = LogReg_model_scaled.predict_proba(scaled_X_test)

# print classification report and accuracy score:
print('Classification report for the model after scaling is given as:', '\n', classification_report(y_test, pred_log_scaled))
print('Accuracy obtained from the given model after scaling is:', accuracy_score(y_test, pred_log_scaled))

"""The accuracy and prediction obtained from this model after standardizing the data set is 94.8% and 0.96 respectively (which is a slight increase when compared to ones obtained through non-standardized dataset)."""

# Confusion Matrix:
cm_log_scale = confusion_matrix(y_test, pred_log_scaled)

class_label = ['Positive', 'Negative']
df_cm_log_scale = pd.DataFrame(cm_log_scale, index = class_label, columns = class_label)
ax = sns.heatmap(df_cm_log, annot = True, fmt = 'd')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.show()

"""The results in the Confusion Matrix is same as that of obtained from non-standardized dataset.

### K-NN
"""

# Creating odd list of K for KNN
myList = list(range(1,20))

# subsetting just the odd ones
neighbors = list(filter(lambda x: x % 2 != 0, myList))

# Empty list to hold accuracy scores
ac_scores_knn = []

for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(scaled_X_train, y_train)
    
    y_pred = knn.predict(scaled_X_test)
    
    scores = accuracy_score(y_test, y_pred)
    ac_scores_knn.append(scores)
    
MSE = [1 - x for x in ac_scores_knn]

optimal_k = neighbors[MSE.index(min(MSE))]
print('The optimal number of neighbors is %d' % optimal_k)

plt.plot(neighbors, ac_scores_knn)

"""So, here we will consider the value of k = 3."""

knn_model = KNeighborsClassifier(n_neighbors = optimal_k, weights = 'uniform', metric = 'euclidean')
knn_model.fit(scaled_X_train, y_train)

pred_knn = knn_model.predict(scaled_X_test)
predictprob_knn = knn_model.predict_proba(scaled_X_test)

# print classification report and accuracy score:
print('Classification report for the model is given as:', '\n', classification_report(y_test, pred_knn))
print('Accuracy obtained from the given model is:', accuracy_score(y_test, pred_knn))

"""The accuracy obtained from the model is 95.87%. Apart from this the, Precision of this model (i.e., the proportion of predicted positives that are really positives) is 0.96."""

# Confusion Matrix:
cm_knn = confusion_matrix(y_test, pred_knn)

class_label = ['Positive', 'Negative']
df_cm_knn = pd.DataFrame(cm_knn, index = class_label, columns = class_label)
ax = sns.heatmap(df_cm_knn, annot = True, fmt = 'd')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.show()

"""From the above Classification Matrix it is clear that the model has predicted 1341 records Positive which were actually positive and 10 records as False Positive. Also, the model had correctly identified 97 records as Negative. However, the model had predicted 52 records as Negative which were actually Positive.

Naive Bayes

### Naive Bayes
"""

naive_model = GaussianNB()
naive_model.fit(scaled_X_train, y_train)

pred_nb = naive_model.predict(scaled_X_test)
predictprob_nb = naive_model.predict_proba(scaled_X_test)

# print classification report and accuracy score:
print('Classification report for the model is given as:', '\n', classification_report(y_test, pred_nb))
print('Accuracy obtained from the given model is:', accuracy_score(y_test, pred_nb))

"""The accuracy obtained from the model is 87.2%. Apart from this the, Precision of this model (i.e., the proportion of predicted positives that are really positives) is 0.95."""

# Confusion Matrix:
cm_nb = confusion_matrix(y_test, pred_nb)

class_label = ['Positive', 'Negative']
df_cm_nb = pd.DataFrame(cm_nb, index = class_label, columns = class_label)
ax = sns.heatmap(df_cm_nb, annot = True, fmt = 'd')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.show()

"""From the above Classification Matrix it is clear that the model has predicted 1224 records as Positive which were actually positive and 127 records as False Positive. Also, the model had correctly identified 84 records as Negative. However, the model had predicted 65 records as False Negative.

### Give your reasoning on which is the best model in this case

Before deciding which model (Logistic Regression, KNN and Naive Bayes) is best lets summarise the results from each of the model. All the three models had predicted 1351 records as Positive and 149 records as Negative with varying amount of True Positive, True Negative, False Positive and False Negative.

**Logistic Regression:**

This algorithm provided an accuracy of 94% and a precision of 0.96 on standardized training and test data set. Apart from this, it also correctly predicted 1338 records as Positive and 76 records as negative. However it also predicted 13 records as Positive which were actually negative and 73 as Negative which were actually Positive.

**KNN (K-Nearest Neighbor):**

This algorithm provided an accuracy of 95.87 % and a precision of 0.96. Apart from this, it also correctly predicted 1341 records as Positive and 97 records as negative. However it also predicted 10 records as Positive which were actually negative and 52 as Negative which were actually Positive.

**Naive Bayes:**

This algorithm provided an accuracy of 87.2 % and a precision of 0.95. Apart from this, it also correctly predicted 1224 records as Positive and 84 records as negative. However it also predicted 127 records as Positive which were actually negative and 65 as Negative which were actually Positive.

Thus, we can see that KNN has the best accuracy among all the three algorithms that has been used here. Apart from these it had also identified the most number of True Positive Records and least False negative records.

**Thus, in this case we can say that KNN (K-Nearest Neighbor) is the best model out of the three.**
"""