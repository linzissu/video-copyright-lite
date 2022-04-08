from flask import Flask, flash, request, redirect, url_for, send_from_directory
import mapper.bch as bch
import os
from mapper.Stega import Stegastamp
from werkzeug.utils import secure_filename
from config import *


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

app.stega = Stegastamp(MODEL_PATH)

@app.route("/api/bch/encode",methods=['GET'])
def bch_encode():
    secret = request.args.get('secret')
    try:
        res = bch.bch_encode(secret)
    except:
        print('encode error!')
        return {'secret': 'error'}
    else:
        print('encode sucess')
        return {'secret': res}


@app.route("/api/bch/decode", methods=['POST'])
def bch_decode():
    code = request.json['code']
    try:
        res = bch.bch_decode(code)
    except:
        print('decode error!')
        return {'secret': 'error'}
    else:
        print('decode sucess')
        return {'secret': res}


@app.route('/api/file/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {'res': 'None'}

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return {'res': 'None'}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'res': filename}


@app.route('/api/stega/encode', methods=['GET'])
def encode():
    secret = request.args.get('secret')
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('name'))
    try:
        res = app.stega.encode(secret, video_path)
    except:
        print('error')
        return {'res': 'error'}
    else:
        return {'res': res}


@app.route('/api/stega/decode', methods=['GET'])
def decode():
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('name'))
    try:
        res = app.stega.decode(video_path)
    except:
        print('error')
        return {'res': 'error'}
    else:
        return {'res': res}


@app.route('/api/file/download', methods=['GET'])
def download_file():
    name = request.args.get('name')
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route('/test', methods=['GET'])
def test():
    res = app.stega.encode('secretsecretsecretsecretsecretsecretsecretsecret', './video/test.mp4')
    res = app.stega.decode('./video/test.mp4')
    return {'res': res}


if __name__ == '__main__':
    app.run(port='8888', host='0.0.0.0')
    app.run()