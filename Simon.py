import RPi.GPIO as GPIO
from time import sleep
from random import randint
import pygame

# set to True to enable debugging output
DEBUG = False

# initialize the pygame library
pygame.init()

# stores the score throughout the game
score = 0

# sends when the user loses, changes after a score of 1
lose_message = "You didn't even make it to a sequence!"

# set the GPIO pin numbers
# the switches (from L to R)
switches = [20, 16, 12, 26]

# the LEDs (from L to R)
leds = [6, 13, 19, 21]

# the sounds that map to each LED (from L to R)
sounds = [
    pygame.mixer.Sound("one.wav"),
    pygame.mixer.Sound("two.wav"),
    pygame.mixer.Sound("three.wav"),
    pygame.mixer.Sound("four.wav")
]

# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the input and output pins
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)

# this function turns the LEDs on
def all_on():
    for i in leds:
        GPIO.output(leds, True)

# this function turns the LEDs off
def all_off():
    for i in leds:
        GPIO.output(leds, False)

# this function flashes the LEDs a few times when the player loses the game
def lose():
    print(lose_message)
    for i in range(0, 4):
        all_on()
        sleep(0.5)
        all_off()
        sleep(0.5)

# the main part of the program
# initialize the Simon sequence
# each item in the sequence represents an LED (or switch), indexed at 0 through 3
seq = []

# randomly add the first two items to the sequence
seq.append(randint(0, 3))
seq.append(randint(0, 3))

print("Welcome to Simon!")
print("Try to play the sequence back by pressing the switches.")
print("Press Ctrl+C to exit...")

# we'll discuss this later, but this allows us to detect
# when Ctrl+C is pressed so that we can reset the GPIO pins
try:
    # keep going until the user presses Ctrl+C
    while True:
        # randomly add one more item to the sequence
        seq.append(randint(0, 3))
        
        if DEBUG:
            # display the sequence to the console
            if len(seq) > 3:
                print()
            print("seq={}".format(seq))
        
        # display the sequence using the LEDs
        for s in seq:
            # turn the appropriate LED on
            GPIO.output(leds[s], True)
            # play its corresponding sound
            sounds[s].play()
            # wait and turn the LED off again
            sleep(1)
            GPIO.output(leds[s], False)
            sleep(0.5)
        
        # wait for player input (via the switches)
        # initialize the count of switches pressed to 0
        switch_count = 0
        
        # keep accepting player input until the number of items in the sequence is reached
        while switch_count < len(seq):
            # initially note that no switch is pressed
            # this will help with switch debouncing
            pressed = False
            
            # so long as no switch is currently pressed...
            while not pressed:
                # ...we can check the status of each switch
                for i in range(len(switches)):
                    # if one switch is pressed
                    while GPIO.input(switches[i]):
                        # note its index
                        val = i
                        # note that a switch has now been pressed
                        pressed = True
            
            if DEBUG:
                # display the index of the switch pressed
                print(val)
            
            # light the matching LED
            GPIO.output(leds[val], True)
            # play its corresponding sound
            sounds[val].play()
            # wait and turn the LED off again
            sleep(1)
            GPIO.output(leds[val], False)
            sleep(0.25)
            
            # check to see if this LED is correct in the sequence
            if val != seq[switch_count]:
                # player is incorrect; invoke the lose function
                lose()
                # reset the GPIO pins
                GPIO.cleanup()
                # exit the game
                exit(0)
            
            # if the player has this item in the sequence correct, increment the count
            switch_count += 1

# detect Ctrl+C
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
