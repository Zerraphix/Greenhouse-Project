from gpiozero import LED
from time import sleep

pump = LED(17) # Definerer PIN

# Forneden er en test af pumpen
while True:
    pump.on()
    sleep(3)
    pump.off()
    sleep(20)

