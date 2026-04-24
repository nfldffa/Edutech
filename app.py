import streamlit as st
import pandas as pd
import joblib
import time

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Edutech Corporate",
    page_icon="🎓",
    layout="wide"
)

# 2. LOAD MODEL
@st.cache_resource
def load_model():
    return joblib.load('model/model_rf_deploy.pkl')

model = load_model()

# 3. SIDEBAR
with st.sidebar:
    st.title("📌 Project Info")
    st.write("""
    Aplikasi ini dirancang untuk memprediksi potensi kelulusan mahasiswa berdasarkan indikator akademik dan finansial.
    """)
    
    st.divider()
    
    st.markdown("### 👨‍💻 Developer")
    st.write("**Naufal Daffa Erlangga**")
    st.caption("Data Science Student & Developer")
    
    st.divider()
    
    with st.expander("📖 Panduan Singkat"):
        st.write("""
        1. Pilih tab **Predictor**.
        2. Masukkan data sesuai profil mahasiswa.
        3. Klik **Run Analysis**.
        4. Hasil dan tingkat keyakinan model akan muncul di bawah.
        """)
    
    st.info("Sistem ini menggunakan algoritma Random Forest dengan akurasi yang telah diuji.")

# 4. MAIN CONTENT
st.title("🎓 Student Diagnostic System")
st.write("Gunakan sistem ini untuk mendeteksi dini risiko dropout mahasiswa.")

# Menggunakan Tabs untuk Navigasi
tab1, tab2 = st.tabs(["🔍 Predictor", "ℹ️ Informasi Fitur"])

with tab1:
    st.subheader("Data Input")
    
    # Bungkus dalam form biar nggak auto-reload tiap ngetik
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📝 Performa Akademik**")
            s1_grade = st.number_input("IPK Semester 1 (0-20)", 0.0, 20.0, 12.0, help="Skala nilai 0 sampai 20")
            s1_approved = st.number_input("SKS Lulus Sem 1", 0, 30, 15)
            s2_grade = st.number_input("IPK Semester 2 (0-20)", 0.0, 20.0, 12.0)
            s2_approved = st.number_input("SKS Lulus Sem 2", 0, 30, 15)
            app_mode = st.number_input("Application Mode (Code)", 1, 100, 1)

        with col2:
            st.write("**💰 Finansial & Demografi**")
            scholarship = st.selectbox("Penerima Beasiswa", ["Ya", "Tidak"])
            tuition = st.selectbox("Biaya Kuliah Lunas?", ["Ya", "Tidak"])
            debtor = st.selectbox("Ada Tunggakan Utang?", ["Ya", "Tidak"])
            gender = st.selectbox("Jenis Kelamin", ["Wanita", "Pria"])
            age = st.slider("Usia Saat Daftar", 15, 60, 20)

        # Tombol Submit
        submit_button = st.form_submit_button("🚀 Run Analysis", use_container_width=True)

    # Logika Prediksi setelah tombol diklik
    if submit_button:
        with st.spinner('Sedang memproses data...'):
            time.sleep(1)
            
            # Mapping input ke format model
            input_data = {
                'Curricular_units_2nd_sem_approved': s2_approved,
                'Curricular_units_2nd_sem_grade': s2_grade,
                'Curricular_units_1st_sem_approved': s1_approved,
                'Curricular_units_1st_sem_grade': s1_grade,
                'Tuition_fees_up_to_date': 1 if tuition == "Ya" else 0,
                'Scholarship_holder': 1 if scholarship == "Ya" else 0,
                'Age_at_enrollment': age,
                'Debtor': 1 if debtor == "Ya" else 0,
                'Gender': 1 if gender == "Pria" else 0,
                'Application_mode': app_mode
            }

            df_input = pd.DataFrame([input_data])
            
            # Prediksi
            prediction = model.predict(df_input)[0]
            # Ambil probabilitas
            probability = model.predict_proba(df_input)[0]
            
            st.divider()
            
            # Tampilan Hasil
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                if prediction == 1:
                    st.error("### 🚨 Hasil: DROPOUT")
                    conf_score = probability[1]
                else:
                    st.success("### ✅ Hasil: GRADUATE")
                    conf_score = probability[0]
            
            with res_col2:
                st.write(f"**Tingkat Keyakinan (Confidence):** {conf_score*100:.2f}%")
                st.progress(conf_score)

            # Pesan Tambahan
            if prediction == 1:
                st.warning("Mahasiswa terdeteksi berisiko tinggi. Disarankan pihak akademik melakukan konsultasi personal.")
            else:
                st.info("Mahasiswa menunjukkan performa yang baik. Dorong untuk terus mempertahankan prestasinya.")

with tab2:
    st.subheader("Detail Fitur")
    st.write("""
    Model ini memprediksi status mahasiswa berdasarkan 10 fitur utama yang paling berpengaruh:
    - **Akademik:** Nilai IPK dan jumlah SKS yang lulus di semester 1 dan 2.
    - **Finansial:** Status beasiswa, pelunasan uang kuliah, dan tunggakan utang.
    - **Demografi:** Usia saat mendaftar dan jenis kelamin.
    - **Administrasi:** Mode aplikasi saat masuk ke institusi.
    """)
    st.write("Seluruh data diproses secara anonim untuk keperluan analisis prediksi.")

# FOOTER
st.divider()
st.caption("© 2026 Edutech Corporate System | Created by Naufal Daffa Erlangga")