import machine
import utime
import micropython

# Definisikan pin Trig dan Echo untuk setiap sensor beserta orientasi
sensor_pins = [
    {'trig': 0, 'echo': 1, 'orientation': 'depan kanan'},
    {'trig': 2, 'echo': 3, 'orientation': 'depan kiri'},
    {'trig': 4, 'echo': 5, 'orientation': 'serong depan kanan'},
    {'trig': 6, 'echo': 7, 'orientation': 'serong depan kiri'},
    {'trig': 8, 'echo': 9, 'orientation': 'samping kanan depan'},
    {'trig': 10, 'echo': 11, 'orientation': 'samping kanan belakang'},
    {'trig': 12, 'echo': 13, 'orientation': 'samping kiri depan'},
    {'trig': 14, 'echo': 15, 'orientation': 'samping kiri belakang'},
    {'trig': 16, 'echo': 17, 'orientation': 'serong belakang kanan'},
    {'trig': 18, 'echo': 19, 'orientation': 'serong belakang kiri'},
    {'trig': 20, 'echo': 21, 'orientation': 'belakang kiri'},
    {'trig': 22, 'echo': 23, 'orientation': 'belakang kanan'},
    # Tambahkan sensor lainnya sesuai kebutuhan
]

# Kelompok sensor yang akan diukur bersamaan
selected_sensor_group1 = [
    sensor_pins[0],  # depan kiri
    sensor_pins[5],  # samping kanan depan
    sensor_pins[12],  # belakang kanan
    sensor_pins[8],  # samping kiri belakang
]

selected_sensor_group2 = [
    sensor_pins[1],  # depan kanan
    sensor_pins[6],  # samping kanan belakang
    sensor_pins[11],  # belakang kiri
    sensor_pins[7],  # samping kiri depan
]

selected_sensor_group3 = [
    sensor_pins[4],  # serong kiri depan
    sensor_pins[3],  # serong kanan depan
    sensor_pins[10],  # serong kiri belakang
    sensor_pins[9],  # serong kanan belakang
]

# Konfigurasi pin sensor
for sensor_pin in sensor_pins:
    machine.Pin(sensor_pin['trig'], machine.Pin.OUT)
    machine.Pin(sensor_pin['echo'], machine.Pin.IN)

# Fungsi untuk mengukur jarak
def measure_distance(trig_pin, echo_pin, orientation):
    # Kirim sinyal ultrasonik
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_ms(10)  # Tahan sinyal selama 10 ms
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)

    # Baca sinyal ultrasonik yang kembali
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1

    print(f"Sensor {orientation}: {distance_cm} cm")

# Fungsi wrapper untuk menggunakan micropython.schedule
def wrapper(sensor):
    measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'])

# Inisialisasi dan jalankan pengukuran untuk kelompok sensor yang diukur bersamaan
for sensor_pin in selected_sensor_group1:
    micropython.schedule(wrapper, sensor_pin)

for sensor_pin in selected_sensor_group2:
    micropython.schedule(wrapper, sensor_pin)

for sensor_pin in selected_sensor_group3:
    micropython.schedule(wrapper, sensor_pin)

# Tunggu sebentar sebelum memulai pengukuran untuk kelompok sensor lainnya
utime.sleep_ms(2000)

# Tunggu agar program utama tidak berakhir
while True:
    pass
