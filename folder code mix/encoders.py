from machine import Pin, PWM, Timer, UART
import utime, time


#motor 1 depan kiri, 2 depan kanan, 3 belakang kiri, 4 belakang kanan

# Define GPIO pins for each encoder channel
encoder_channels = [(8, 9), (27, 26), (10, 11), (21, 20)]  # Each tuple contains (channel_A, channel_B) pins for an encoder

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
    rpwm.duty_u16(R * 256)
    lpwm.duty_u16(L * 256)
    
#kalau 256 itu 8 bit, kalau 16 bit 65536

"""def drive_motor(motor_index, R, L):
    rpwm, lpwm = motors[motor_index]
    rpwm.duty_u16(R)
    lpwm.duty_u16(L)"""
    
def switch_case(case):
    if case == "8":
        case_maju()
    elif case == "5":
        case_mundur()
    elif case == "4":
        case_kiri()
    elif case == "6":
        case_kanan()
    elif case == "3":
        case_cw()
    elif case == "1":
        case_ccw()
    elif case == "9":
        case_d_kanan_fr()
    elif case == "7":
        case_d_kiri_fr()
    elif case == "]":
        case_d_kanan_bw()
    elif case == "[":
        case_d_kiri_bw()
    elif case == "p":
        case_pivotatas()
    elif case == "o":
        case_pivotkanan()
    else:
        case_default()

"""def case_maju():
    drive_motor(0, 0, 50)
    drive_motor(1, 0, 50)
    drive_motor(2, 0, 50)
    drive_motor(3, 0, 50)
    
def case_mundur():
    drive_motor(0, 50, 0)
    drive_motor(1, 50, 0)
    drive_motor(2, 50, 0)
    drive_motor(3, 50, 0)"""

def case_maju():
    drive_motor(0, 0, 100)
    drive_motor(1, 0, 100)
    drive_motor(2, 0, 100)
    drive_motor(3, 0, 100)
    
def case_mundur():
    drive_motor(0, 150, 0)
    drive_motor(1, 150, 0)
    drive_motor(2, 150, 0)
    drive_motor(3, 150, 0)

"""def case_maju():
    drive_motor(0, 0, 23650)
    drive_motor(1, 0, 23808)
    drive_motor(2, 0, 24320)
    drive_motor(3, 0, 23808)"""

"""def case_maju():
    drive_motor(0, 0, 93)
    drive_motor(1, 0, 93)
    drive_motor(2, 0, 95)
    drive_motor(3, 0, 93)"""
    
def case_mundur():
    drive_motor(0, 98, 0)
    drive_motor(1, 95, 0)
    drive_motor(2, 98, 0)
    drive_motor(3, 95, 0)
    
def case_kiri():
    drive_motor(0, 150, 0)
    drive_motor(1, 0, 150)
    drive_motor(2, 0, 150)
    drive_motor(3, 150, 0)
    
def case_kanan():
    drive_motor(0, 0, 150)
    drive_motor(1, 150, 0)
    drive_motor(2, 150, 0)
    drive_motor(3, 0, 150)
    
def case_cw():
    drive_motor(0, 0, 75)
    drive_motor(1, 75, 0)
    drive_motor(2, 0, 75)
    drive_motor(3, 75, 0)
    
def case_ccw():
    drive_motor(0, 75, 0)
    drive_motor(1, 0, 75)
    drive_motor(2, 75, 0)
    drive_motor(3, 0, 75)

def case_d_kanan_fr():
    drive_motor(0, 0, 100)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, 100)

def case_d_kiri_fr():
    drive_motor(0, 0, 0)
    drive_motor(1, 0, 100)
    drive_motor(2, 0, 100)
    drive_motor(3, 0, 0)
    
def case_d_kanan_bw():
    drive_motor(0, 0, 0)
    drive_motor(1, 100, 0)
    drive_motor(2, 100, 0)
    drive_motor(3, 0, 0)
    
def case_d_kiri_bw():
    drive_motor(0, 100, 0)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 100, 0)
    
def case_pivotkanan():
    drive_motor(0, 0, 150)
    drive_motor(1, 0, 0)
    drive_motor(2, 0, 150)
    drive_motor(3, 0, 0)

def case_pivotatas():
    drive_motor(0, 0, 150)
    drive_motor(1, 150, 0)
    drive_motor(2, 0, 0)
    drive_motor(3, 0, 0)
        
def case_default():
    stop_motors()
    print("Default case")

# Create a Timer object
timer = Timer()

try:
    """# Define UART pins (TX, RX)
    uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # Adjust pins accordingly

    # Wait for UART to initialize
    time.sleep(2)

    # Read data from UART
    received_data = uart.read()
    print("Received Data:", received_data.decode())
    switch_case(received_data.decode())
    uart.deinit()"""
     
    while True:
        user_input = input("enter number: ")
        print("you entered: ", user_input)
        switch_case(user_input)
        for i in range(len(encoder_channels)):
            print("Encoder", i+1, "RPM:", encoder_counts[i])
    
    # Run all motors forward for 5 seconds
    """for motor_index in range(len(motor_pins)):
        drive_motor(motor_index, 0, 15)
    timer.init(mode=Timer.ONE_SHOT, period=3000, callback=stop_and_measure)"""
    
except KeyboardInterrupt:
    stop_motors()
    #uart.deinit()
    pass
