from PIL import Image
import piexif

image = Image.open('imagem_exemplo.jpg')
exif_data = piexif.load(image.info['exif'])

if exif_data.get('thumbnail'):
    with open('thumbnail.jpg', 'wb+') as tb:
        tb.write(exif_data['thumbnail'])

for tag_name, info_dict in exif_data.items():
    if tag_name == 'thumbnail' or info_dict is None:
        continue
    for tag, values in info_dict.items():
        try:
            tags = piexif.TAGS[tag_name][tag]['name']
        except KeyError:
            tags = f"Tag não reconhecida: {tag}"
        except Exception as e:
            tags = f"Erro ao ler tag {tag}: {e}"
        print(f'{tags}: {values}')

# print(exif_data)
