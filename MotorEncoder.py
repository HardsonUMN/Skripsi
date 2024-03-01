import RPi.GPIO as GPIO
import time

# Motor Connections (Both must use PWM pins)
RPWM = 5
LPWM = 6

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set motor connections as outputs
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

# Create PWM objects for RPWM and LPWM
rpwm_pwm = GPIO.PWM(RPWM, 1000)  # 1000 Hz PWM frequency
lpwm_pwm = GPIO.PWM(LPWM, 1000)  # 1000 Hz PWM frequency

# Stop motors
rpwm_pwm.start(0)
lpwm_pwm.start(0)

try:
    while True:
        # Accelerate forward
        GPIO.output(RPWM, GPIO.LOW)
        for i in range(255):
            lpwm_pwm.ChangeDutyCycle(i)
            time.sleep(0.02)

        time.sleep(1)

        # Decelerate forward
        for i in range(255, -1, -1):
            lpwm_pwm.ChangeDutyCycle(i)
            time.sleep(0.02)

        time.sleep(0.5)

        # Accelerate reverse
        GPIO.output(LPWM, GPIO.LOW)
        for i in range(255):
            rpwm_pwm.ChangeDutyCycle(i)
            time.sleep(0.02)

        time.sleep(1)

        # Decelerate reverse
        for i in range(255, -1, -1):
            rpwm_pwm.ChangeDutyCycle(i)
            time.sleep(0.02)

        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO on exit
    rpwm_pwm.stop()
    lpwm_pwm.stop()
    GPIO.cleanup()