import numpy as np
import time
from adafruit_servokit import ServoKit
import board
import busio

class SimpleQuadruped:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.kit = ServoKit(channels=16, i2c=i2c, address=0x40)

        # New motor mapping
        self.SERVO_CONFIG = {
            'leg_FR': {'up_down': 0, 'fwd_back': 4},  # Front Right
            'leg_FL': {'up_down': 1, 'fwd_back': 5},  # Front Left
            'leg_BR': {'up_down': 2, 'fwd_back': 6},  # Back Right
            'leg_BL': {'up_down': 3, 'fwd_back': 7}   # Back Left
        }

        # Flipped angles - assuming 90° is neutral
        self.ANGLES = {
            'stand': 165,    # Default standing angle (legs down)
            'up': 175,       # Legs pulled up
            'down': 145,     # Return to standing position
            'forward': 85,   # Leg moved forward
            'back': 145      # Leg moved backward
        }

        self._init_servos()
        self.stand()

    def angle_tester(self):
        """Interactive TUI for testing and adjusting angles"""
        current_angles = self.ANGLES.copy()
        selected_angle = 'stand'

        def print_menu():
            print("\n=== Angle Testing Menu ===")
            print("Current Angles:")
            for name, angle in current_angles.items():
                prefix = "→ " if name == selected_angle else "  "
                print(f"{prefix}{name}: {angle}°")
            print("\nCommands:")
            print("w/s: Select angle to modify")
            print("a/d: Decrease/Increase selected angle by 5°")
            print("1/2: Decrease/Increase selected angle by 1°")
            print("t: Test current angles")
            print("r: Reset to original angles")
            print("q: Save and quit")

        def test_angles():
            print("\nTesting current angles configuration...")
            # Test stand position
            for leg in self.SERVO_CONFIG.values():
                self.kit.servo[leg['up_down']].angle = current_angles['stand']
                self.kit.servo[leg['fwd_back']].angle = 90
            time.sleep(1)

            # Test up position
            print("Testing 'up' position...")
            self.move_leg('leg_FR', current_angles['up'], current_angles['forward'])
            time.sleep(1)

            # Test down position
            print("Testing 'down' position...")
            self.move_leg('leg_FR', current_angles['down'], current_angles['back'])
            time.sleep(1)

            # Return to stand
            self.stand()

        angle_names = list(current_angles.keys())
        current_idx = 0

        while True:
            print_menu()
            cmd = input("\nEnter command: ").lower()

            if cmd == 'w':  # Move selection up
                current_idx = (current_idx - 1) % len(angle_names)
                selected_angle = angle_names[current_idx]

            elif cmd == 's':  # Move selection down
                current_idx = (current_idx + 1) % len(angle_names)
                selected_angle = angle_names[current_idx]

            elif cmd == 'a':  # Decrease by 5
                current_angles[selected_angle] = max(0, current_angles[selected_angle] - 5)

            elif cmd == 'd':  # Increase by 5
                current_angles[selected_angle] = min(180, current_angles[selected_angle] + 5)

            elif cmd == '1':  # Decrease by 1
                current_angles[selected_angle] = max(0, current_angles[selected_angle] - 1)

            elif cmd == '2':  # Increase by 1
                current_angles[selected_angle] = min(180, current_angles[selected_angle] + 1)

            elif cmd == 't':  # Test current configuration
                test_angles()

            elif cmd == 'r':  # Reset angles
                current_angles = self.ANGLES.copy()

            elif cmd == 'q':  # Save and quit
                save = input("Save these angles as new defaults? (y/n): ").lower()
                if save == 'y':
                    self.ANGLES = current_angles.copy()
                    print("Angles saved!")
                break

    def _init_servos(self):
        """Initialize all servos to neutral position"""
        for leg in self.SERVO_CONFIG.values():
            for servo in leg.values():
                self.kit.servo[servo].set_pulse_width_range(500, 2500)
                self.kit.servo[servo].angle = 90
                time.sleep(0.1)

    def stand(self):
        """Put the robot in standing position"""
        print("Standing up...")
        # Set all vertical servos to standing angle
        for leg in self.SERVO_CONFIG.values():
            self.kit.servo[leg['up_down']].angle = self.ANGLES['stand']
            self.kit.servo[leg['fwd_back']].angle = 90  # Neutral forward/back position
        time.sleep(1)

    def move_leg(self, leg_name, vertical_pos, horizontal_pos):
        """Move a specific leg to given positions"""
        servos = self.SERVO_CONFIG[leg_name]
        self.kit.servo[servos['up_down']].angle = vertical_pos
        self.kit.servo[servos['fwd_back']].angle = horizontal_pos

    def walking_gait(self):
        """Implement walking gait using state-based diagonal leg movements"""
        try:
            while True:
                # State 1: Diagonal pairs in opposite positions
                print("State 1")
                # FR and BL diagonal pair
                self.move_leg('leg_FR', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_BL', self.ANGLES['up'], self.ANGLES['forward'])
                # FL and BR diagonal pair
                self.move_leg('leg_FL', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BR', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.25)

                # State 2: First transition state
                print("State 2")
                self.move_leg('leg_FR', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_BL', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_FL', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BR', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.25)

                # State 3: Opposite diagonal pairs
                print("State 3")
                # FL and BR diagonal pair
                self.move_leg('leg_FL', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_BR', self.ANGLES['up'], self.ANGLES['forward'])
                # FR and BL diagonal pair
                self.move_leg('leg_FR', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BL', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.25)

                # State 4: Second transition state
                print("State 4")
                self.move_leg('leg_FL', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_BR', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_FR', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BL', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.25)

        except KeyboardInterrupt:
            print("\nStopping walking gait...")
            self.stand()

    def trot_gait(self):
        """Implement trot gait - diagonal legs move together"""
        try:
            while True:
                # Phase 1: FR + BL up and forward
                print("Phase 1: FR + BL")
                self.move_leg('leg_FR', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_BL', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_FL', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BR', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.2)

                # Put FR + BL down
                self.move_leg('leg_FR', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_BL', self.ANGLES['down'], self.ANGLES['forward'])
                time.sleep(0.2)

                # Phase 2: FL + BR up and forward
                print("Phase 2: FL + BR")
                self.move_leg('leg_FL', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_BR', self.ANGLES['up'], self.ANGLES['forward'])
                self.move_leg('leg_FR', self.ANGLES['down'], self.ANGLES['back'])
                self.move_leg('leg_BL', self.ANGLES['down'], self.ANGLES['back'])
                time.sleep(0.2)

                # Put FL + BR down
                self.move_leg('leg_FL', self.ANGLES['down'], self.ANGLES['forward'])
                self.move_leg('leg_BR', self.ANGLES['down'], self.ANGLES['forward'])
                time.sleep(0.2)

        except KeyboardInterrupt:
            print("\nStopping trot...")
            self.stand()

    def creep_gait(self):
        """Implement creep gait - one leg at a time"""
        sequence = ['leg_FR', 'leg_FL', 'leg_BR', 'leg_BL']

        try:
            while True:
                for leg in sequence:
                    print(f"Moving {leg}")
                    # Lift and move forward
                    self.move_leg(leg, self.ANGLES['up'], self.ANGLES['forward'])
                    time.sleep(0.2)
                    # Put down
                    self.move_leg(leg, self.ANGLES['down'], self.ANGLES['forward'])
                    time.sleep(0.2)
                    # Move back while down
                    self.move_leg(leg, self.ANGLES['down'], self.ANGLES['back'])
                    time.sleep(0.2)

        except KeyboardInterrupt:
            print("\nStopping creep...")
            self.stand()

def main():
    robot = SimpleQuadruped()

    while True:
        command = input("\nEnter command (s: stand, t: trot, c: creep, w: walk, a: angle test, r: reset, q: quit): ")

        if command.lower() == 's':
            robot.stand()
        elif command.lower() == 't':
            print("Starting trot gait... Press CTRL+C to stop")
            robot.trot_gait()
        elif command.lower() == 'c':
            print("Starting creep gait... Press CTRL+C to stop")
            robot.creep_gait()
        elif command.lower() == 'w':
            print("Starting walking gait... Press CTRL+C to stop")
            robot.walking_gait()
        elif command.lower() == 'a':
            print("Entering angle test mode...")
            robot.angle_tester()
        elif command.lower() == 'r':
            print("Resetting position...")
            robot._init_servos()
        elif command.lower() == 'q':
            print("Quitting...")
            robot._init_servos()
            break
        else:
            print("Invalid command!")

if __name__ == "__main__":
    main()

