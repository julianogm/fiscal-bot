import requests
import lxml.html
import cssselect
from datetime import date
from constant import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_senado(url):
    response = requests.get(url, headers = {'Accept':'application/json'})
    return response.json()

def lista_senadores():
    lista = get_senado(API_SENADO + "senador/lista/atual")['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
    return lista