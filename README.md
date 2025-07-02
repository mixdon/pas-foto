## Pas Foto Otomatis - Background Remover

Proyek ini membangun sistem otomatis berbasis Computer Vision untuk menghapus dan mengganti latar belakang pas foto secara akurat dan efisien.

### Fitur:
1. Menghapus latar belakang asli dari pas foto menggunakan model segmentasi U²-Net.
2. Mengganti latar belakang dengan:
   - Warna solid (biru, merah, putih, dll)
   - Gambar khusus yang diunggah pengguna
3. Menyesuaikan ukuran foto sesuai standar (2x3, 3x4, 4x6 cm) atau ukuran custom.
4. Membuat hasil masking lebih halus dengan feathering otomatis di tepi objek.

### Teknologi:
- U²-Net (segmentasi citra)
- PyTorch (model dan inferensi)
- Pillow (pengolahan gambar)
- Flask (backend aplikasi)

Sistem ini memudahkan pembuatan pas foto formal untuk keperluan seperti KTP, CV, ijazah, paspor, dan kebutuhan resmi lainnya.

##How to Run Project
Clone this repository.

Install the dependencies:

``pip install -r requirements.txt
Run the project:

``python app.py
