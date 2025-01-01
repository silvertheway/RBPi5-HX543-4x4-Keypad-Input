import RPi.GPIO as GPIO
import time

LeftGPIOInputs = [5,6,13,19]
RightGPIOInputs = [12,16,20,21]
KeypadInputs = [
["1","2","3","A"],
["4","5","6","B"],
["7","8","9","C"],
["*","0","#","D"]
]
KeysHeld = []
HeldChecks = 3 # yes this is so stupid. i hate this keypad and the way it works.
CurrentChecks = 0

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for Pin in range(0,3):
    GPIO.setup(LeftGPIOInputs[Pin],GPIO.OUT)
    GPIO.setup(RightGPIOInputs[Pin], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def readLine(Pin, Char):
    global CurrentChecks
    global HeldChecks
    global KeysHeld
    
    CurrentChecks +=1
    GPIO.output(Pin, GPIO.HIGH)
    for i in range(0,3): #read inputs.
        if (GPIO.input(RightGPIOInputs[i]) == 1 and not RightGPIOInputs[i] in KeysHeld):
            KeysHeld.append(RightGPIOInputs[i])
            print(Char[i])
    if CurrentChecks >= HeldChecks:
        for Key in KeysHeld:
            if (GPIO.input(Key) == 0):
                KeysHeld.remove(Key)
        CurrentChecks = 0
            
    GPIO.output(Pin, GPIO.LOW)

try:
    while True:
        for i in range(0,3):
            readLine(LeftGPIOInputs[i], KeypadInputs[i])
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
