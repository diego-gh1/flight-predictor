import requests
url="http://127.0.0.1:8000/predict"
params = {
    'aeropuerto_origen': 'ABE',
    'aeropuerto_destino': 'CRP',
    'dia': 2,
    'mes':3,
    'dia_de_semana': 2,
    'horario': 832,
    'aerolinea':'United Air Lines Inc.',
    'scheduled_time': 832,
    'scheduled_arrival':832
}
response = requests.get(url, params=params)
