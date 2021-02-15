import Jetson.GPIO as GPIO
import time



def main():
	GPIO.setmode(GPIO.BOARD)
	inputPin1 = 11
	inputPin2 = 12
	GPIO.setup(inputPin1, GPIO.IN)
	GPIO.setup(inputPin2, GPIO.IN)
	while True:
		x1 = GPIO.input(inputPin1)
		x2 = GPIO.input(inputPin2)
		print(x1, " ", x2)
		time.sleep(0.1)

if __name__ == "__main__":
    main()
