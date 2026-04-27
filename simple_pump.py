from gpiozero import LED
from time import sleep

pump = LED(17) # 11 PB2

def pump_on():
    pump.on()

def pump_off():
    pump.off()
  
while True:
  pump_on()
  sleep(5)
  pump_off()
  sleep(10)
