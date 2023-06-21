import pickle
from fastapi import FastAPI
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
    model_pipeline = pickle.load(open("pipeline_XGBoost_1.pkl","rb"))
    return model_pipeline

@app.get('/predict')

def predict(aeropuerto_origen,aeropuerto_destino,dia,mes,dia_de_semana,scheduled_arrival,aerolinea, scheduled_time):

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

    probabilidad = model.predict_proba(df)[0]

    print (preds)

    return {'status':'OK', 'predictions':str(probabilidad)}



def load_model_delay ():
    model_pipeline_delay = pickle.load(open("pipeline_dtc_nuevo.pkl","rb"))
    return model_pipeline_delay

@app.get('/predict_delays')

def predict_delays(aeropuerto_origen,aeropuerto_destino,dia,mes,dia_de_semana,scheduled_arrival,aerolinea, scheduled_time):

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

    model=load_model_delay()
    print(type(model))

    preds=model.predict(df)

    #preds = preds[0]

    #probabilidad = model.predict_proba(df)[0]

    print (preds)

    return {'status':'OK', 'predictions':str(preds[0])}


#if __name__ == "__main__":
    lat_origin = diccionario_aeropuertos['SEA'][0]
    long_origin = diccionario_aeropuertos['SEA'][1]
    lat_dest = diccionario_aeropuertos['SEA'][0]
    long_dest = diccionario_aeropuertos['SEA'][1]

    distancia_km = geodesic((lat_origin, long_origin), (lat_dest, long_dest)).kilometers

    # Convertir la distancia a millas
    distancia_millas = distancia_km * 0.621371

    print("Distancia entre los puntos:", distancia_millas, "millas")
    columns_name= ['MONTH', 'DAY', 'DAY_OF_WEEK', 'SCHEDULED_TIME', 'DISTANCE',
       'SCHEDULED_ARRIVAL', 'ORIGIN_LONGITUDE', 'ORIGIN_LATITUDE',
       'DESTINATION_LONGITUDE', 'DESTINATION_LATITUDE','AIRLINE']


    params_columnas = ['1','1','1', '200',distancia_millas,'2150',long_origin,lat_origin,long_dest,lat_dest,'HA']

    df= pd.DataFrame([params_columnas],columns=columns_name)

    model=load_model_delay()
    print(type(model))

    preds=model.predict(df)

    #probabilidad = model.predict_proba(df)[0]

    print (preds)
