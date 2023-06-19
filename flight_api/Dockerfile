FROM python:3.8.6-buster

COPY main.py main.py
COPY requirements.txt requirements.txt
COPY pipeline_XGBoost_1.pkl pipeline_XGBoost_1.pkl
COPY archivo.txt archivo.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# the --port $PORT is added here so that we can run this on Google Cloud Run
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
