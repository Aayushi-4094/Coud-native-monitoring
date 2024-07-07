import psutil
from flask import Flask, jsonify, render_template


app = Flask(__name__)

@app.route('/cpu')
def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    message = None
    if cpu_percent > 80 or mem_percent > 80:
        message = "High CPU or Memory utilisation detected. Please scale up"
    return render_template("index.html", cpu_percent=cpu_percent, mem_percent=mem_percent, message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)