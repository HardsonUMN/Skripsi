from machine import Pin, Timer
import utime

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
led = Pin(25, Pin.OUT)
timer = Timer()

file = open("temps.txt", "w")

def blink(timer):
    led.toggle()

def fileprocessing(distance):
    timestamp = utime.localtime()
    file.write(str(timestamp)+ " || " + str(distance) + str("cm") + "\n")
    file.flush()
    
def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   fileprocessing(distance)
   print("The distance from object is ",distance,"cm")


while True:
   ultra()
   timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
   utime.sleep(1)
