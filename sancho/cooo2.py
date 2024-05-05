from machine import Pin
import utime, time
import select
import sys

machine.freq(200000000)

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Definisikan pin Trig dan Echo untuk setiap sensor beserta orientasi
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

# Konfigurasi pin sensor
for sensor_pin in sensor_pins:
    machine.Pin(sensor_pin['trig'], machine.Pin.OUT)
    machine.Pin(sensor_pin['echo'], machine.Pin.IN)

        
# Fungsi untuk mengukur jarak
def measure_distance(trig_pin, echo_pin, orientation, indices):
    while True:
        for i in indices:
            machine.Pin(trig_pin[i], machine.Pin.OUT).value(0)
            utime.sleep_us(2)
            machine.Pin(trig_pin[i], machine.Pin.OUT).value(1)
            utime.sleep_us(5)
            machine.Pin(trig_pin[i], machine.Pin.OUT).value(0)
            pulse_time = machine.time_pulse_us(machine.Pin(echo_pin[i], machine.Pin.IN), 1, 30000)
            distance_cm = (pulse_time / 2) / 29.1
            print(f"Sensor {orientation[i]}: {distance_cm} cm")
            if 1 < distance_cm < 15:
                print(f"{orientation[i]}, {distance_cm} cm")
            utime.sleep_ms(50)

# Jalankan fungsi pengukuran pada setiap kelompok sensor secara bersamaan
while True:
    if poll_obj.poll(0):
        ch = sys.stdin.read().strip()
        
        if ch == 'maju':
            for sensor in sensor_pins:
                measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'], [1, 2, 0, 3])
                
        if ch == 'mundur':
            for sensor in sensor_pins:
                measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'], [11, 9, 10, 8])
        
        if ch == 'kiri':
            for sensor in sensor_pins:
                measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'], [6, 3, 7, 9])
       
       if ch == 'kanan':
            for sensor in sensor_pins:
                measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'], [4, 2, 5, 8])
    utime.sleep_ms(100)

