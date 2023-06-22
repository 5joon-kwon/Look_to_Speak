from flask import *
from eye_tracking import track
import os 
import cv2

UPLOAD_FOLDER = 'C:\\Users\\johng\\Desktop\\'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload/", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('fail')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('saved file')
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            res = track(img, 120)
            return jsonify(res)
    return ''

# @app.route('/get_direction/<filename>')
# def get_direction(filename):
#     img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     res = track(img)
#     return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)