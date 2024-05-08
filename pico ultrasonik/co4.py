from machine import Timer
import utime

timer = Timer()
machine.freq(200000000)
global sensor_readings
sensor_readings = []
global sensor
sensor = 0  # Initialize sensor count

# Define pins Trig and Echo for each sensor along with orientation
sensor_pins = [
    {'trig': 29, 'echo': 23, 'orientation': 'depan kanan'},
    {'trig': 0, 'echo': 1, 'orientation': 'depan kiri'},
    {'trig': 27, 'echo': 28, 'orientation': 'serong depan kanan'},
    {'trig': 2, 'echo': 3, 'orientation': 'serong depan kiri'},
    {'trig': 22, 'echo': 26, 'orientation': 'samping kanan depan'},
    {'trig': 18, 'echo': 19, 'orientation': 'samping kanan belakang'},
    {'trig': 4, 'echo': 5, 'orientation': 'samping kiri depan'},
    {'trig': 6, 'echo': 7, 'orientation': 'samping kiri belakang'},
    {'trig': 16, 'echo': 17, 'orientation': 'serong belakang kanan'},
    {'trig': 8, 'echo': 9, 'orientation': 'serong belakang kiri'},
    {'trig': 14, 'echo': 15, 'orientation': 'belakang kiri'},
    {'trig': 12, 'echo': 13, 'orientation': 'belakang kanan'},
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
        print(", ".join(sensor_readings))
        sensor_readings.clear()  # Reset readings
        sensor = 0  # Reset sensor count

# Function to measure distance
def measure_distance(trig_pin, echo_pin, orientation):
    global sensor  # Access the global sensor variable
    global sensor_readings  # Access the global sensor_readings list
    # Send ultrasonic signal
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_ms(10)
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)

    # Read the returning ultrasonic signal
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    
    if 1 < distance_cm < 15:
        sensor_readings.append(f"{orientation}, {distance_cm}")
    
    sensor += 1  # Increment sensor count

# Mapping sensor groups to measurement function
sensor_groups = [
    [sensor_pins[1], sensor_pins[4], sensor_pins[7], sensor_pins[11]],
    [sensor_pins[0], sensor_pins[5], sensor_pins[6], sensor_pins[10]],
    [sensor_pins[3], sensor_pins[2], sensor_pins[8], sensor_pins[9]],
]

# Initialize timer to trigger the callback function every 5 seconds
timer.init(mode=Timer.PERIODIC, period=1000, callback=timer_callback)

# Run the measurement function for each sensor group simultaneously
while True:
    pass
