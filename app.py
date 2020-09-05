from flask import Flask, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import flasgger
from flasgger import Swagger
app=Flask(__name__)
Swagger(app)
pickle_file=open("classifier.pkl","rb")
classifier=pickle.load(pickle_file)

@app.route('/')
def welcome():
    return "Hi there"

@app.route('/predict', methods=["Get"])
def predict_decision():
    """Date or Ditch? 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: Attractive
        in: query
        type: number
        required: true
      - name:  Shared_Interests
        in: query
        type: number
        required: true
      - name:  Fun
        in: query
        type: number
        required: true
      - name:  Sincere
        in: query
        type: number
        required: true
      - name:  Intelligent
        in: query
        type: number
        required: true
      - name:  Ambitious
        in: query
        type: number
        required: true
      - name: Gender
        in: query
        type: string
        required: true      
    responses:
        200:
            description: Decision taken by the user.
        
    """

    Attractive= request.args.get("Attractive")
    Sincere= request.args.get("Sincere")
    Intelligent= request.args.get("Intelligent")
    Fun= request.args.get("Fun")
    Ambitious= request.args.get("Ambitious")
    Shared_Interests= request.args.get("Shared_Interests")
    Gender=request.args.get("Gender")
    if Gender=="Female":
        Gender=0
    elif Gender=="Male":
        Gender=1    
    prediction=classifier.predict([[Attractive,Shared_Interests,Fun,Sincere,Intelligent,Ambitious,Gender]])
    decision=str(prediction)
    if int(decision[1])==1:
        return "Date"
    elif int(decision[1])==0:
        return "Ditch"   
@app.route('/predict_file',methods=["POST"])
def predict_decision_file():
    """Date or Ditch? 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: file
        in: formData
        type: file
        required: true
    responses:
        200:
            description:  Decision taken by the user.
        
    """
    df=pd.read_csv(request.files.get("file"))
    rows,columns=df.shape
    
    try:
        for i in rows:
           if df.iloc[i,6]=="Male":
              df.iloc[i,6]=1
           elif df.iloc[i,6]=="Female":
              df.illoc[i,6]=0
    except:
        pass
    
    prediction=classifier.predict(df)
    prediction_list=list(prediction)
    decision_list=[]
    for dec in prediction_list:
        if dec==1:
            decision_list.append("Date")
        elif dec==0:
            decision_list.append("Ditch")    
    
    return str(decision_list)

if __name__ == '__main__':
    app.run()