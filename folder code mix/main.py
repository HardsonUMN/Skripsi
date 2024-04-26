from machine import Pin, PWM, Timer
import utime
from rotary_irq_rp2 import RotaryIRQ
vb
rotary = RotaryIRQ(10, 11)

# Define driver pin
RPWM = 14
LPWM = 15

# Set up the GPIO pins as outputs
RPWM_pin = Pin(RPWM, Pin.OUT)
LPWM_pin = Pin(LPWM, Pin.OUT)

# Create PWM objects for RPWM and LPWM
RPWM_pwm = PWM(RPWM_pin)
LPWM_pwm = PWM(LPWM_pin)
RPWM_pwm.freq(1000)
LPWM_pwm.freq(1000)
RPWM_pwm.duty_u16(0)
LPWM_pwm.duty_u16(0)

# Initialize variables to keep track of encoder state
def stop_motors():
    RPWM_pwm.duty_u16(0)
    LPWM_pwm.duty_u16(0)
        
def drive_motor(R,L):
    RPWM_pwm.duty_u16(R*256)
    LPWM_pwm.duty_u16(L*256)

def callbacks(timer):
    stop_motors()
    print("end")
    
current_val = 0  # Track the last known value of the encoder
drive_motor(100, 0)
while True:
    new_val = rotary.value()  # What is the encoder value right now?
    
    if current_val != new_val:  # The encoder value has changed!
        print('Encoder value:', new_val)  # Do something with the new value
        
        current_val = new_val  # Track this change as the last know value
