from flask import Flask, render_template, request
from PIL import Image, ImageOps
from pix2tex.cli import LatexOCR
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = LatexOCR()

@app.route('/', methods=['GET', 'POST'])
def index():
    latex_code = None
    image_path = None

    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            filename = image_file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)

            file_ext = filename.rsplit('.', 1)[1].lower()

            # 🧠 Use raw image for PNGs, preprocess JPEGs
            image = Image.open(filepath)
            if file_ext in ['jpg', 'jpeg']:
                image = image.convert('L')  # grayscale
                image = ImageOps.autocontrast(image)
                image = image.resize((1000, 500))

            latex_code = model(image)
            image_path = filepath

    return render_template('index.html', latex_code=latex_code, image_path=image_path)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
