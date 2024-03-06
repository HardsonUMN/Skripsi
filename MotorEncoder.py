from machine import Pin, PWM
import utime

# Motor Connections (Both must use PWM pins)
RPWM = 0  # Replace with the actual GPIO pin number for RPWM
LPWM = 1  # Replace with the actual GPIO pin number for LPWM

# Set up the GPIO pins as outputs
rpwm_pin = Pin(RPWM, Pin.OUT)
lpwm_pin = Pin(LPWM, Pin.OUT)

# Create PWM objects for RPWM and LPWM
rpwm_pwm = PWM(rpwm_pin, freq=1000, duty=0)
lpwm_pwm = PWM(lpwm_pin, freq=1000, duty=0)

try:
    while True:
        # Accelerate forward
        rpwm_pwm.duty(0)
        for i in range(255):
            lpwm_pwm.duty(i)
            utime.sleep_ms(20)

        utime.sleep(1)

        # Decelerate forward
        for i in range(255, -1, -1):
            lpwm_pwm.duty(i)
            utime.sleep_ms(20)

        utime.sleep(0.5)

        # Accelerate reverse
        lpwm_pwm.duty(0)
        for i in range(255):
            rpwm_pwm.duty(i)
            utime.sleep_ms(20)

        utime.sleep(1)

        # Decelerate reverse
        for i in range(255, -1, -1):
            rpwm_pwm.duty(i)
            utime.sleep_ms(20)

        utime.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    # Stop PWM and clean up GPIO on exit
    rpwm_pwm.deinit()
    lpwm_pwm.deinit()
