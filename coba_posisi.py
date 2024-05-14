from machine import Pin, PWM, Timer, UART
import utime, time
import select
import sys
import math

machine.freq(200000000)
#motor 1 depan kiri, 2 depan kanan, 3 belakang kiri, 4 belakang kanan

# Define GPIO pins for each encoder channel
encoder_channels = [(8, 9), (27, 26), (10, 11), (21, 20)]  # Each tuple contains (channel_A, channel_B) pins for an encoder

# Define driver pins for motors
motor_pins = [(6, 7), (19, 18), (14, 15), (17, 16)]  # Each tuple contains (RPWM, LPWM) pins for a motor

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Set up the GPIO pins as outputs for motors
motors = []
for rpwm_pin, lpwm_pin in motor_pins:
    rpwm = Pin(rpwm_pin, Pin.OUT)
    lpwm = Pin(lpwm_pin, Pin.OUT)
    motors.append((PWM(rpwm), PWM(lpwm)))

# Set PWM frequency and initial duty cycle for all motors
for rpwm, lpwm in motors:
    rpwm.freq(10000)
    lpwm.freq(10000)
    rpwm.duty_u16(0)
    lpwm.duty_u16(0)

encoder_counts = [0, 0, 0, 0]

# Setup GPIO pins as inputs with pull-down resistors for encoders
encoders = []
encoder_handlers = []

def handle_encoder(encoder_index):
    global encoder_counts

    encoder_a, encoder_b = encoders[encoder_index]
    current_encoder_state = (encoder_a.value() << 1) | encoder_b.value()
    if current_encoder_state == 0b00 and previous_encoder_states[encoder_index] == 0b01:
        encoder_counts[encoder_index] -= 1
    elif current_encoder_state == 0b00 and previous_encoder_states[encoder_index] == 0b10:
        encoder_counts[encoder_index] += 1
    previous_encoder_states[encoder_index] = current_encoder_state

# Set interrupt untuk pembacaan encoder
previous_encoder_states = [0, 0, 0, 0]

for i in range(len(encoder_channels)):
    channel_A, channel_B = encoder_channels[i]
    encoder_a = Pin(channel_A, Pin.IN, Pin.PULL_DOWN)
    encoder_b = Pin(channel_B, Pin.IN, Pin.PULL_DOWN)
    encoders.append((encoder_a, encoder_b))
    
    def create_handler(index):
        def handler(pin):
            handle_encoder(index)
        return handler

    encoder_handler = create_handler(i)
    encoder_handlers.append(encoder_handler)

    encoder_a.irq(handler=encoder_handler, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)
    encoder_b.irq(handler=encoder_handler, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)

def stop_motors():
    for rpwm, lpwm in motors:
        rpwm.duty_u16(0)
        lpwm.duty_u16(0)
    
def drive_motor(motor_index, R, L):
    rpwm, lpwm = motors[motor_index]
    rpwm.duty_u16(R)
    lpwm.duty_u16(L)

def switch_case(case):
    if case == "maju":
        case_maju()
    elif case == "mundur":
        case_mundur()
    elif case == "kiri":
        case_kiri()
    elif case == "kanan":
        case_kanan()
    elif case == "cw":
        case_cw()
    elif case == "ccw":
        case_ccw()
    elif case == "d_kanan_fw":
        case_d_kanan_fw()
    elif case == "d_kiri_fw":
        case_d_kiri_fw()
    elif case == "d_kanan_bw":
        case_d_kanan_bw()
    elif case == "d_kiri_bw":
        case_d_kiri_bw()
    elif case == "pivotatas":
        case_pivotatas()
    elif case == "pivotkanan":
        case_pivotkanan()
    else:
        case_default()

def case_maju():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, 0, pwm_front_fw)
    drive_motor(2, 0, pwm_send_fw)
    drive_motor(3, 0, pwm_back_fw)
    
def case_mundur():
    drive_motor(0, pwm_send_bw, 0)
    drive_motor(1, pwm_front_bw, 0)
    drive_motor(2, pwm_send_bw, 0)
    drive_motor(3, pwm_back_bw, 0)

def case_kiri():
    drive_motor(0, pwm_send_bw, 0)
    drive_motor(1, 0, pwm_front_fw)
    drive_motor(2, 0, pwm_send_fw)
    drive_motor(3, pwm_back_bw, 0)
    
def case_kanan():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, pwm_front_bw, 0)
    drive_motor(2, pwm_send_bw, 0)
    drive_motor(3, 0, pwm_back_fw)
    
def case_cw():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, pwm_front_bw, 0)
    drive_motor(2, 0, pwm_send_fw)
    drive_motor(3, pwm_back_bw, 0)
    
def case_ccw():
    drive_motor(0, pwm_send_bw, 0)
    drive_motor(1, 0, pwm_front_fw)
    drive_motor(2, pwm_send_bw, 0)
    drive_motor(3, 0, pwm_back_fw)

def case_d_kanan_fw():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, pwm_send_fw)

def case_d_kiri_fw():
    drive_motor(0, 0, 0)
    drive_motor(1, 0, pwm_send_fw)
    drive_motor(2, 0, pwm_send_fw)
    drive_motor(3, 0, 0)
    
def case_d_kanan_bw():
    drive_motor(0, 0, 0)
    drive_motor(1, pwm_send_bw, 0)
    drive_motor(2, pwm_send_bw, 0)
    drive_motor(3, 0, 0)
    
def case_d_kiri_bw():
    drive_motor(0, pwm_send_bw, 0)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, pwm_send_bw, 0)
    
def case_pivotkanan():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, pwm_send_fw)
    drive_motor(3, 0, 0)

def case_pivotatas():
    drive_motor(0, 0, pwm_send_fw)
    drive_motor(1, pwm_send_bw, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, 0)
        
def case_default():
    stop_motors()
    print("Default case")
    
def convert_8bit_to_16bit_pwm(pwm_8bit):
    max_8bit_value = 255.00  # Maximum value for 8-bit PWM
    max_16bit_value = 65535.00  # Maximum value for 16-bit PWM
    
    const_front_fw = 1
    const_back_fw = 1
    const_front_bw = 1.1
    const_back_bw = 1
    
    # Scale the 8-bit PWM value to fit within the range of the 16-bit PWM
    pwm_16bit = (pwm_8bit / max_8bit_value) * max_16bit_value
    
    pwm_front_fw = pwm_16bit * const_front_fw 
    pwm_back_fw = pwm_16bit * const_back_fw
    pwm_front_bw = pwm_16bit * const_front_bw
    pwm_back_bw = pwm_16bit * const_back_bw

    # Round to the nearest integer
    pwm_send_fw = int(round(pwm_16bit))
    pwm_send_bw = int(round(pwm_16bit))
    
    pwm_front_fwx = int(round(pwm_front_fw)) 
    pwm_back_fwx = int(round(pwm_back_fw))
    pwm_front_bwx = int(round(pwm_front_bw))
    pwm_back_bwx = int(round(pwm_back_bw))
    
    if pwm_front_bw <= 13000:
        pwm_front_bw = pwm_front_bw + 3000
    if pwm_back_bw <= 13000:
        pwm_back_bw = pwm_front_bw + 3000
    if pwm_send_bw <= 13000:
        pwm_send_bw = pwm_send_bw + 3000
        
    return pwm_send_fw, pwm_send_bw, pwm_front_fwx, pwm_back_fwx, pwm_front_bwx, pwm_back_bwx

# Constants for odometry
WHEEL_DIAMETER = 0.1  # Example wheel diameter in meters
ENCODER_COUNTS_PER_REV = 3786  # Example encoder counts per revolution
WHEEL_BASE = 0.3  # Distance between the left and right wheels

# Calculate distance per encoder count
distance_per_count = (math.pi * WHEEL_DIAMETER) / ENCODER_COUNTS_PER_REV

# Robot position and orientation
x_pos = 0.0
y_pos = 0.0
theta = 0.0

# Update robot position based on encoder counts
def update_position():
    global x_pos, y_pos, theta
    global encoder_counts
    global previous_encoder_counts

    # Calculate the distance each wheel has traveled
    distances = [(encoder_counts[i] - previous_encoder_counts[i]) * distance_per_count for i in range(4)]

    # Average the distances for each side of the robot
    distance_left = (distances[0] + distances[2]) / 2.0
    distance_right = (distances[1] + distances[3]) / 2.0

    # Calculate the change in position and orientation
    delta_theta = (distance_right - distance_left) / WHEEL_BASE
    delta_x = (distance_left + distance_right) / 2.0 * math.cos(theta + delta_theta / 2.0)
    delta_y = (distance_left + distance_right) / 2.0 * math.sin(theta + delta_theta / 2.0)

    # Update the robot's position and orientation
    x_pos += delta_x
    y_pos += delta_y
    theta += delta_theta

    # Normalize theta to be within -pi to pi
    theta = (theta + math.pi) % (2 * math.pi) - math.pi

# Initialize previous encoder counts for position calculation
previous_encoder_counts = [0, 0, 0, 0]

# Initialize motor PWM values
pwm_send_fw, pwm_send_bw, pwm_front_fw, pwm_back_fw, pwm_front_bw, pwm_back_bw = convert_8bit_to_16bit_pwm(100.0)

try:
    while True:
        if poll_obj.poll(0):
            movement = sys.stdin.readline().strip()

            if movement:
                switch_case(movement)
                sys.stdin.readline()

                # Reset encoder counts to 0
                encoder_counts = [0, 0, 0, 0]

        # Update the robot's position
        update_position()

        # Print the robot's position and orientation
        print("Position: ({:.2f}, {:.2f}) Theta: {:.2f}".format(x_pos, y_pos, theta))

        # Check if any encoder has reached its target count and stop the corresponding motor
        for i in range(len(encoder_channels)):
            if encoder_counts[i] >= 37860:  # 3786 counts per rotation * 10 rotations
                drive_motor(i, 0, 0)

except KeyboardInterrupt:
    stop_motors()
    pass
