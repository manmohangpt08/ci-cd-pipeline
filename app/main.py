from flask import Flask
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    # RAM stats
    ram = psutil.virtual_memory()
    used_gb = ram.used / (1024 ** 3)
    total_gb = ram.total / (1024 ** 3)
    ram_percent = ram.percent

    # CPU stats
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=True)

    # HTML response
    html = f"""
    <html>
    <head>
        <title>System Monitor</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                color: #333;
                text-align: center;
                padding-top: 50px;
            }}
            .card {{
                background: white;
                display: inline-block;
                padding: 20px 40px;
                border-radius: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #0066cc;
            }}
            h2 {{
                color: #009933;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>System Monitor</h1>
            <h2>CPU Usage:</h2>
            <p>{cpu_percent}% of {cpu_cores} cores</p>
            <h2>RAM Usage:</h2>
            <p>{used_gb:.2f} GB / {total_gb:.2f} GB ({ram_percent}%)</p>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
