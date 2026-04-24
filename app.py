import streamlit as st
import pandas as pd
import joblib
import time

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Edutech Corporate System",
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
    
    st.divider()
    with st.expander("📖 Panduan Singkat"):
        st.write("""
        1. Masukkan data profil mahasiswa.
        2. Klik **Run Analysis**.
        3. Lihat hasil prediksi dan rekomendasi tindakan.
        """)

# 4. MAIN CONTENT
st.title("🎓 Edutech Corporate Diagnostic System")
st.write("Sistem Pendeteksi Risiko Kelulusan Mahasiswa.")

tab1, tab2 = st.tabs(["🔍 Predictor", "ℹ️ Informasi Fitur"])

with tab1:
    st.subheader("Data Input")
    
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📝 Performa Akademik**")
            s1_grade = st.number_input("IPK Semester 1 (0-20)", 0.0, 20.0, 12.0)
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

        submit_button = st.form_submit_button("🚀 Run Analysis", use_container_width=True)

    if submit_button:
        with st.spinner('Sedang memproses data...'):
            time.sleep(1)
            
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
            prediction = model.predict(df_input)[0]
            probability = model.predict_proba(df_input)[0]
            
            # BAGIAN HASIL & ANALISIS DINAMIS
            st.divider()
            res_col1, res_col2 = st.columns([1, 1])
            
            if prediction == 1:
                with res_col1:
                    st.error("### 🚨 Hasil: DROPOUT")
                    conf_score = probability[1]
                with res_col2:
                    st.write(f"**Tingkat Risiko:** {conf_score*100:.2f}%")
                    st.progress(conf_score)
                
                st.markdown("### 📋 Rekomendasi Action Items")
                st.write("Berdasarkan hasil diagnosa dan perbandingan performa:")

                # 1. Monitoring Performa Akademik (S1 vs S2)
                if s1_grade > s2_grade or s1_approved > s2_approved:
                    st.warning("""
                    **1. Monitoring Penurunan Nilai:** Mengaktifkan program pendampingan (mentoring) khusus bagi mahasiswa yang nilai atau SKS semester 2-nya turun dibanding semester 1.
                    """)
                elif s1_grade < s2_grade or s1_approved < s2_approved:
                    st.success("""
                    **1. Apresiasi & Konsistensi:** Mahasiswa menunjukkan tren peningkatan performa di semester 2. Dorong untuk mempertahankan konsistensi agar peluang lulus tepat waktu tetap terjaga.
                    """)
                else:
                    st.info("**1. Pemantauan Rutin:** Performa akademik mahasiswa stabil. Tetap pantau progresnya agar tidak mengalami kejenuhan.")

                # 2. Skema Keringanan Biaya (Finansial - Debtor/Tuition)
                if debtor == "Ya" or tuition == "Tidak":
                    st.warning("""
                    **2. Pemberian Skema Keringanan Biaya:** Memberikan opsi cicilan atau bantuan darurat bagi mahasiswa yang terdeteksi memiliki masalah finansial (Debtor/Tunggakan) agar tidak terpaksa putus kuliah.
                    """)
                
                # 3. Optimasi Beasiswa (Finansial - Scholarship)
                if scholarship == "Tidak" and prediction == 1:
                    st.info("""
                    **3. Peninjauan Beasiswa:** Mahasiswa berisiko ini tidak memiliki beasiswa. Perlu dicek apakah layak mendapatkan bantuan dana untuk meningkatkan retensi.
                    """)
                
                # 4. Automasi & Integrasi (Sistem)
                st.info("""
                **4. Automasi Prediksi:** Mengintegrasikan model machine learning ini ke dalam portal akademik sebagai sistem deteksi dini bagi dosen pembimbing akademik.
                """)

            else:
                with res_col1:
                    st.success("### ✅ Hasil: GRADUATE")
                    conf_score = probability[0]
                with res_col2:
                    st.write(f"**Tingkat Keyakinan:** {conf_score*100:.2f}%")
                    st.progress(conf_score)

                st.markdown("### 📋 Rekomendasi Action Items")
                st.write("Mahasiswa terpantau aman, berikut langkah pemeliharaan:")
                st.success("1. **Apresiasi Performa:** Pertahankan konsistensi nilai untuk persiapan kelulusan tepat waktu.")
                st.info("2. **Program Peer-Mentoring:** Mahasiswa ini bisa dijadikan mentor bagi mahasiswa lain yang berisiko.")

with tab2:
    st.subheader("Detail Fitur")
    st.write("""
    Model ini memprediksi status mahasiswa berdasarkan 10 fitur utama yang paling berpengaruh:
    - **Akademik:** Nilai IPK dan jumlah SKS yang lulus di semester 1 dan 2.
    - **Finansial:** Status beasiswa, pelunasan uang kuliah, dan tunggakan utang.
    - **Demografi:** Usia saat mendaftar dan jenis kelamin.
    """)

# FOOTER
st.divider()
st.caption("© 2026 Edutech Corporate System | Naufal Daffa Erlangga")