# 🕵️ Removedor de Metadados EXIF

Ferramenta web feita em **Flask** para inspecionar e remover metadados de imagens `.jpg/.jpeg`.
Com ela você pode:

* 📤 Fazer upload de imagens
* 🔎 Visualizar metadados EXIF (dados ocultos da foto)
* 🧹 Remover metadados preservando a orientação da imagem

---

## 🚀 Tecnologias

* [Python 3.10](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Pillow (PIL)](https://pillow.readthedocs.io/)
* [piexif](https://pypi.org/project/piexif/)
* HTML, CSS e JavaScript

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/removedor-metadados.git
cd removedor-metadados
```

Crie o ambiente com **conda**:

```bash
conda env create -f environment.yml
conda activate removedor-metadados
```

---

## ▶️ Uso

Inicie o servidor Flask:

```bash
python app.py
```

Abra no navegador:
👉 [http://localhost:5000](http://localhost:5000)

1. Selecione uma imagem `.jpg` ou `.jpeg`
2. Veja os metadados listados na tela
3. Clique em **Remover** para gerar a versão limpa

---

## 📂 Estrutura de pastas

```
.
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── uploads/        # imagens enviadas
├── thumbnails/     # miniaturas extraídas
└── output/         # imagens sem metadados
```

---

## ⚠️ Observações

* Apenas arquivos `.jpg/.jpeg` são aceitos.
* Os metadados removidos incluem EXIF, GPS e outros dados sensíveis.
* O valor de **orientação** da foto é preservado.

---

## Tasks

* [x] Realizar tratamento de erros

---
## Materiais Utilizados

<a target="_blank" href="https://icons8.com/icon/p3miLroKw4iR/magnifying-glass-tilted-left">emoji de lupa inclinada para a esquerda</a> ícone por <a target="_blank" href="https://icons8.com">Icons8</a>