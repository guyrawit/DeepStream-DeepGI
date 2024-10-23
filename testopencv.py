

import cv2
import gi
import numpy as np

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline with appsrc
# pipeline = Gst.parse_launch(
#     "appsrc name=source ! videoscale ! video/x-raw,width=3840,height=2160  ! videoconvert ! autovideosink "
# )

pipeline = Gst.parse_launch(
     "appsrc name=source ! videoconvert ! video/x-raw, format=I420 ! nvvideoconvert ! video/x-raw(memory:NVMM), width=2160, height=1440 ! nvvideoconvert ! autovideosink"
)


# Get appsrc element
appsrc = pipeline.get_by_name('source')

# Set the properties for appsrc
appsrc.set_property('caps', Gst.Caps.from_string('video/x-raw, format=BGR, width=1920, height=1080'))
appsrc.set_property('is-live', True)
appsrc.set_property('format', Gst.Format.TIME)

# Set pipeline to play state
pipeline.set_state(Gst.State.PLAYING)

# Open the video file using OpenCV
cap = cv2.VideoCapture("filesrc location=/app/local_data/output4.mp4 ! qtdemux ! h264parse ! nvv4l2decoder ! nvvideoconvert ! video/x-raw,format=BGR !  appsink", cv2.CAP_GSTREAMER)

# Loop through the video frames
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Reached the end of the video or encountered an error.")
        break

    # Create a GStreamer buffer from the frame
    buffer = Gst.Buffer.new_allocate(None, frame.nbytes, None)
    buffer.fill(0, frame.tobytes())

    # Push the buffer into appsrc
    appsrc.emit("push-buffer", buffer)

    # Optional: Sleep for a short duration to control the playback rate
    GLib.usleep(33000)  # Approx 30 FPS

# Stop the pipeline and release resources
pipeline.set_state(Gst.State.NULL)
cap.release()
