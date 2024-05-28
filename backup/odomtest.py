from machine import Pin, PWM, Timer, UART
import utime, time
import select
import sys
import math

# Constants
WHEEL_CIRCUMFERENCE = 0.193  # in meters
ENCODER_COUNTS_PER_REV = 400
L = 0.325  # distance between left and right wheels in meters
W = 0.249  # distance between front and back wheels in meters

# Derived parameters
WHEEL_RADIUS = WHEEL_CIRCUMFERENCE / (2 * math.pi)
d = (L + W) / 4

# Initial robot position and orientation
x = 0.0
y = 0.0
theta = 0.0

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

# Set interrupt for encoder reading
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

    encoder_a.irq(handler=encoder_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
    encoder_b.irq(handler=encoder_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

def tahan_waktu(waktu):
    myTime = utime.ticks_ms()
    flag = True
    while flag:
        currentTime = utime.ticks_ms()
        if utime.ticks_diff(currentTime, myTime) < waktu:
            flag = True
        else:
            flag = False
    flag = True  # reset flag to true for reuse

def stop_motors():
    for rpwm, lpwm in motors:
        rpwm.duty_u16(0)
        lpwm.duty_u16(0)

def drive_motor(motor_index, R, L):
    rpwm, lpwm = motors[motor_index]
    rpwm.duty_u16(R)
    lpwm.duty_u16(L)
    # kalau 256 itu 8 bit, kalau 16 bit 65535

def switch_case(case):
    global encoder_counts

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
    elif case == "init":
        timer.init(mode=Timer.PERIODIC, period=500, callback=print_enc_callback)
        encoder_counts = [0, 0, 0, 0]  # Reset encoder counts
    elif case == "deinit":
        timer.deinit()
        encoder_counts = [0, 0, 0, 0]  # Reset encoder counts
    else:
        case_default()

def case_maju():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, 0, pwm_2_fwx)
    drive_motor(2, 0, pwm_3_fwx)
    drive_motor(3, 0, pwm_4_fwx)

def case_mundur():
    drive_motor(0, pwm_1_bwx, 0)
    drive_motor(1, pwm_2_bwx, 0)
    drive_motor(2, pwm_3_bwx, 0)
    drive_motor(3, pwm_4_bwx, 0)

def case_kiri():
    drive_motor(0, pwm_1_bwx, 0)
    drive_motor(1, 0, pwm_2_fwx)
    drive_motor(2, 0, pwm_3_fwx)
    drive_motor(3, pwm_4_bwx, 0)

def case_kanan():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, pwm_2_bwx, 0)
    drive_motor(2, pwm_3_bwx, 0)
    drive_motor(3, 0, pwm_4_fwx)

def case_cw():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, pwm_2_bwx, 0)
    drive_motor(2, 0, pwm_3_fwx)
    drive_motor(3, pwm_4_bwx, 0)

def case_ccw():
    drive_motor(0, pwm_1_bwx, 0)
    drive_motor(1, 0, pwm_2_fwx)
    drive_motor(2, pwm_3_bwx, 0)
    drive_motor(3, 0, pwm_4_fwx)

def case_d_kanan_fw():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, pwm_4_fwx)

def case_d_kiri_fw():
    drive_motor(0, 0, 0)
    drive_motor(1, 0, pwm_2_fwx)
    drive_motor(2, 0, pwm_3_fwx)
    drive_motor(3, 0, 0)

def case_d_kanan_bw():
    drive_motor(0, 0, 0)
    drive_motor(1, pwm_2_bwx, 0)
    drive_motor(2, pwm_3_bwx, 0)
    drive_motor(3, 0, 0)

def case_d_kiri_bw():
    drive_motor(0, pwm_1_bwx, 0)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, pwm_4_bwx, 0)

def case_pivotkanan():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, pwm_3_fwx)
    drive_motor(3, 0, 0)

def case_pivotatas():
    drive_motor(0, 0, pwm_1_fwx)
    drive_motor(1, pwm_2_bwx, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, 0)

def case_default():
    stop_motors()
    # print("Default case")

def convert_8bit_to_16bit_pwm(pwm_8bit):
    max_8bit_value = 255.00  # Maximum value for 8-bit PWM
    max_16bit_value = 65535.00  # Maximum value for 16-bit PWM
    
    '''const_pwm_1_fw = 1
    const_pwm_1_bw = 1
    const_pwm_2_fw = 1
    const_pwm_2_bw = 1
    const_pwm_3_fw = 1
    const_pwm_3_bw = 1
    const_pwm_4_fw = 1
    const_pwm_4_bw = 1'''
    
    const_pwm_1_fw = 1
    const_pwm_1_bw = 1
    const_pwm_2_fw = 1.0406
    const_pwm_2_bw = 1.056
    const_pwm_3_fw = 1.004
    const_pwm_3_bw = 1.088
    const_pwm_4_fw = 1.022
    const_pwm_4_bw = 1.01
    
    pwm_16bit = (pwm_8bit / max_8bit_value) * max_16bit_value
    
    pwm_1_fw = pwm_16bit * const_pwm_1_fw
    pwm_1_bw = pwm_16bit * const_pwm_1_bw
    pwm_2_fw = pwm_16bit * const_pwm_2_fw
    pwm_2_bw = pwm_16bit * const_pwm_2_bw
    pwm_3_fw = pwm_16bit * const_pwm_3_fw
    pwm_3_bw = pwm_16bit * const_pwm_3_bw
    pwm_4_fw = pwm_16bit * const_pwm_4_fw
    pwm_4_bw = pwm_16bit * const_pwm_4_bw
    
    pwm_1_fwx = int(round(pwm_1_fw))
    pwm_2_fwx = int(round(pwm_2_fw))
    pwm_3_fwx = int(round(pwm_3_fw))
    pwm_4_fwx = int(round(pwm_4_fw))
    
    pwm_1_bwx = int(round(pwm_1_bw))
    pwm_2_bwx = int(round(pwm_2_bw))
    pwm_3_bwx = int(round(pwm_3_bw))
    pwm_4_bwx = int(round(pwm_4_bw))
    
    return pwm_1_fwx, pwm_2_fwx, pwm_3_fwx, pwm_4_fwx, pwm_1_bwx, pwm_2_bwx, pwm_3_bwx, pwm_4_bwx

pwm_1_fwx, pwm_2_fwx, pwm_3_fwx, pwm_4_fwx, pwm_1_bwx, pwm_2_bwx, pwm_3_bwx, pwm_4_bwx = convert_8bit_to_16bit_pwm(100.0)

def print_enc_callback(timer):
    print(','.join(map(str, encoder_counts)))

timer = Timer()

# Function to calculate wheel displacements
def calculate_wheel_displacements(enc_counts):
    wheel_displacements = [0.0] * 4
    for i in range(4):
        wheel_displacements[i] = (WHEEL_CIRCUMFERENCE * enc_counts[i]) / ENCODER_COUNTS_PER_REV
    return wheel_displacements

# Function to calculate local frame displacements
def calculate_local_displacements(wheel_displacements):
    delta_x_local = (wheel_displacements[0] + wheel_displacements[1] + wheel_displacements[2] + wheel_displacements[3]) / 4
    delta_y_local = (-wheel_displacements[0] + wheel_displacements[1] - wheel_displacements[2] + wheel_displacements[3]) / 4
    delta_theta = (-wheel_displacements[0] + wheel_displacements[1] - wheel_displacements[2] + wheel_displacements[3]) / (4 * d)
    return delta_x_local, delta_y_local, delta_theta

# Function to update global position and orientation
def update_global_position(x, y, theta, delta_x_local, delta_y_local, delta_theta):
    delta_x_global = delta_x_local * math.cos(theta) - delta_y_local * math.sin(theta)
    delta_y_global = delta_x_local * math.sin(theta) + delta_y_local * math.cos(theta)
    
    x += delta_x_global
    y += delta_y_global
    theta += delta_theta
    
    return x, y, theta

def update_robot_position(encoder_counts):
    global x, y, theta
    
    wheel_displacements = calculate_wheel_displacements(encoder_counts)
    delta_x_local, delta_y_local, delta_theta = calculate_local_displacements(wheel_displacements)
    x, y, theta = update_global_position(x, y, theta, delta_x_local, delta_y_local, delta_theta)
    
    return x, y, theta

try:    
    while True:
        if poll_obj.poll(0):
            movement = sys.stdin.readline().strip()
        
            if movement:
                switch_case(movement)
                # Update the robot position with the current encoder counts
                x, y, theta = update_robot_position(encoder_counts)
                # Print the updated position and orientation
                print("Updated Position:")
                print("x =", x)
                print("y =", y)
                print("theta =", theta)
                print("encoder=", encoder_counts)
                #sys.stdin.readline()
                
except KeyboardInterrupt:
    stop_motors()
    pass