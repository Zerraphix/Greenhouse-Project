import pigpio
import time

PIN = 17 # Vi angiver PIN som styrere GATE på MOSFET 


pi = pigpio.pi()
pi.set_mode(PIN, pigpio.OUTPUT)

def start_pump(): # Definerer funktionen start_pump
    pi.write(PIN, 1) # Vi bruger pi.write med argumenterne PIN(17) og 1 for at aktivere pumpen

def stop_pump(): # Definerer funktionen stop_pump
    pi.write(PIN, 0) # Her slukker vi for pumpen ved at give den en værdi på 0


# Forneden er en test af pumpen
while True:
    pump_on()
    sleep(3)
    pump_off()
    sleep(20)

