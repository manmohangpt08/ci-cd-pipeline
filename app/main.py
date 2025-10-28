from flask import Flask
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    ram = psutil.virtual_memory()
    used_gb = ram.used / (1024 ** 3)
    total_gb = ram.total / (1024 ** 3)
    percent = ram.percent
    return f"<h2>Current RAM Usage:</h2><p>{used_gb:.2f} GB / {total_gb:.2f} GB ({percent}%)</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)