# Flask config
UPLOAD_FOLDER = '/home/qdl/Desktop/video-stega-stamp/video'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'flv'}
MAX_CONTENT_LENGTH = 50 * 1000 * 1000

# file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# model
MODEL_PATH = '/home/qdl/Desktop/video-stega-stamp/model/stegastamp_pretrained'

