from ast import Return
from re import T
from traceback import print_tb
from turtle import pu
from geopy.distance import geodesic
from unittest import result
from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import pandas as pd

e = urllib.request.urlopen("http://www.sismologia.cl/ultimos_sismos.html").read()
soup = BeautifulSoup(e, 'html.parser')

# Obt    enemos la tabla

tabla_sismos = soup.find_all('table')[0]

# Obtenemos todas las filas
rows = tabla_sismos.find_all("tr")

output_rows = []
for row in rows:
        # obtenemos todas las columns
    cells = row.find_all("td")
    output_row = []
    if len(cells) > 0:
        for cell in cells:
            output_row.append(cell.text)
            output_rows.append(output_row)

dataset = pd.DataFrame(output_rows)

dataset.columns = [
        "Fecha Local",
        "Fecha UTC",
        "Latitud",
        "Longitud",
        "Profundidad [Km]",
        "Magnitud",
        "Referencia Geográfica",
    ]
dataset[["Latitud", "Longitud"]] = dataset[["Latitud", "Longitud"]].apply(pd.to_numeric)
dataset_filter = dataset[
            (-27.100 <= dataset["Latitud"])
            & (dataset["Latitud"] <= -21.680)
            & (-72.150 <= dataset["Longitud"])
            & (dataset["Longitud"] <= -66.180)
            ]

tranque = (-24.39,-69.14)

latitud1 = dataset_filter['Latitud'].values[0]
longitud1 = dataset_filter['Longitud'].values[0]
profundidad = dataset_filter['Profundidad [Km]'].values[0]
magnitud = dataset_filter['Magnitud'].values[0]
magnitud2 = magnitud.split(' ')
magnitud3 = float(magnitud2[0])
magnitud4 = magnitud2[1]
delhi = (latitud1, longitud1)
distancia = int(round((geodesic(tranque, delhi).km)))

print (magnitud3)
print (distancia)


def bot_send_text(bot_message):
    
    bot_token = '5242107370:AAGiBaDihZbdphDhybneHT0pU_4bJGDVWkk'
    bot_chatID = '-713984361'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def sismo_scraping():  
    string="A ocurrido un sismo en las cercanías del Tranque Laguna Seca" "\n""\n" "*Datos del sismo:*" "\n" #titulo con salto de linea
    
    for column in dataset_filter.head(1).columns:
        string += column +  " : " + str(dataset_filter[column].values[0]) + "\n"
          
    return string

def distancias():       
    string2="El sismo se registro a una *DISTANCIA* de  "  f'{str(distancia)}' "Km del Tranque Laguna seca, y una *MAGNITUD* de " f'{str(magnitud3)}' "" f'{str(magnitud4)}'
    return string2

# def amarillo():
#     msg1 = 5
#     dist = 15
#     # msg3 = "NO Aplica para activar protocolo"
#     if msg1 <= 7 or dist <= 100:
#         msg = "Alerta *MORADA*"
#         print("Alerta *MORADA*")
#     elif msg1 <= 7 or dist <= 120:
#         msg = "Alerta *ROJA*"
#         print("Alerta *ROJA*")
#     elif msg1 >=4 or dist <= 10:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <=5 or dist <= 50:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <=6 or dist <= 120:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <= 3.9:
#         msg = "Alerta *AMARILLA*"
#         print("Alerta *AMARILLA*")
#     else:
#         msg = "NO APLICA PARA ACTIVAR PROTOCOLO"
#         print ("NO APLICA PARA ACTIVAR PROTOCOLO")
#     return msg


        
def main():
    ultimo_sismo = None
    # text3 = f'{amarillo()}'
    while True:
        text = f'{sismo_scraping()}'
        text2 = f'{distancias()}'
        if text != ultimo_sismo:
            bot_send_text(text)
            ultimo_sismo = text
            bot_send_text(text2)
            # bot_send_text(text3)
        time.sleep(60) 

if __name__ == '__main__':

    main()
