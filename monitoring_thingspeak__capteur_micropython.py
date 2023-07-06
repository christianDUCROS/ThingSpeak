# ************************************** 
from machine import Pin
import machine 
import network  
import comptes_wifi 
import urequests
import time
import onewire
import ds18x20
# **************************************

# ************Affichage Erreur **********
Led_builtin = Pin('LED',Pin.OUT)# RP2 W ou 25 pour RP2
Led_builtin.off()
 
def affichage_erreur(code) : # 1 wifi, 2 capteur 3 http     
    if code == 1 : 
        while True:
            Led_builtin.toggle() #changement état
            time.sleep_ms(500)
    if code == 2 : 
        while True:
            Led_builtin.toggle() #changement état
            time.sleep_ms(50)
    if code == 3 : 
        while True:
            Led_builtin.on() #ON 
            time.sleep(10)    
# **************************************


# **********connexion wifi**************
ssid = comptes_wifi.ssid
password = comptes_wifi.password

def connexion_wifi_STA(pssid,ppassword) : # Connexion wifi mode STATION
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(pssid, ppassword)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        affichage_erreur(1)
        #raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        Led_builtin.on()
        time.sleep(3)
        Led_builtin.off()
# **************************************

# **********mesure capteur DS18x20******
ow = onewire.OneWire(Pin(15))
ds = ds18x20.DS18X20(ow)
adresse_capteur1 = bytearray(b'(\xfefffra\x81\x17\x04*')

def mesure_capteur(adresse_capteur1) :
    try :
        ds.convert_temp()
        time.sleep_ms(750)
        temperature =ds.read_temp(adresse_capteur1)
        temperature = int(temperature)
        print('La température actuelle est de : ',temperature)
        return temperature
    except :
        affichage_erreur(2)
# **************************************

# *********Connexion ThingSpeak*****************************
champ = 'field1' #salon
def send_temperature_ThingSpeak(temperature) :
    data_capteur = str(temperature)
    try : 
        print('https://api.thingspeak.com/update?api_key=94E2Q0HA89TJVJH4&{}={}'.format(champ,data_capteur))
        request = urequests.get('https://api.thingspeak.com/update?api_key=94E2Q0HA89TJVJH4&{}={}'.format(champ,data_capteur))
        request.close()
        print('données envoyées')
    except :
        print("Pb d'envoi")
        affichage_erreur(3)
# **************************************


# *************main*************************
while True : 
    print("lancement de l'application")
    print("Connexion wifi")
    connexion_wifi_STA(ssid,password)
    print("Mesure capteur")
    temperature = mesure_capteur()
    print(temperature)
    print("Envoi donnée ThingSpeak")
    send_temperature_ThingSpeak(temperature)
    print('mise en sommeil légé') #RP2 ne permet pas le sommeil profond
    time.sleep(3) #temps d'affichage avant mise en sommeil
    machine.lightsleep(3600000) #1 heure
# ****************************************



        
