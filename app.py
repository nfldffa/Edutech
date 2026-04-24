import streamlit as st
import pandas as pd
import joblib

# 1. SETTING PAGE & LOAD MODEL
st.set_page_config(page_title="Student Tracker", page_icon="🎓")

@st.cache_resource
def load_model():
    return joblib.load('model/model_rf_deploy.pkl')

model = load_model()

# 2. UI HEADER
st.title("🎓 Prediksi Kelulusan Mahasiswa")
st.markdown("---")

# 3. INPUT FORM
with st.form("prediction_form"):
    st.subheader("📝 Data Akademik & Profil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        s1_grade = st.number_input("IPK Semester 1 (0-20)", 0.0, 20.0, 12.0)
        s1_approved = st.number_input("SKS Lulus Semester 1", 0, 30, 10)
        s2_grade = st.number_input("IPK Semester 2 (0-20)", 0.0, 20.0, 12.0)
        s2_approved = st.number_input("SKS Lulus Semester 2", 0, 30, 10)
        age = st.slider("Usia Saat Mendaftar", 15, 60, 20)

    with col2:
        gender = st.selectbox("Jenis Kelamin", ["Wanita", "Pria"])
        scholarship = st.selectbox("Penerima Beasiswa?", ["Ya", "Tidak"])
        tuition = st.selectbox("Biaya Kuliah Lunas?", ["Ya", "Tidak"])
        debtor = st.selectbox("Punya Hutang/Tunggakan?", ["Ya", "Tidak"])
        app_mode = st.number_input("Mode Aplikasi (Kode)", 1, 100, 1)

    # Submit Button
    submit = st.form_submit_button("Cek Hasil Prediksi", use_container_width=True)

# 4. PREDICTION LOGIC
if submit:
    # Mapping sederhana
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

    # 5. DISPLAY RESULT
    st.markdown("### 📊 Hasil Analisis:")
    if prediction == 1:
        st.error("⚠️ **Hasil: Berisiko Dropout**")
        st.info("Saran: Mahasiswa memerlukan pendampingan akademik atau bantuan finansial lebih lanjut.")
    else:
        st.success("✅ **Hasil: Berpotensi Lulus (Graduate)**")
        st.info("Saran: Pertahankan performa akademik dan jaga kestabilan finansial.")

# 6. FOOTER
st.sidebar.caption("Created by Naufal Daffa Erlangga")