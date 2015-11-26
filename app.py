import os
from flask import Flask, render_template, Response, request, url_for, redirect
from werkzeug import secure_filename
import sys
import random
from server.heart_rate_imposer import HeartRateImposer
from keras.models import model_from_json

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['avi'])

app.config['UPLOAD_FOLDER'] = '/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

video_file = sys.argv[1]
opencv_path = sys.argv[2]

def gen_http_frame(gen_frames):
    for frame in gen_frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route("/upload", methods=['POST'])
def upload():

	file = request.files['file']
	if file and allowed_file(file.filename):
        	filename = secure_filename(file.filename)
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    		hri = HeartRateImposer(url_for('uploaded_file', filename=filename), opencv_path)
    		return Response(gen_http_frame(hri.gen_heartrate_frames),
                    		mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# @app.route('/video/<youtube_extension>')
# def stream(youtube_extension):
#     url = 'www.youtube.com/' + youtube_extension
#     hri = HeartRateImposer(video_file, opencv_path)
#     return Response(gen_http_frame(hri.gen_heartrate_frames),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def stream():
    hri = HeartRateImposer(video_file, opencv_path)
    return Response(gen_http_frame(hri.gen_heartrate_frames),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
