# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Perusahaan Edutech saat ini menghadapi tantangan besar dalam mempertahankan mahasiswa hingga lulus. Tingginya angka mahasiswa yang memutuskan untuk tidak melanjutkan studi (dropout) berdampak pada pendapatan perusahaan dan efektivitas program pendidikan yang ditawarkan. Dengan memanfaatkan data historis mahasiswa, perusahaan ingin membangun sistem yang mampu mendeteksi potensi dropout lebih dini untuk melakukan tindakan preventif.

### Permasalahan Bisnis
- Tingginya tingkat dropout yang mencapai persentase signifikan sehingga mengganggu stabilitas operasional.
- Kurangnya sistem peringatan dini (early warning system) yang dapat mengidentifikasi mahasiswa bermasalah secara otomatis.
- Kesulitan dalam memetakan faktor-faktor utama (seperti performa akademik dan kondisi finansial) yang paling mempengaruhi keputusan mahasiswa untuk berhenti kuliah.

### Cakupan Proyek
1. **Business & Data Understanding:** Memahami latar belakang masalah dan struktur dataset mahasiswa yang tersedia.
2. **Data Cleaning & Preprocessing:** Menangani data duplikat, memastikan tidak ada nilai hilang yang mengganggu, serta menyaring data untuk fokus pada klasifikasi status 'Graduate' dan 'Dropout'.
3. **Exploratory Data Analysis (EDA):** Melakukan analisis mendalam untuk menemukan pola hubungan antara variabel akademik, demografi, dan status ekonomi terhadap kelulusan.
4. **Feature Engineering:** Menyiapkan fitur-fitur relevan untuk digunakan dalam proses pemodelan machine learning.
5. **Machine Learning Modeling:** Membangun model klasifikasi menggunakan algoritma **Random Forest Classifier** untuk memprediksi risiko dropout.
6. **Model Evaluation:** Menguji performa model menggunakan metrik Accuracy, Precision, Recall, dan F1-Score.
7. **Prototype Development:** Membangun aplikasi web menggunakan **Streamlit** untuk mempermudah akses prediksi bagi tim akademik.
8. **Business Dashboarding:** Membuat dashboard interaktif di **Looker Studio** untuk pemantauan data secara makro bagi manajemen.

### Persiapan

Sumber data: [data.csv](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/refs/heads/main/students_performance/data.csv)


Setup environment:
```bash
# 1. Membuat virtual environment
python -m venv venv

# 2. Mengaktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Menginstal library yang dibutuhkan
pip install -r requirements.txt
```

## Business Dashboard
Business Dashboard ini dirancang menggunakan Looker Studio sebagai alat pantau bagi manajemen untuk melihat tren retensi mahasiswa berdasarkan data historis yang sudah diproses.

### Komponen Visualisasi Utama:
- **Scorecards:** Ringkasan metrik utama mencakup Total Mahasiswa (3.630), Jumlah Graduate (Hijau), dan Jumlah Dropout (Merah).
- **Status Mahasiswa (Pie Chart):** Menunjukkan proporsi kelulusan vs dropout secara keseluruhan.
- **Analisis Beasiswa & Finansial (Stacked Bar):** Visualisasi korelasi antara penerimaan beasiswa dan status tunggakan biaya (debtor) terhadap kemungkinan dropout.
- **Performa Akademik (Column Chart):** Perbandingan rata-rata nilai semester 1 dan semester 2 yang menyoroti penurunan performa pada mahasiswa dropout.
- **Distribusi Usia (Column Chart):** Memetakan risiko dropout berdasarkan rentang usia mahasiswa saat mulai mendaftar.
- **Interactive Filters:** Filter berdasarkan Jenis Kelamin dan Beasiswa untuk analisis data yang lebih spesifik.

🔗 **Link Dashboard:** [Students Dashboard](https://datastudio.google.com/reporting/2ae32d60-cf65-4242-98b0-2ae5a04cd2c5)

## Menjalankan Sistem Machine Learning
Proyek ini menyertakan prototipe sistem prediksi berbasis web menggunakan **Streamlit**. Sistem ini memungkinkan pengguna memasukkan data mahasiswa dan mendapatkan hasil prediksi secara instan.

**Cara menjalankan prototype:**
1. Pastikan virtual environment aktif dan library di `requirements.txt` sudah terinstal.
2. Jalankan perintah berikut di terminal:
   ```bash
   streamlit run app.py
   ```
3. Buka browser di alamat `http://localhost:8501`.
4. Masukkan parameter data mahasiswa pada input yang disediakan untuk melihat hasil prediksi (**Graduate** atau **Dropout**).

**Link Prototype:** [edutech-corporate](https://edutech-corporate.streamlit.app/)

## Conclusion
Berdasarkan hasil analisis dan pemodelan, dapat disimpulkan bahwa penurunan performa akademik di semester kedua merupakan indikator terkuat mahasiswa akan dropout. Selain itu, kondisi finansial (debtor) memiliki pengaruh besar, di mana mahasiswa dengan tunggakan biaya memiliki risiko berhenti kuliah jauh lebih tinggi. Beasiswa terbukti menjadi faktor pendukung utama yang menjaga tingkat kelulusan tetap tinggi.

### Rekomendasi Action Items
- **Monitoring Penurunan Nilai:** Sistem melakukan komparasi otomatis antara Semester 1 dan Semester 2.
- **Pemberian Skema Keringanan Biaya:** Berdasarkan status finansial, jika mahasiswa terdeteksi sebagai 'Debtor' atau belum melunasi biaya kuliah, sistem merekomendasikan opsi cicilan atau bantuan dana darurat.
- **Automasi Prediksi:** Mengintegrasikan model machine learning ini ke dalam portal akademik sebagai sistem deteksi dini bagi dosen pembimbing akademik.
- **Optimasi & Peninjauan Beasiswa:** Bagi mahasiswa berisiko dropout yang belum menerima beasiswa, sistem memberikan saran peninjauan kelayakan bantuan dana untuk meningkatkan retensi.
- **Automasi Prediksi:** Mengintegrasikan model machine learning ini ke dalam portal akademik sebagai sistem deteksi dini (Early Warning System) bagi dosen pembimbing akademik.