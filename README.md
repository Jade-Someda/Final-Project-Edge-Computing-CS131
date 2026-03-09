# Final-Project-Edge-Computing-CS131
# Developers: Jade Someda and Tanya Carillo

This final project is an implementation of a Smart Monitoring System for Industrial Sites.\
In the case a hazard is detected a message will be sent from the Jetson Nano to Gmail, via Cloud Messaging Services.

## Architecture & Design/Implementation:
Jetson Nano Developer\
Web-Camera\
Phone (iOS/Android)\
USB-A to USB-C converter\
Google Cloud Service (Workspace - Gmail)\

Messaging Pattern - Event-Driven\
Communcation Protocal -  Simple Mail Transfer Protocol(SMTP)\
Jetson Inference: Detectnet -  AI/Object Detection\
SwapSpace - Virtualize memory to have more space to store Ephochs. 

## Training Model:
Framework: Pytorch\
Architecture: SSD (Single Shot Detector)\
Neural Network: Convolutional Neural Network(CNN)\
Activation Function -  ReLu/ReLu6\
Loss Function - SmoothL1/CrossEntropy\
Backbone: modelsVGG/MobileNet/ SqueezeNet\
Optimizer: SGD\

# Resources:
RoboFlow Universide for our Dataset (Image Format: Pascal VOC XML)

# Challenges
* 5 year old SSD card lead to significant training-time taking twice as long as anticipated.
* We had not trained a model before, so this slowed our process. (Organizing the correct direcories, choosing a good dataset, ensuring 1:1 ratio between XML/JPEG files, etc)
*  Time Constraint: Completed this in 3 weeks.
*  We planned to use Push-Notification/Event-Driven Messaging Pattern with Firebase(HTTPS), but we were unable to generate a token(used to communcate between the cloud and phone), so we switched to SMTP(ie. using gmail as the messaging protocal).


 # Reflection: 
 We succesfully were able to train a model with a dataset of 500+ images, with 40 Ephocs and batch size of 2. Our Webcamera was our vision system, and the Jetson Nano was able to detect our labels with the training. And once a label was detected the codebase, would then trigger to communcate to Google Cloud which would then send a notification/message via Gmail which was viewed via Phone.\

For instance: If a worker was detected not wearing a helmet, then a message regarding this hazard was sent.\

We saw the versatility of this device, since current Safety Survelliance is often reliant upon human error. Watchman watching various camera's or up to the sueprvision of upper-management faculty who can only see so much at once. Our vision for this project was that multiple Smart Montiers can be placed on site, and be the 'extra-pair' of eyes. Once a hazard is dected the manager can simply see the notification and proceed as neccesary.\

Overall this project intersting and we learned quite a lot about AI/ML training and in working with Edge Devices. 
