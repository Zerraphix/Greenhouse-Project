import pigpio
import time
import smbus # Anvendes kun ved brug af eksemplet længer nede efter funktionerne.

PIN = 17 # Vi angiver PIN som styrere GATE på MOSFET 

# Initialiserer pigpio
pi = pigpio.pi()
pi.set_mode(PIN, pigpio.OUTPUT)

def start_pump(): # Definerer funktionen start_pump
    pi.write(PIN, 1) # Vi bruger pi.write med argumenterne PIN(17) og 1 for at aktivere pumpen

def stop_pump(): # Definerer funktionen stop_pump
    pi.write(PIN, 0) # Her slukker vi for pumpen ved at give den en værdi på 0

# Et eksempel på hvordan main loop kan se ud:
"""
adc = MCP3021()
pump_aktiv = False  # Holder styr på state

try:
    while True:
        humidity = adc.read_percent()
        print(f"Fugtighed: {humidity}%")

        if humidity < 10 and not pump_aktiv:
            print("Starter pumpe")
            start_pump()
            pump_aktiv = True

        elif humidity > 60 and pump_aktiv:
            print("Stopper pumpe")
            stop_pump()
            pump_aktiv = False

        time.sleep(5)
"""
