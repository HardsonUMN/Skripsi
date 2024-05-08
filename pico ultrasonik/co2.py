from machine import Pin
import utime
import select
import sys

machine.freq(200000000)

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

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

sensor_readings = []

def measure_distance(trig_pin, echo_pin, orientation):
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)
    utime.sleep_us(2)
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_us(5)
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    return (orientation, distance_cm)

def continuous_measurement(direction):
    global sensor_readings
    if direction == '8':
        indices = [0, 1, 2, 3]
    elif direction == '5':
        indices = [8, 9, 10, 11]
    elif direction == 'kiri':
        indices = [1, 3, 5, 7]
    elif direction == 'kanan':
        indices = [0, 2, 4, 6]

    for sensor_index in indices:
        sensor = sensor_pins[sensor_index]
        sensor_reading = measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'])
        sensor_readings.append(sensor_reading)

    if len(sensor_readings) == 4:
        print(sensor_readings)
        sensor_readings = []

while True:
    if poll_obj.poll(0):
        direction = sys.stdin.readline().strip()
        if direction:
            #print("Received direction:", direction)
            if direction in ['8', '5', 'kiri', 'kanan']:
                continuous_measurement(direction)
            else:
                print("Invalid direction entered!")

    utime.sleep_ms(100)