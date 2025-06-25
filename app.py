from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
import gdown
from utils.segmentation import load_model, get_segmentation_mask
from utils.preprocessing import apply_mask, replace_background

app = Flask(__name__)

# Gunakan model U2NETP (versi kecil, sekitar 4MB)
model_path = "model/u2netp.pth"
if not os.path.exists(model_path):
    url = "https://drive.google.com/uc?id=1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy"  # U2NETP
    os.makedirs("model", exist_ok=True)
    gdown.download(url, model_path, quiet=False)

model = load_model(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    bg_color = request.form.get('color', 'white')
    bg_file = request.files.get('background')

    size = request.form.get('size', '3x4')
    if size == 'custom':
        try:
            width = float(request.form.get('custom_width', 3))
            height = float(request.form.get('custom_height', 4))
        except (ValueError, TypeError):
            width, height = 3, 4
    else:
        try:
            parts = size.split('x')
            width = float(parts[0])
            height = float(parts[1])
        except:
            width, height = 3, 4
    size_cm = (width, height)

    image = Image.open(file).convert("RGB")
    mask = get_segmentation_mask(image, model)
    feather_radius = max(1, int(min(image.size) * 0.005))
    cutout = apply_mask(image, mask, feather_radius=feather_radius)

    if bg_file and bg_file.filename != '':
        bg_image = Image.open(bg_file).convert("RGB")
        final_image = replace_background(cutout, bg_image, size_cm)
    else:
        final_image = replace_background(cutout, bg_color, size_cm)

    buf = io.BytesIO()
    final_image.save(buf, format='JPEG')
    buf.seek(0)
    return send_file(buf, mimetype='image/jpeg', as_attachment=True, download_name='pasfoto.jpg')

if __name__ == "__main__":
    app.run(debug=True)