from machine import Timer
import utime

timer = Timer()
machine.freq(200000000)

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
    # Tambahkan sensor lainnya sesuai kebutuhan
]

# Konfigurasi pin sensor
for sensor_pin in sensor_pins:
    machine.Pin(sensor_pin['trig'], machine.Pin.OUT)
    machine.Pin(sensor_pin['echo'], machine.Pin.IN)

def timer_callback(timer):
    for group in sensor_groups:
        for sensor in group:
            measure_distance(sensor['trig'], sensor['echo'], sensor['orientation'])
        print("\n")
        
# Fungsi untuk mengukur jarak
def measure_distance(trig_pin, echo_pin, orientation):
    # Kirim sinyal ultrasonik
    machine.Pin(trig_pin, machine.Pin.OUT).value(1)
    utime.sleep_ms(10) 
    #timer.init(mode=Timer.PERIODIC, freq=10, callback=measure_distance)
    machine.Pin(trig_pin, machine.Pin.OUT).value(0)

    # Baca sinyal ultrasonik yang kembali
    pulse_time = machine.time_pulse_us(machine.Pin(echo_pin, machine.Pin.IN), 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1

    print(f"Sensor {orientation}: {distance_cm} cm")
    
    if orientation == 'depan kiri':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
            
            
            global distance_kiri
            distance_kiri = distance_cm
            print(f"{distance_kiri}askljkdjasjsadjlkajslk")
            
            
        else:
            pass

    elif orientation == 'samping kanan depan':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
    
    elif orientation == 'samping kiri belakang':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'belakang kanan':
        if 1< distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'depan kanan':
        if 1< distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
            
            
            global distance_kanan
            distance_kanan = distance_cm
            aas = [distance_kanan, distance_kiri]
            print(f"kanan {aas[0]}")
            if distance_kanan > distance_kiri :
                print(f"KANANNNNN")
                
                
        else:
            pass
        
    elif orientation == 'samping kanan belakang':
        if 1< distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'samping kiri depan':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'belakang kiri':
        if 1< distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
    
    elif orientation == 'serong depan kiri':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'serong depan kanan':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
    
    elif orientation == 'serong belakang kanan':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
        
    elif orientation == 'serong belakang kiri':
        if 1 < distance_cm < 15:
            print(f"{orientation}, {distance_cm}")
        else:
            pass
    

# Pemetaan kelompok sensor ke fungsi pengukuran
sensor_groups = [
    [sensor_pins[1], sensor_pins[4], sensor_pins[7], sensor_pins[11]],
    [sensor_pins[0], sensor_pins[5], sensor_pins[6], sensor_pins[10]],
    [sensor_pins[3], sensor_pins[2], sensor_pins[8], sensor_pins[9]],
]

# Initialize timer to trigger the callback function every 5 seconds
timer.init(mode=Timer.PERIODIC, period=1000, callback=timer_callback)

# Jalankan fungsi pengukuran pada setiap kelompok sensor secara bersamaan
while True:
    pass

