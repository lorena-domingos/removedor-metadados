from flask import Flask, jsonify, render_template, request
from PIL import Image
import piexif
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
THUMBNAIL_FOLDER = 'thumbnails'
CLEANED_IMAGE = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)
os.makedirs(CLEANED_IMAGE, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def image_validation():
    image = request.files['image']
    # print(image)
    image_str = image.filename
    image_name, image_ext = os.path.splitext(image_str)
    extensions_allowed = ['jpg', 'jpeg']
    # print(image_name)
    # print(image_ext)
    if image_ext[1:].lower() in extensions_allowed:
        return image
    else:
        return None

@app.route('/upload', methods=['POST'])
def image_process():
    file = image_validation()
    if file is None:
        return jsonify({'error': 'Nenhum arquivo encontrada'}), 400

    image = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, image)

    try:
        file.save(file_path)
    except PermissionError:
        return jsonify({'error': 'Sem permissão para criar o arquivo'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro inesperado, {e}'}), 500

    return jsonify({'filename': image})

@app.route('/api/metadata', methods=['GET'])
def api():
    filename = request.args.get("filename")
    if not filename:
        print(f'Nenhuma imagem para processar')

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    exif_data = piexif.load(file_path)

    tag_list = []

    if exif_data.get('thumbnail'):
        with open(f'{THUMBNAIL_FOLDER}/thumbnail.jpg', 'wb+') as tb:
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

@app.route('/remove/metadata', methods=['POST'])
def remove_metadata():
    filename = request.form.get('filename')
    if not filename:
        print("Imagem não carreggada")
    
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        exif_dict = piexif.load(input_path)
        orientation_value = exif_dict["0th"].get(piexif.ImageIFD.Orientation)
        new_exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        
        if orientation_value is not None:
            new_exif["0th"][piexif.ImageIFD.Orientation] = orientation_value
            
        output_path = os.path.join(CLEANED_IMAGE, filename)
        
        image = Image.open(input_path)
        exif_bytes = piexif.dump(new_exif)
        image.save(output_path, exif=exif_bytes)
        
        return jsonify({'status': 'success', 'message': 'Metadados removidos!', 'output_file': filename}), 200
    
    except Exception as e:
        print(f"Erro ao tentar remover metadados: {e}")
        return jsonify({'status': 'error', 'message': 'Falha ao processar a imagem.'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)