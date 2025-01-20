import blobconverter

# Download the MobileNet-SSD blob
blob_path = blobconverter.from_zoo(
    name="mobilenet-ssd",
    shaves=6,  # Adjust shaves based on your device (e.g., 6 for OAK-D Pro)
    version="2021.2"
)

