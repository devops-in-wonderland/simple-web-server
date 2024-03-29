from flask import Flask, render_template, request, Response
import os
import time

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024
app.config['UPLOAD_PATH'] = 'uploads'


def mkdir_if_does_not_exists(dir: str):
    if not os.path.isdir(dir):
        os.mkdir(dir)


mkdir_if_does_not_exists(app.config['UPLOAD_PATH'])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename == 'index.html':

        timestamp_text = str(int(time.time() * 1e3))

        new_file_dir = os.path.join(
            app.config['UPLOAD_PATH'], timestamp_text)

        mkdir_if_does_not_exists(new_file_dir)

        new_file_path = os.path.join(new_file_dir, uploaded_file.filename)

        uploaded_file.save(new_file_path)

        return timestamp_text
    else:
        return Response(status=405)

@app.route('/test-results/<folder>')
def get_results(folder):
    try:
        with open(f'{app.config['UPLOAD_PATH']}/{str(folder)}/index.html') as f:
            content = f.read()
    except:
        return "Test report not found."
    return content


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
