#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


# In[2]:


data=pd.read_csv("enron_spam_data.csv", encoding="latin-1")


# In[3]:


data.drop(['Subject', 'Date', 'Message ID'], axis=1, inplace=True)


# In[4]:


data.head()


# In[5]:


data.isna().sum()


# In[6]:


data = data.dropna().reset_index(drop=True)


# In[7]:


data.isna().sum()


# In[8]:


data.head()


# In[9]:


data["Message"][0]


# In[10]:


import re

corpus = []
length = len(data)
for i in range(0,length):
    text = re.sub("[^a-zA-Z0-9]"," ",data["Message"][i])
    text = text.lower()
    text = text.split()
    pe = PorterStemmer()
    stopword = stopwords.words("english")
    text = [pe.stem(word) for word in text if not word in set(stopword)]
    text = " ".join(text)
    corpus.append(text)


# In[11]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=35000)
X = cv.fit_transform(corpus).toarray()


# In[12]:


y=data['Spam/Ham']


# In[13]:


len(X)


# In[14]:


len(y)


# In[15]:


y


# In[16]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 20)


# In[ ]:


from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()

model.fit(X_train, y_train)


# In[ ]:


y_pred=model.predict(X_test)


# In[ ]:


y_pred = list(map(lambda pred: 1 if pred=="spam" else 0, y_pred))


# In[ ]:


y_test = list(map(lambda test: 1 if test=="spam" else 0, y_test))


# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score, precision_score, recall_score

cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test,y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
print(recall)
print(precision)
print(accuracy)
print(cm)


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt

target_names = ['Ham', 'Spam']

fig = plt.figure(figsize=(2,2))
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')
ax.set_xlabel('Predicted Labels')
ax.set_ylabel('True Labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(target_names)
ax.yaxis.set_ticklabels(target_names)


# In[23]:


import joblib


# In[24]:


joblib.dump(model, "NB_model.joblib")


# In[25]:


joblib.dump(cv, "countVect.joblib")


# In[26]:


############# CODES TO WRITE IN THE BACKEND OF STREAMLIT


# In[27]:


# Install these packages in the environment of streamlit (if you have not installed previously)
get_ipython().system('pip install -U scikit-learn')
get_ipython().system('pip install nltk')
get_ipython().system('pip install joblib')
get_ipython().system('pip install pandas')


# In[28]:


# Import the packages

import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import joblib


# In[29]:


# load the model and countVectorizer pickle files which we dumped previously

model = joblib.load("NB_model.joblib")
cv = joblib.load("countVect.joblib")


# In[30]:


# Copy and paste this function in the streamlit backend code

def preprocess(input_email):
    input_email = re.sub('[^a-zA-Z]', ' ', input_email)
    input_email.lower()
    input_email = input_email.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    input_email = [ps.stem(word) for word in input_email if not word in set(all_stopwords)]
    input_email = ' '.join(input_email)
    new_corpus = [input_email]
    new_X_test = cv.transform(new_corpus).toarray()
    
    return new_X_test


# In[31]:


# Take input from the user

input_email = """attached is the latest version of the cost center assignments for the transfers out of ees . these transfers will be effective july 1 , 2001 and i need to get this to hr by friday , june 1 , 2001 to give them time to get everything effected .
i think i have incorporated all your comments , but please review one more time and make sure we have not included anyone we shouldn ' t have or excluded anyone . you ' ll note that at this point we are not forming east and west risk management cost centers . don and rogers have decided for cost management purposes to leave it consolidated at this point .
once you have signed off on your groupings , rachel massey in corporate planning will be working with each of you to forecast your q 3 and q 4 cost center expense plans .
please let me know asap of any changes and don ' t hesitate to call with questions .
thanks
wade"""


# In[32]:


# Preprocess the input_email and predit the class

new_X_test = preprocess(input_email)
new_y_pred = model.predict(new_X_test)
print(new_y_pred[0])


# In[33]:


# You don't need the code below this point in your streamlit
#######################################################################


# In[34]:


# Ham email sample from dataset

input_email = """draft summary schedule - done
separately get business controllers and rac management to rate each business
by control point ( red , amber or green ) by next thursday and arrange joint
meetings with commercial on businesses that have a poor assessment or
significantly different assessments - action mike jordan and steve young
others as soon as possible
follow up on status of investment required for weather business in oslo -
action mike jordan
investigate reporting of trades not captured on trade date within dpr on a
daily basis - action mike jordan
establish accountability for existing process for creating authorised trader
list - action steve young
change process for publishing authorisation list - placing it on commercial
bulleting board - and reference location within dpr - action mike jordan
generate an update of status re master isda - action steve young and
investigate possibility of flagging this status within gcp - action mike
jordan
determine current eol straight through process rate ( stp ) across bridges to
risk management systems - action mike jordan
define summary information on coal / p & p etc businesses for inclusion in dpr
for supervisory review by john
regards
mike"""


# In[35]:


new_X_test = preprocess(input_email)
new_y_pred = model.predict(new_X_test)
print(new_y_pred[0])


# In[36]:


from win32com.client import Dispatch
import tkinter as tk

def speak(text):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(text)
    
def result():
    test_email = [text.get()]    
    test_email = preprocess(test_email[0])
    pred = model.predict(test_email)
    
    if pred[0]=='spam':
        speak("This is a Spam email")
        print("This is a Spam email")
    else:
        speak("This is not a Spam email")
        print("This is not a Spam email")


# In[ ]:





# In[ ]:


root=tk.Tk()
root.geometry("200x200")
l2=tk.Label(root, text="Email Spam Classification Application")
l2.pack()
l1=tk.Label(root, text="Enter Your Message:")
l1.pack()
text=tk.Entry(root)
text.pack()

B=tk.Button(root, text="Click", command=result)
B.pack()

root.mainloop()


# In[ ]:




