from adafruit_servokit import ServoKit
import board
import busio
import time


# Initialize servo controller
i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16, i2c=i2c, address=0x40)

# Define angles
STAND = 165    # Default standing angle
UP = 100       # Legs up position
DOWN = 160      # Legs down position
FWD = 60       # Forward position
BACK = 120      # Back position
MID = 70       # Middle position


adjust=15

# Initialize all servos
for i in range(8):
    kit.servo[i].set_pulse_width_range(500, 2500)
    # Set all servos to standing position
    if i < 4:  # Vertical servos
        kit.servo[i].angle = STAND
    else:      # Horizontal servos
        kit.servo[i].angle = 90
    time.sleep(0.1)

def walking_state_1():
    # Vertical servos (0-3)
    kit.servo[0].angle = DOWN+10
    kit.servo[1].angle = UP
    kit.servo[2].angle = DOWN+10
    kit.servo[3].angle = UP

    # Horizontal servos (4-7)
    kit.servo[4].angle = FWD
    kit.servo[5].angle = FWD
    kit.servo[6].angle = FWD-10
    kit.servo[7].angle = FWD

def walking_state_2():
    # Vertical servos
    kit.servo[0].angle = UP
    kit.servo[1].angle = DOWN
    kit.servo[2].angle = UP
    kit.servo[3].angle = DOWN

    # Horizontal servos
    kit.servo[4].angle = FWD
    kit.servo[5].angle = FWD
    kit.servo[6].angle = FWD-10
    kit.servo[7].angle = FWD

def walking_state_3():
    # Vertical servos
    kit.servo[0].angle = UP+15
    kit.servo[1].angle = DOWN
    kit.servo[2].angle = UP
    kit.servo[3].angle = DOWN

    # Horizontal servos
    kit.servo[4].angle = BACK+10
    kit.servo[5].angle = BACK
    kit.servo[6].angle = BACK
    kit.servo[7].angle = BACK

def walking_state_4():
    # Vertical servos
    kit.servo[0].angle = DOWN+10
    kit.servo[1].angle = UP
    kit.servo[2].angle = DOWN
    kit.servo[3].angle = UP

    # Horizontal servos
    kit.servo[4].angle = BACK+10
    kit.servo[5].angle = BACK
    kit.servo[6].angle = BACK
    kit.servo[7].angle = BACK

def stand():
    """Return to standing position"""
    for i in range(8):
        if i < 4:  # Vertical servos
            kit.servo[i].angle = STAND
        else:      # Horizontal servos
            kit.servo[i].angle = 90
        time.sleep(0.1)

try:
    print("Starting walking sequence. Press CTRL+C to stop.")
    while True:
        walking_state_1()
        time.sleep(0.25)
        walking_state_2()
        time.sleep(0.25)
        walking_state_3()
        time.sleep(0.25)
        walking_state_4()
        time.sleep(0.25)

except KeyboardInterrupt:
    print("\nStopping and returning to stand position...")
    stand()