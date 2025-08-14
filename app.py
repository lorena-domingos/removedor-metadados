from flask import Flask, jsonify, render_template, request
from PIL import Image
import piexif
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def image_process():
    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'filename': file.filename})

@app.route('/api/metadata', methods=['GET'])
def api():
    filename = request.args.get("filename")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    image = Image.open(file_path)
    exif_data = piexif.load(image.info['exif'])

    tag_list = []

    if exif_data.get('thumbnail'):
        with open('thumbnail.jpg', 'wb+') as tb:
            tb.write(exif_data['thumbnail'])

    for tag_name, info_dict in exif_data.items():
        if tag_name == 'thumbnail' or info_dict is None:
            continue
        for tag, values in info_dict.items():
            if isinstance(values, bytes):
                try:
                    values = values.decode('utf-8')
                except UnicodeDecodeError:
                    values = values.decode('latin1')
            try:
                tags = piexif.TAGS[tag_name][tag]['name']
            except KeyError:
                tags = f"Tag não reconhecida: {tag}"
            except Exception as e:
                tags = f"Erro ao ler tag {tag}: {e}"
            tag_list.append({'tags': tags, 'values': values})
    return jsonify(tags=tag_list)

if __name__ == '__main__':
    app.run(debug=True)