document.addEventListener('DOMContentLoaded', () => {
    const studentsInput = document.getElementById('students');
    const calculateBtn = document.getElementById('calculate-btn');
    
    const outStudents = document.getElementById('out-students');
    const outLights = document.getElementById('out-lights');
    const outFans = document.getElementById('out-fans');
    const outSaved = document.getElementById('out-saved');
    const statusText = document.getElementById('status-text');
    
    const manualBtn = document.getElementById('manual-btn');
    const cameraBtn = document.getElementById('toggle-camera-btn');
    const manualSection = document.getElementById('manual-section');
    const cameraSection = document.getElementById('camera-section');

    let manualOverride = false; 
    let phoneFlashlightState = false; // Keep track of light state
    const PHONE_IP_URL = "http://10.231.100.154:8080";

    manualBtn.addEventListener('click', () => {
        manualOverride = true;
        cameraSection.classList.add('hidden');
        manualSection.classList.remove('hidden');
    });

    cameraBtn.addEventListener('click', () => {
        manualOverride = false;
        manualSection.classList.add('hidden');
        cameraSection.classList.remove('hidden');
    });

    calculateBtn.addEventListener('click', () => {
        calculateEnergy(studentsInput.value);
    });
    
    studentsInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') calculateEnergy(studentsInput.value);
    });

    // Auto-fetch camera status
    setInterval(async () => {
        if (manualOverride) return;
        
        try {
            const res = await fetch('/camera_status');
            if(!res.ok) throw new Error("Fetch failed");
            const data = await res.json();
            const studentsDetected = data.detected_students;
            
            if (studentsDetected > 0) {
                statusText.innerHTML = `${studentsDetected} person(s) present`;
                document.body.classList.add('lights-on');
            } else {
                statusText.innerHTML = `No presence detected`;
                document.body.classList.remove('lights-on');
            }

            if (parseInt(outStudents.innerText || 0) !== studentsDetected) {
                calculateEnergy(studentsDetected);
            }
        } catch (e) {
            statusText.innerHTML = `Model connecting...`;
        }
    }, 2000);

    async function calculateEnergy(students) {
        if (students === '' || Number(students) < 0) return;

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ students: parseInt(students) })
            });

            if (!response.ok) throw new Error('API failed');

            const data = await response.json();
            
            animateValue(outStudents, parseInt(outStudents.innerText||0), data.students, 400);
            animateValue(outLights, parseInt(outLights.innerText||0), data.lights, 400);
            animateValue(outFans, parseInt(outFans.innerText||0), data.fans, 400);
            
            // Replicate FinTech balance effect ($40,500.80)
            const currentSaved = parseFloat(outSaved.innerText.replace(/,/g, ''));
            animateValueFloat(outSaved, currentSaved, data.electricity_saved, 600);
            
        } catch (error) {
            console.error('Data error:', error);
        }
    }

    function animateValue(obj, start, end, duration) {
        if(isNaN(start)) start = 0;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = end;
            }
        };
        window.requestAnimationFrame(step);
    }
    
    function animateValueFloat(obj, start, end, duration) {
        if(isNaN(start)) start = 0;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            let val = (progress * (end - start) + start).toFixed(2);
            val = val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            obj.innerHTML = val;
            if (progress < 1 && start !== end) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = end.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
        };
        window.requestAnimationFrame(step);
    }
});
