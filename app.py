import cv2
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

import requests
import threading

# Global variable to store detected student count
current_students_detected = 0
camera = None

# Just using local PC webcam
CAMERA_SOURCE = 0

def toggle_phone_light(turn_on):
    # Disabled since we are using PC webcam
    pass

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(CAMERA_SOURCE)
    return camera

def gen_frames():  
    global current_students_detected
    cam = get_camera()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        success, frame = cam.read()
        if not success:
            # If camera fails, reconnect
            cam.open(CAMERA_SOURCE)
            continue
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            current_students_detected = len(faces)
            
            # Flashlight Logic
            if current_students_detected > 0:
                threading.Thread(target=toggle_phone_light, args=(True,)).start()
            else:
                threading.Thread(target=toggle_phone_light, args=(False,)).start()
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Person', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Route for the real-time video stream
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_status')
def camera_status():
    # Route to get the number of students currently detected by the camera
    global current_students_detected
    return jsonify({'detected_students': current_students_detected})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        students = int(data.get('students', 0))
    except (ValueError, TypeError):
        students = 0
        
    if students == 0:
        lights, fans = 0, 0
    elif 1 <= students <= 10:
        lights, fans = 1, 1
    elif 11 <= students <= 30:
        lights, fans = 2, 2
    elif 31 <= students <= 60:
        lights, fans = 3, 3
    else:
        lights, fans = 4, 4
        
    max_lights, max_fans = 4, 4
    lights_saved = max_lights - lights
    fans_saved = max_fans - fans
    
    electricity_saved = (lights_saved * 40) + (fans_saved * 75) 
    
    if students == 0:
        suggestion = "Room is empty. Lights automatically turned OFF."
    elif students <= 10:
        suggestion = "Small group detected. Using minimal lighting/cooling."
    elif students <= 30:
        suggestion = "Medium occupancy. System adjusting properly."
    else:
        suggestion = "Full capacity. Keep doors closed for optimal AC."
        
    return jsonify({
        'students': students,
        'lights': lights,
        'fans': fans,
        'electricity_saved': electricity_saved,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)