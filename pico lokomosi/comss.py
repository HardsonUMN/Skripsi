import machine
import utime

# Configure UART
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

try:
    while True:
        # Receive data
        if uart.any():
            received_data = uart.readline().decode('utf-8').strip()
            #print("Received:", received_data)

        # Send data
        uart.write(received_data.encode('utf-8')
        #print("Sent: Hello from Raspberry Pico!")

        utime.sleep(1)

except KeyboardInterrupt:
    print("UART communication closed.")

