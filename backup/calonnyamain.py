from machine import Pin, PWM, Timer, UART
import utime, time
import select
import sys

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

    if case == "8":
        case_maju()
    elif case == "2":
        case_mundur()
    elif case == "4":
        case_kiri()
    elif case == "6":
        case_kanan()
    elif case == "p":
        case_cw()
    elif case == "o":
        case_ccw()
    elif case == "9":
        case_d_kanan_fw()
    elif case == "7":
        case_d_kiri_fw()
    elif case == "3":
        case_d_kanan_bw()
    elif case == "1":
        case_d_kiri_bw()
    elif case == "l":
        case_pivotatas()
    elif case == "k":
        case_pivotkanan()
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
    
    const_pwm_1_fw = 1
    const_pwm_1_bw = 1
    #const_pwm_2_fw = 1.006243
    const_pwm_2_fw = 1.00561
    const_pwm_2_bw = 1
    const_pwm_3_fw = 1
    const_pwm_3_bw = 1
    #const_pwm_4_fw = 1.005489
    const_pwm_4_fw = 1.004825
    const_pwm_4_bw = 1
    
    '''const_pwm_1_fw = 1
    const_pwm_1_bw = 1
    const_pwm_2_fw = 1.0406
    const_pwm_2_bw = 1.056
    const_pwm_3_fw = 1.004
    const_pwm_3_bw = 1.088
    const_pwm_4_fw = 1.022
    const_pwm_4_bw = 1.01'''
    
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

pwm_1_fwx, pwm_2_fwx, pwm_3_fwx, pwm_4_fwx, pwm_1_bwx, pwm_2_bwx, pwm_3_bwx, pwm_4_bwx = convert_8bit_to_16bit_pwm(100)


timer = Timer()
try:
    while True:
        user_input = input("enter number: ")
        print("you enter: ", user_input)
        switch_case(user_input)
        
    """while True:
        if poll_obj.poll(0):
            movement = sys.stdin.readline().strip()
        
            if movement:
                switch_case(movement)
                sys.stdin.readline()"""
except KeyboardInterrupt:
    stop_motors()
    pass
