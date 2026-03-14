import jetson.inference
import jetson.utils
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
#This is the trigger file: 
# The “trigger” file refers to the file that communicates with the jetson-nano and the cloud. 
# This file sources the training model, feeds it into detectnet/jetson-inference 
# which assesses the live visual feedback that's being received from the camera. 
# If a hazard(a label) is detected then the jetson-nano communicates 
# to the cloud to then send a specific message/gmail to the user.  

# Email setup
SENDER_EMAIL = "[insert_email_address]@gmail.com"  # REPLACE with your Gmail
SENDER_PASSWORD = "[insert_16_character_password]"  # REPLACE with Gmail App Password
RECIPIENT_EMAIL = "[insert_email_address]@gmail.com"  # REPLACE with email on your phone

# Cooldown setup
last_alert_time = {}
COOLDOWN = 30  # seconds

# Labels
WORKER_LABEL = 'worker'
HELMET_LABEL = 'helmet'
JACKET_LABEL = 'jacket'
MACHINE_LABEL = 'machine'

def send_alert(alert_type):
    current_time = time.time()
    
    # Check cooldown per alert type
    if alert_type in last_alert_time:
        if current_time - last_alert_time[alert_type] < COOLDOWN:
            return
    
    # Set message based on alert type
    if alert_type == 'no-helmet':
        subject = 'URGENT: Helmet Violation Near Machine!'
        body = 'DANGER: Worker detected without a helmet near machinery on construction site!'
    elif alert_type == 'no-jacket':
        subject = 'URGENT: Jacket Violation Near Machine!'
        body = 'DANGER: Worker detected without a safety jacket near machinery on construction site!'
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("[OK] Email alert sent: %s" % alert_type)
        last_alert_time[alert_type] = current_time
    except Exception as e:
        print("[ERROR] Failed to send email: %s | Error: %s" % (alert_type, str(e)))

# Load detection model
net = jetson.inference.detectNet(
    argv=[
        "--model=/jetson-inference/python/training/detection/ssd/models/construction-safety/ssd-mobilenet.onnx",
        "--labels=/jetson-inference/python/training/detection/ssd/models/construction-safety/labels.txt",
        "--input-blob=input_0",
        "--output-cvg=scores",
        "--output-bbox=boxes",
        "--threshold=0.3"
    ]
)

# Open webcam
camera = jetson.utils.videoSource("/dev/video0")
display = jetson.utils.videoOutput("display://0")

print("Starting hazard detection...")

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img)
    
    # Collect all detected labels in this frame
    detected_labels = [net.GetClassDesc(d.ClassID) for d in detections]
    print("Detected labels: %s" % detected_labels)
    
    # CRITICAL CHANGE: Only send alert if BOTH worker AND machine are detected
    if WORKER_LABEL in detected_labels and MACHINE_LABEL in detected_labels:
        print(">>> Worker AND machine detected in same frame!")
        
        # Worker near machine but no helmet
        if HELMET_LABEL not in detected_labels:
            print("DANGER: Worker without helmet near machine!")
            send_alert('no-helmet')
        
        # Worker near machine but no jacket
        if JACKET_LABEL not in detected_labels:
            print("DANGER: Worker without jacket near machine!")
            send_alert('no-jacket')
    elif WORKER_LABEL in detected_labels:
        print("Worker detected, but no machine nearby - no alert sent")
    elif MACHINE_LABEL in detected_labels:
        print("Machine detected, but no worker nearby - no alert sent")
    
    display.Render(img)
    display.SetStatus("Hazard Detection | FPS: %.0f" % net.GetNetworkFPS())

