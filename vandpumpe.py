from gpiozero import LED
from time import sleep

pump = LED(17) # Definerer PIN

def pump_on():
    pump.on()

def pump_off():
    pump.off()


# Forneden er en test af pumpen
while True:
    pump_on()
    sleep(3)
    pump_off()
    sleep(20)

