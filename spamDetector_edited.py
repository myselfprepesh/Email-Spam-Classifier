import streamlit as st
# import pickle
# from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from win32com.client import Dispatch

import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import joblib

def speak(text):
	speak=Dispatch(("SAPI.SpVoice"))
	speak.Speak(text)

# Load the models, make sure the paths are accurate
model = joblib.load("new_nb_model.joblib")
cv = joblib.load("cv.joblib")

# model = pickle.load(open('spam.pkl','rb'))
# cv=pickle.load(open('vectorizer.pkl','rb'))

# Function to preprocess the email
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


def main():
	
	st.title("Email Spam Classifier")
	st.write("Detect the spam email")
	activites=["Classification","About"]
	choices=st.sidebar.selectbox("Select Activities",activites)
	if choices=="Classification":
		st.subheader("Classification")
		msg=st.text_area(label = "", height=500, max_chars=None, key=None)
		if st.button("Click Here"):
			print(msg)
			print(type(msg))
			data=[msg]
			print ("Prepesh")
			print(data)

			# vect=cv.transform(data).toarray()
			# result=model.predict(vect)

			# Make sure the "data" is in string format
			new_X_test = preprocess(data[0])	# If it is in "list" format, then use "data[0]"
			new_y_pred = model.predict(new_X_test)

			if new_y_pred[0]=="ham":
				st.success("This is Not A Spam Email")
				speak("This is Not A Spam Email")
			else:
				st.error("This is A Spam Email")
				speak("This is A Spam Email")
main()
