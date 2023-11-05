import pandas as pd
import numpy as np
from fastapi import FastAPI

#Read the data

data=pd.read_csv('API_Folder/authors.csv')

#create instance called app
app=FastAPI()

@app.get('/')
def read_root():
    return{"message":"Hello, World"}

@app.get("/get_info/")
def get_info(ID:int):
    """THis code is to get the id of a person from the data """
    info=data[data.id==ID].to_dict('records')
    return (info)