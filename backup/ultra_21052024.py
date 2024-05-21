from machine import Timer
import utime

timer = Timer()
machine.freq(200000000)
global sensor_readings
sensor_readings = []
global sensor
sensor = 0  # Initialize sensor count

utime.sleep(5)

# Define pins Trig and Echo for each sensor along with orientation
sensor_pins = [
    {'trig': 29, 'echo': 23, 'orientation': 'depan_kanan'},
    {'trig': 0, 'echo': 1, 'orientation': 'depan_kiri'},
    {'trig': 27, 'echo': 28, 'orientation': 'serong_depan_kanan'},
    {'trig': 2, 'echo': 3, 'orientation': 'serong_depan_kiri'},
    {'trig': 22, 'echo': 26, 'orientation': 'samping_kanan_depan'},
    {'trig': 18, 'echo': 19, 'orientation': 'samping_kanan_belakang'},
    {'trig': 4, 'echo': 5, 'orientation': 'samping_kiri_depan'},
    {'trig': 6, 'echo': 7, 'orientation': 'samping_kiri_belakang'},
    {'trig': 16, 'echo': 17, 'orientation': 'serong_belakang_kanan'},
    {'trig': 8, 'echo': 9, 'orientation': 'serong_belakang_kiri'},
    {'trig': 14, 'echo': 15, 'orientation': 'belakang_kiri'},
    {'trig': 12, 'echo': 13, 'orientation': 'belakang_kanan'},
]

# Configure sensor pins
for sensor_pin in sensor_pins:
    machine.Pin(sensor_pin['trig'], machine.Pin.OUT)
    machine.Pin(sensor_pin['echo'], machine.Pin.IN)

def timer_callback(timer):
    global sensor  # Access the global sensor variable
    for group in sensor_groups:
        for sensor_info in group:
            measure_distance(sensor_info['trig'], sensor_info['echo'], sensor_info['orientation'])
    if sensor == 12:  # Check if all sensors are read
        clean_data = [reading.rstrip("\r\n") for reading in sensor_readings]

        print(", ".join(clean_data))
        
        sensor_readings.clear()  # Reset readings
        sensor = 0  # Reset sensor count

# Function to measure distance
def measure_distance(trig_pin, echo_pin, orientation):
    global sensor  # Access the global sensor variable
    global sensor_readings  # Access the global sensor_readings list
    # Send ultrasonic signal
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_ms(50)
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)

    # Read the returning ultrasonic signal
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    distance_rounded = round(distance_cm)
    
    if distance_rounded == 0:
        distance_rounded = 17
    sensor_readings.append(f"{distance_rounded}")
    sensor += 1  # Increment sensor count

# Mapping sensor groups to measurement function
sensor_groups = [
    [sensor_pins[3], sensor_pins[1], sensor_pins[0], sensor_pins[2]],
    [sensor_pins[4], sensor_pins[5], sensor_pins[8], sensor_pins[11]],
    [sensor_pins[10], sensor_pins[9], sensor_pins[6], sensor_pins[7]],
]

# Initialize timer to trigger the callback function every 5 seconds
timer.init(mode=Timer.PERIODIC, period=300, callback=timer_callback)

# Run the measurement function for each sensor group simultaneously
while True:
    pass


# Function to measure distance
def measure_distance(trig_pin, echo_pin, orientation):
    global sensor  # Access the global sensor variable
    global sensor_readings  # Access the global sensor_readings list
    # Send ultrasonic signal
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_ms(50)
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)

    # Read the returning ultrasonic signal
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    distance_rounded = round(distance_cm)
    
    if 1 < distance_rounded < 15:
        #sensor_readings.append(f"{orientation}, {distance_cm}")
        sensor_readings.append(f"{distance_rounded}")
    else:
        sensor_readings.append("0")
    sensor += 1  # Increment sensor count

# Mapping sensor groups to measurement function
sensor_groups = [
    [sensor_pins[3], sensor_pins[1], sensor_pins[0], sensor_pins[2]],
    [sensor_pins[4], sensor_pins[5], sensor_pins[8], sensor_pins[11]],
    [sensor_pins[10], sensor_pins[9], sensor_pins[6], sensor_pins[7]],
]

# Initialize timer to trigger the callback function every 5 seconds
#timer.init(mode=Timer.PERIODIC, period=500, callback=timer_callback)

# Run the measurement function for each sensor group simultaneously
while True:
    pass
