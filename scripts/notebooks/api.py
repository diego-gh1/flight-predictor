
import pickle
from fastapi import FastAPI
import joblib
import json
from geopy.distance import geodesic
import pandas as pd



with open('archivo.txt', 'r') as archivo:
    diccionario_aeropuertos = json.load(archivo)

app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}

def load_model ():
    model_pipeline = pickle.load(open("../../Models/pipeline_XGBoost_1.pkl","rb"))
    return model_pipeline

@app.get('/predict')

def predict(aeropuerto_origen,aeropuerto_destino,dia,mes,dia_de_semana,horario,aerolinea, scheduled_time, scheduled_arrival):

    lat_origin = diccionario_aeropuertos[aeropuerto_origen][0]
    long_origin = diccionario_aeropuertos[aeropuerto_origen][1]
    lat_dest = diccionario_aeropuertos[aeropuerto_destino][0]
    long_dest = diccionario_aeropuertos[aeropuerto_destino][1]

    distancia_km = geodesic((lat_origin, long_origin), (lat_dest, long_dest)).kilometers

    # Convertir la distancia a millas
    distancia_millas = distancia_km * 0.621371

    print("Distancia entre los puntos:", distancia_millas, "millas")

    columns_name= ['MONTH', 'DAY', 'DAY_OF_WEEK', 'SCHEDULED_TIME', 'DISTANCE',
       'SCHEDULED_ARRIVAL', 'ORIGIN_LONGITUDE', 'ORIGIN_LATITUDE',
       'DESTINATION_LONGITUDE', 'DESTINATION_LATITUDE','AIRLINE']

    params_columnas = [mes,dia,dia_de_semana, scheduled_time,distancia_millas,scheduled_arrival,long_origin,lat_origin,long_dest,lat_dest,aerolinea]

    df= pd.DataFrame([params_columnas],columns=columns_name)

    model=load_model()
    print(type(model))

    preds=model.predict(df)


    print (preds)

    return {'status':'OK', 'predictions':str(preds[0])}
