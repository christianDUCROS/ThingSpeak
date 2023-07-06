'''
Exploitation de thingSpeak 
Envoi de 3 données de température simulées avec random
Vous devez modifier api_key
Envoi toutes les minutes
'''

import requests 
import random #simulation de capteur
import time

while True : 
    start = time.time()#mesure intervalle entre 2 envois 

    #**********simulation capteurs **************
    temp_salon= random.randint(18,25)
    temp_ch1= random.randint(18,25)
    temp_ch2= random.randint(18,25)
    #********************************************

    #**********envoi vers API *******************
    url_T_salon = 'https://api.thingspeak.com/update?api_key=94E2Q0HA89TJVJH4&field1={}'.format(temp_salon)
    url_T_ch1 = 'https://api.thingspeak.com/update?api_key=94E2Q0HA89TJVJH4&field2={}'.format(temp_ch1)
    url_T_ch2 = 'https://api.thingspeak.com/update?api_key=94E2Q0HA89TJVJH4&field3={}'.format(temp_ch2)

    print(url_T_salon)
    print(url_T_ch1)
    print(url_T_ch2)

    requests.get(url_T_salon)
    time.sleep(15)
    requests.get(url_T_ch1)
    time.sleep(15)
    requests.get(url_T_ch2)
    time.sleep(15)
 
    #**********tempo intervalle 1min *******************
    while (time.time()- start) < 60 :
        time.sleep(1)
