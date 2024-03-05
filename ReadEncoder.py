import RPi.GPIO as GPIO
import time

# Define GPIO pins for encoder channels
encoder_channel_A = 17
encoder_channel_B = 27

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins as inputs with pull-down resistors
GPIO.setup(encoder_channel_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_channel_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize variables to keep track of encoder state
encoder_state_A = GPIO.input(encoder_channel_A)
encoder_state_B = GPIO.input(encoder_channel_B)
encoder_position = 0

try:
    while True:
        # Read the current state of the encoder channels
        current_state_A = GPIO.input(encoder_channel_A)
        current_state_B = GPIO.input(encoder_channel_B)

        # Check for changes in encoder state
        if current_state_A != encoder_state_A:
            # Encoder A has changed, update position
            if current_state_A == GPIO.HIGH and current_state_B == GPIO.LOW:
                encoder_position += 1
            elif current_state_A == GPIO.LOW and current_state_B == GPIO.HIGH:
                encoder_position -= 1

        # Update encoder state variables
        encoder_state_A = current_state_A
        encoder_state_B = current_state_B

        # Print the current encoder position and encoder values
        print("Encoder Position: {}, Encoder Values: A={}, B={}".format(encoder_position, current_state_A, current_state_B))

        # Add a small delay to control the speed of reading
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO on exit
    GPIO.cleanup()
