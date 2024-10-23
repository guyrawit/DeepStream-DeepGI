# Use the NVIDIA DeepStream base image
FROM nvcr.io/nvidia/deepstream:7.1-gc-triton-devel

# Install additional dependencies required for OpenCV and DeepStream
RUN apt-get update && apt-get install -y libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-render-util0 libxcb-shape0 libxcb-xkb1 libxcb-xinerama0 libxkbcommon-x11-0 \
    git cmake build-essential

# Copy the application code to /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Clone the necessary repositories for OpenCV and OpenCV contrib modules
RUN git clone https://github.com/opencv/opencv-python.git && \
    git clone https://github.com/opencv/opencv_contrib.git

# Build OpenCV with GStreamer and CUDA support
ENV CMAKE_ARGS="-D CMAKE_BUILD_TYPE=Release -D WITH_GSTREAMER=ON"

# Create OpenCV wheels using pip
RUN cd opencv-python && \
    pip wheel . --verbose 

# # Install the generated wheel files
# # Assuming the wheel files are in opencv-python/dist/ after the build
# RUN pip install opencv-python/dist/*.whl

# Install any other Python dependencies listed in your requirements file
RUN pip3 install -r requirements_deepstream.txt
