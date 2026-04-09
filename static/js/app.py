from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    
    # Assumptions: 40W per light, 75W per fan
    electricity_saved = (lights_saved * 40) + (fans_saved * 75) 
    
    # AI Suggestion based on logic
    if students == 0:
        suggestion = "Turn off devices when room is empty."
    elif students <= 10:
        suggestion = "Small group detected. Using minimal lighting and cooling for optimal efficiency."
    elif students <= 30:
        suggestion = "Medium occupancy. Keep windows open if weather permits to save more fan energy."
    else:
        suggestion = "Optimize energy usage by keeping doors closed."
        
    return jsonify({
        'students': students,
        'lights': lights,
        'fans': fans,
        'electricity_saved': electricity_saved,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

