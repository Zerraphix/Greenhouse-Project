import os
import base64
from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure
from flask import Flask, render_template, Response, jsonify
from picamera2 import Picamera2
import cv2
import atexit

from get_soil_MCP3021_data import get_soil_data
from log_image_data import create_image_table, insert_image
from get_image_data import get_latest_image, get_images

app = Flask(__name__)

os.makedirs("static/img", exist_ok=True)
os.makedirs("database", exist_ok=True)

create_image_table()

picam2 = None
camera_available = False


def setup_camera():
    global picam2, camera_available

    try:
        picam2 = Picamera2()

        config = picam2.create_preview_configuration(
            main={"size": (640, 360)}
        )
        picam2.configure(config)
        picam2.start()

        camera_available = True
        print("Camera initialized successfully.")

    except Exception as e:
        picam2 = None
        camera_available = False
        print(f"Camera not available: {e}")


setup_camera()


def get_soil_raw():
    try:
        result = get_soil_data(10)
        if not result:
            return None

        timestamps, raw, percent = result

        if not timestamps or not raw:
            return None

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

    except Exception as e:
        print(f"Error generating raw soil graph: {e}")
        return None


def get_soil_percent():
    try:
        result = get_soil_data(10)
        if not result:
            return None

        timestamps, raw, percent = result

        if not timestamps or not percent:
            return None

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

    except Exception as e:
        print(f"Error generating percent soil graph: {e}")
        return None


def generate_frames():
    global picam2, camera_available

    if not camera_available or picam2 is None:
        return

    while True:
        try:
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

        except Exception as e:
            print(f"Error while generating frames: {e}")
            break


def take_picture():
    global picam2, camera_available

    if not camera_available or picam2 is None:
        return None

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.jpg"
        filepath = os.path.join("static", "img", filename)

        picam2.capture_file(filepath)
        insert_image(filename)

        return filename

    except Exception as e:
        print(f"Error taking picture: {e}")
        return None


@app.route("/")
def home():
    latest_image = get_latest_image()
    return render_template("index.html", latest_image=latest_image)


@app.route("/soil")
def soil():
    soil_raw = get_soil_raw()
    soil_percent = get_soil_percent()
    return render_template("soil.html", soil_raw=soil_raw, soil_percent=soil_percent)


@app.route("/live")
def live():
    latest_image = get_latest_image()
    return render_template("live.html", latest_image=latest_image)


@app.route("/gallery")
def gallery():
    images = get_images(10)
    return render_template("gallery.html", images=images)


@app.route("/take_pic")
def take_picture_route():
    filename = take_picture()

    if filename:
        return jsonify({
            "status": "ok",
            "filename": filename,
            "image_url": f"/static/img/{filename}"
        })

    return jsonify({
        "status": "error",
        "message": "Camera is not available"
    }), 503


@app.route("/camera_feed")
def camera_feed():
    if not camera_available:
        return "Camera not available", 503

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@atexit.register
def cleanup():
    try:
        if picam2:
            picam2.stop()
    except Exception:
        pass


app.run(debug=True)