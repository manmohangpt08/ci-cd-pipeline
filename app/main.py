from flask import Flask
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    # RAM stats
    ram = psutil.virtual_memory()
    used_ram_gb = ram.used / (1024 ** 3)
    total_ram_gb = ram.total / (1024 ** 3)
    ram_percent = ram.percent

    # CPU stats
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=True)

    # Disk stats (root filesystem)
    disk = psutil.disk_usage('/')
    used_disk_gb = disk.used / (1024 ** 3)
    total_disk_gb = disk.total / (1024 ** 3)
    free_disk_gb = disk.free / (1024 ** 3)
    disk_percent = disk.percent

    # HTML response
    html = f"""
    <html>
    <head>
        <title>System Monitor</title>
        <meta http-equiv="refresh" content="5">
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
                padding: 25px 50px;
                border-radius: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.15);
                min-width: 400px;
            }}
            h1 {{
                color: #0066cc;
            }}
            h2 {{
                color: #009933;
            }}
            p {{
                font-size: 1.1em;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>System Usage Monitoring</h1>

            <h2>CPU Usage:</h2>
            <p>{cpu_percent}% of {cpu_cores} cores</p>

            <h2>RAM Usage:</h2>
            <p>{used_ram_gb:.2f} GB / {total_ram_gb:.2f} GB ({ram_percent}%)</p>

            <h2>Disk Usage:</h2>
            <p>{used_disk_gb:.2f} GB used / {total_disk_gb:.2f} GB total ({disk_percent}%)</p>
            <p>Free space: {free_disk_gb:.2f} GB</p>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
