# Final-Project-Edge-Computing-CS131
Developers: Jade Someda and Tanya Carillo

This final project is an implementation of a Smart Monitoring System for Industrial Sites.\
In the case a hazard is detected a message will be sent from the Jetson Nano to Gmail, via Cloud Messaging Services.\

## Architecture & Design/Implementation:
Jetson Nano Developer\
Web-Camera\
Phone (iOS/Android)\
USB-A to USB-C converter\
Google Cloud Service (Workspace - Gmail)\

Messaging Pattern - Event-Driven\
Communcation Protocal -  Simple Mail Transfer Protocol(SMTP)\
Jetson Inference: Detectnet -  AI/Object Detection\

## Training Model:
Framework: Pytorch\
Architecture: SSD (Single Shot Detector)\
Neural Network: Convolutional Neural Network(CNN)\
Activation Function -  ReLu/ReLu6\
Loss Function - SmoothL1/CrossEntropy\
Backbone: modelsVGG/MobileNet/ SqueezeNet\
Optimizer: SGD\

