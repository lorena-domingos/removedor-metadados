from flask import Flask, jsonify, render_template
from PIL import Image
import piexif

app = Flask(__name__)

@app.route('/api/metadata', methods=['GET'])
def api():
    image = Image.open('imagem_exemplo.jpg')
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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)