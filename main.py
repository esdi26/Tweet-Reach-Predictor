from fastapi import FastAPI
from api.app import app as fastapi_app  # api klasöründeki app.py'den app nesnesini import et

app = fastapi_app
