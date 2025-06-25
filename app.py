from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io
import urllib.request
from utils.segmentation import load_model, get_segmentation_mask
from utils.preprocessing import apply_mask, replace_background

app = Flask(__name__)

# Download model jika belum ada
model_path = "model/u2netp.pth"
if not os.path.exists(model_path):
    os.makedirs("model", exist_ok=True)
    print("Downloading model...")
    url = "https://huggingface.co/someone/u2netp/resolve/main/u2netp.pth"  # Ganti URL dengan yang benar
    urllib.request.urlretrieve(url, model_path)

# Load model
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
