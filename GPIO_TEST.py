import Jetson.GPIO as GPIO
import sys
import time 

led_pin = 40

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led_pin, GPIO.OUT)
    try:
        while True:
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(1)
            print("运行正常")
    except :
        print("ERROR")
    finally:
        GPIO.cleanup(led_pin)

if __name__ == '__main__':
    main()        

