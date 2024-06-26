from machine import Pin, PWM, Timer
import utime

# Define GPIO pins for encoder channels
encoder_channel_A = 8
encoder_channel_B = 9

# Define driver pin
RPWM = 6
LPWM = 7

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

# Setup GPIO pins as inputs with pull-down resistors
encoder_A = Pin(encoder_channel_A, Pin.IN, Pin.PULL_DOWN)
encoder_B = Pin(encoder_channel_B, Pin.IN, Pin.PULL_DOWN)

# Initialize variables to keep track of encoder state
encoder_position = 0
prev_state_A = encoder_A.value()
prev_state_B = encoder_B.value()

def stop_motors():
    RPWM_pwm.duty_u16(0)
    LPWM_pwm.duty_u16(0)
    
def encoder():
    global encoder_position, prev_state_A, prev_state_B
    # Read the current state of the encoder channels
    current_state_A = encoder_A.value()
    current_state_B = encoder_B.value()
        
    # Check for changes in encoder state
    if current_state_A != prev_state_A or current_state_B != prev_state_B:
        # Encoder A has changed, update position
        if current_state_A == 1 and prev_state_A == 0 and current_state_A > current_state_B:
            encoder_position -= 1
                
        elif current_state_B == 1 and prev_state_B == 0 and current_state_A < current_state_B:
            encoder_position += 1

    # Update encoder state variables
    prev_state_A = current_state_A
    prev_state_B = current_state_B

    # Print the current encoder position and encoder values
    print("Encoder Position: {}, Encoder Values: A={}, B={}".format(encoder_position, current_state_A, current_state_B))

    
def drive_motor(R,L):
    RPWM_pwm.duty_u16(R*256)
    LPWM_pwm.duty_u16(L*256)

def callbacks(timer):
    encoder()

encoder_timer = Timer()
try:
    encoder()
    # Add a small delay to control the speed of reading
    encoder_timer.init(period=10, mode=Timer.PERIODIC, callback=callbacks)

except KeyboardInterrupt:
    stop_motors()
    pass
