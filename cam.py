import cv2
import depthai as dai

# Create a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(30)

# Define a neural network
detection_nn = pipeline.createMobileNetDetectionNetwork()
detection_nn.setConfidenceThreshold(0.5)
# Set the correct blob path for MobileNet-SSD
detection_nn.setBlobPath("models/mobilenet-ssd_openvino_2021.2.blob")
cam_rgb.preview.link(detection_nn.input)

# XLink outputs
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("detections")
detection_nn.out.link(xout_nn.input)

