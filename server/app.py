import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename
 
app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['avi'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/upload", methods=['POST'])
def upload():

	file = request.files['file']
	if file and allowed_file(file.filename):
        	filename = secure_filename(file.filename)
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    		return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080)