# Check your L4T version with: cat /etc/nv_tegra_release
# Replace r32.7.1 with your version if different
FROM dustynv/jetson-inference:r32.7.1

WORKDIR /jetson-inference

# Install pip and firebase-admin baked into the image
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install firebase-admin

CMD ["bash"]
