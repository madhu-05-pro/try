from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    phone_number = data.get('phoneNumber')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not phone_number or latitude is None or longitude is None:
        return "Missing data", 400

    message = f"Emergency! Contact: {phone_number}. Location: {latitude}, {longitude}"
    adb_command = f'adb shell am start -a android.intent.action.SENDTO -d sms:+919790559885 --es sms_body "{message}" --ez exit_on_sent true'
    
    try:
        subprocess.run(adb_command, shell=True, check=True)
        return "SMS sent successfully!"
    except subprocess.CalledProcessError as e:
        return f"Failed to send SMS: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
