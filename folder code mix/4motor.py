from machine import Pin, PWM, Timer
import utime

# Define GPIO pins for each encoder channel
encoder_channels = [(8, 9), (26, 27), (10, 11), (20, 21)]  # Each tuple contains (channel_A, channel_B) pins for an encoder

# Define driver pins for motors
motor_pins = [(6, 7), (19, 18), (14, 15), (17, 16)]  # Each tuple contains (RPWM, LPWM) pins for a motor

# Set up the GPIO pins as outputs for motors
motors = []
for rpwm_pin, lpwm_pin in motor_pins:
    rpwm = Pin(rpwm_pin, Pin.OUT)
    lpwm = Pin(lpwm_pin, Pin.OUT)
    motors.append((PWM(rpwm), PWM(lpwm)))

# Set PWM frequency and initial duty cycle for all motors
for rpwm, lpwm in motors:
    rpwm.freq(1000)
    lpwm.freq(1000)
    rpwm.duty_u16(0)
    lpwm.duty_u16(0)

# Setup GPIO pins as inputs with pull-down resistors for encoders
encoders = []
for channel_A, channel_B in encoder_channels:
    encoder_A = Pin(channel_A, Pin.IN, Pin.PULL_DOWN)
    encoder_B = Pin(channel_B, Pin.IN, Pin.PULL_DOWN)
    encoders.append((encoder_A, encoder_B))

# Initialize variables to keep track of encoder states and positions
encoder_positions = [0] * len(encoder_channels)
prev_states = [(encoder_A.value(), encoder_B.value()) for encoder_A, encoder_B in encoders]

def stop_motors():
    for rpwm, lpwm in motors:
        rpwm.duty_u16(0)
        lpwm.duty_u16(0)
    
def encoder(encoder_index):
    global encoder_positions, prev_states
    encoder_A, encoder_B = encoders[encoder_index]
    # Read the current state of the encoder channels
    current_state = (encoder_A.value(), encoder_B.value())
        
    # Check for changes in encoder state
    if current_state != prev_states[encoder_index]:
        # Encoder A has changed, update position
        if current_state[0] != prev_states[encoder_index][0]:
            if current_state[0] == 1 and current_state[1] == 0:
                encoder_positions[encoder_index] -= 1
            elif current_state[0] == 0 and current_state[1] == 1:
                encoder_positions[encoder_index] += 1

    # Update encoder state variables
    prev_states[encoder_index] = current_state

    # Print the current encoder position and encoder values
    print("Encoder {}: Position: {}, Values: A={}, B={}".format(encoder_index, encoder_positions[encoder_index], current_state[0], current_state[1]))

def drive_motor(motor_index, R, L):
    rpwm, lpwm = motors[motor_index]
    rpwm.duty_u16(R * 256)
    lpwm.duty_u16(L * 256)

def stop_and_measure(timer):
    stop_motors()  # Stop all motors
    for i in range(len(encoder_channels)):
        encoder(i)  # Take encoder measurements for all encoders

# Create a Timer object
timer = Timer()

try:
    # Run all motors forward for 5 seconds
    for motor_index in range(len(motor_pins)):
        drive_motor(motor_index, 0, 15)
    timer.init(mode=Timer.ONE_SHOT, period=3000, callback=stop_and_measure)
    

except KeyboardInterrupt:
    stop_motors()
    pass
