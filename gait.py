from adafruit_servokit import ServoKit
import board
import busio
import time

class QuadrupedRobot:
    def __init__(self, i2c_address=0x40, channels=16):
        # Initialize servo controller
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.kit = ServoKit(channels=channels, i2c=self.i2c, address=i2c_address)

        # Define angles
        self.STAND = 165    # Default standing angle
        self.UP = 100       # Legs up position
        self.DOWN = 160     # Legs down position
        self.FWD = 60       # Forward position
        self.BACK = 120     # Back position
        self.MID = 70       # Middle position
        self.adjust = 15

        # Initialize servos
        self.initialize_servos()

    def initialize_servos(self):
        """Set all servos to their default positions."""
        for i in range(8):
            self.kit.servo[i].set_pulse_width_range(500, 2500)
            # Set all servos to standing position
            if i < 4:  # Vertical servos
                self.kit.servo[i].angle = self.STAND
            else:      # Horizontal servos
                self.kit.servo[i].angle = 90
            time.sleep(0.1)

    def walking_state_1(self):
        """Execute walking state 1."""
        # Vertical servos (0-3)
        self.kit.servo[0].angle = self.DOWN + 10
        self.kit.servo[1].angle = self.UP
        self.kit.servo[2].angle = self.DOWN + 10
        self.kit.servo[3].angle = self.UP

        # Horizontal servos (4-7)
        self.kit.servo[4].angle = self.FWD
        self.kit.servo[5].angle = self.FWD
        self.kit.servo[6].angle = self.FWD - 10
        self.kit.servo[7].angle = self.FWD

    def walking_state_2(self):
        """Execute walking state 2."""
        # Vertical servos
        self.kit.servo[0].angle = self.UP
        self.kit.servo[1].angle = self.DOWN
        self.kit.servo[2].angle = self.UP
        self.kit.servo[3].angle = self.DOWN

        # Horizontal servos
        self.kit.servo[4].angle = self.FWD
        self.kit.servo[5].angle = self.FWD
        self.kit.servo[6].angle = self.FWD - 10
        self.kit.servo[7].angle = self.FWD

    def walking_state_3(self):
        """Execute walking state 3."""
        # Vertical servos
        self.kit.servo[0].angle = self.UP + 15
        self.kit.servo[1].angle = self.DOWN
        self.kit.servo[2].angle = self.UP
        self.kit.servo[3].angle = self.DOWN

        # Horizontal servos
        self.kit.servo[4].angle = self.BACK + 10
        self.kit.servo[5].angle = self.BACK
        self.kit.servo[6].angle = self.BACK
        self.kit.servo[7].angle = self.BACK

    def walking_state_4(self):
        """Execute walking state 4."""
        # Vertical servos
        self.kit.servo[0].angle = self.DOWN + 10
        self.kit.servo[1].angle = self.UP
        self.kit.servo[2].angle = self.DOWN
        self.kit.servo[3].angle = self.UP

        # Horizontal servos
        self.kit.servo[4].angle = self.BACK + 10
        self.kit.servo[5].angle = self.BACK
        self.kit.servo[6].angle = self.BACK
        self.kit.servo[7].angle = self.BACK

    def stand(self):
        """Return to standing position."""
        for i in range(8):
            if i < 4:  # Vertical servos
                self.kit.servo[i].angle = self.STAND
            else:      # Horizontal servos
                self.kit.servo[i].angle = 90
            time.sleep(0.1)

    def walk(self, steps=1):
        """Perform a walking sequence for a given number of steps."""
        for _ in range(steps):
            self.walking_state_1()
            time.sleep(0.25)
            self.walking_state_2()
            time.sleep(0.25)
            self.walking_state_3()
            time.sleep(0.25)
            self.walking_state_4()
            time.sleep(0.25)
