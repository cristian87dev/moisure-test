import RPi.GPIO as GPIO    #Importamos la librería GPIO
import time                #Importamos time (time.sleep)
import datetime
import paho.mqtt.client as mqtt
from gpiozero import Buzzer

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message received " , msg)
    print("message topic=", message.topic)
    if message.topic == "/casa/living/buzzer":
        if msg == "ON":
            buzzer.on()
        elif msg == "OFF":
            buzzer.off()

GPIO.setmode(GPIO.BCM)     #Ponemos la placa en modo BCM
GPIO_TRIGGER = 25          #Usamos el pin GPIO 25 como TRIGGER
GPIO_ECHO    = 7           #Usamos el pin GPIO 7 como ECHO
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER,False)    #Ponemos el pin 25 como LOW

buzzer = Buzzer(17)

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.username_pw_set("yurrparf", "15B5GARLiVhk")
client.connect("192.168.0.53", 1883, 60)
client.loop_start()
client.subscribe("/casa/living/buzzer")
 
try:
    while True:     #Iniciamos un loop infinito
        #buzzer.on()
        #time.sleep(1)
        #buzzer.off()
        #time.sleep(1)
        GPIO.output(GPIO_TRIGGER,True)   #Enviamos un pulso de ultrasonidos
        time.sleep(0.00001)              #Una pequeñña pausa
        GPIO.output(GPIO_TRIGGER,False)  #Apagamos el pulso
        start = time.time()              #Guarda el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==0:  #Mientras el sensor no reciba señal...
            start = time.time()          #Mantenemos el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==1:  #Si el sensor recibe señal...
            stop = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
        elapsed = stop-start             #Obtenemos el tiempo transcurrido entre envío y recepción
        distance = (elapsed * 34300)/2   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
        print(distance)                   #Devolvemos la distancia (en centímetros) por pantalla
        client.publish("/casa/living/temperature", distance)
        print(datetime.datetime.now())
        time.sleep(1)                    #Pequeña pausa para no saturar el procesador de la Raspberry
except KeyboardInterrupt:                #Si el usuario pulsa CONTROL+C...
    print("quit")                        #Avisamos del cierre al usuario
    client.loop_stop()
    GPIO.cleanup()