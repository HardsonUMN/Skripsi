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

def drive_motor():
    motor1_RPWM, motor1_LPWM = motors[0]
    motor2_RPWM, motor2_LPWM = motors[1]
    motor3_RPWM, motor3_LPWM = motors[2]
    motor4_RPWM, motor4_LPWM = motors[3]
    
    motor1_RPWM.duty_u16(200 * 256)
    motor1_LPWM.duty_u16(0 * 256)
    motor2_RPWM.duty_u16(200 * 256)
    motor2_LPWM.duty_u16(0 * 256)
    motor3_RPWM.duty_u16(200 * 256)
    motor3_LPWM.duty_u16(0 * 256)
    motor4_RPWM.duty_u16(200 * 256)
    motor4_LPWM.duty_u16(0 * 256)
    
def drive_motorz(motor_index, R, L):
    rpwm, lpwm = motors[motor_index]
    rpwm.duty_u16(R * 256)
    lpwm.duty_u16(L * 256)


def timer_callback(timer):
    stop_motors()
        
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) // (from_high - from_low) + to_low

''''# Usage example:
sensor_value = 512  # Example sensor value
mapped_value = map_value(sensor_value, 0, 1023, 0, 255)  # Map sensor value to range 0-255
print(mapped_value)  # Output the mapped value'''


# Create a Timer object
timer = Timer()

try:
    # Run all motors forward for 5 seconds
    drive_motor()
    timer.init(mode=Timer.ONE_SHOT, period=5000, callback=timer_callback)
    
    # Run the loop indefinitely
    while True:
        for i in range(len(encoder_channels)):
            encoder(i)
        pass

except KeyboardInterrupt:
    stop_motors()
    print("Program terminated by user.")
    pass
