import pigpio
import time

PIN = 17 # Vi angiver PIN som styrere GATE på MOSFET 

# Initialiser pigpio
pi = pigpio.pi()
pi.set_mode(PIN, pigpio.OUTPUT)

def start_pump(duration): # Her defineres funktionen start_pump
    pi.write(PIN, 1)  # tænder pumpe
    time.sleep(duration) # Angiver længden på hvor længe den skal være tændt
    pi.write(PIN, 0)  # slukker pumpe

def stop_pump(): # Her derfinere vi funktionen stop_pump
    pi.write(PIN, 0) # Vi sætter pin output til low (0), som slukker pumpen

