from machine import Pin
import utime

# Define GPIO pins for encoder channels
encoder_channel_A = 16
encoder_channel_B = 17

# Setup GPIO pins as inputs with pull-down resistors
encoder_A = Pin(encoder_channel_A, Pin.IN, Pin.PULL_DOWN)
encoder_B = Pin(encoder_channel_B, Pin.IN, Pin.PULL_DOWN)

# Initialize variables to keep track of encoder state
encoder_position = 0
prev_state_A = encoder_A.value()
prev_state_B = encoder_B.value()


try:
    while True:
        # Read the current state of the encoder channels
        current_state_A = encoder_A.value()
        current_state_B = encoder_B.value()
        
        # Check for changes in encoder state
        if current_state_A != prev_state_A or current_state_B != prev_state_B:
            # Encoder A has changed, update position
            if current_state_A == 1 and prev_state_A == 0 and current_state_A > current_state_B:
                encoder_position += 1
                
            elif current_state_B == 1 and prev_state_B == 0 and current_state_A < current_state_B:
                encoder_position -= 1

        # Update encoder state variables
        prev_state_A = current_state_A
        prev_state_B = current_state_B

        # Print the current encoder position and encoder values
        print("Encoder Position: {}, Encoder Values: A={}, B={}".format(encoder_position, current_state_A, current_state_B))

        # Add a small delay to control the speed of reading
        utime.sleep_ms(10)

except KeyboardInterrupt:
    pass
