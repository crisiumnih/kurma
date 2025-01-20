from pid_calc import PIDController
from gait import *
from cam import *

def main():
    pid_x = PIDController(0.5, 0.01, 0.1)
    pid_z = PIDController(0.5, 0.01, 0.1)

    target_x = 0 
    target_z = 1.0

    pipeline = setup_pipeline()

    with dai.device(pipeline) as device:
        video_q = device.getOutputQueue(name="video", maxSize=4, blocking=False)
        detection_q = device.getOutputQueue(name="detections", maxSize=4, blocking=False)

        while True:
            for detection in in_detections.detections:
                if detection.label == 15:
                    current_x = detection.spatialCoordinates.x 
                    current_z = detection.spatialCoordinates.z 

                    #PID Calculations

                    x_control = pid_x.compute(target_x, current_x)
                    z_control = pid_z.compute(target_z, current_z)

                    QuadrupedRobot.walk()

                    if (target_x == current_x) & (target_z == current_z):
                        QuadrupedRobot.stand()

                time.sleep(0.05)

if __name__ == "__main__":
    main()
