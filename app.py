import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2
import atexit
from get_soil_MCP3021_data import get_soil_data

app = Flask(__name__)

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (640, 360
    )}
)
picam2.configure(config)
picam2.start()



def get_soil_raw():
    timestamps, raw, percent = get_soil_data(10)
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_title("Soil MCP3021 Raw")
    ax.set_facecolor("lightgray")
    ax.plot(timestamps, raw, linestyle="dashed", marker="o", color="red")
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel("RAW")
    ax.spines['top'].set_color('blue')
    ax.spines['left'].set_color('blue')
    ax.spines['right'].set_color('blue')
    ax.spines['bottom'].set_color('blue')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def get_soil_percent():
    timestamps, raw, percent = get_soil_data(10)
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_title("Soil MCP3021 Percent")
    ax.set_facecolor("lightgray")
    ax.plot(timestamps, percent, linestyle="dashed", marker="o", color="blue")
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel("Percent (%)")
    ax.spines['top'].set_color('blue')
    ax.spines['left'].set_color('blue')
    ax.spines['right'].set_color('blue')
    ax.spines['bottom'].set_color('blue')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def generate_frames():
    while True:
        frame = picam2.capture_array()

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

def take_picture():
    filename = "static/img/image.jpg"
    picam2.capture_file(filename)
        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/soil")
def soil():
    soil_raw = get_soil_raw()
    soil_percent = get_soil_percent()
    return render_template("soil.html", soil_raw=soil_raw, soil_percent=soil_percent)

@app.route("/take_pic")
def take_picture_route():
    take_picture()
    return {"status": "ok"}
@app.route("/live")
def live():
    return render_template("live.html" )

@app.route("/camera_feed")
def camera_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@atexit.register
def cleanup():
    try:
        picam2.stop()
    except Exception:
        pass
app.run(debug=True)