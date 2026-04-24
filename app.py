import streamlit as st
import pandas as pd
import joblib

# CONFIG & LOAD
st.set_page_config(page_title="Student Success Tracker", page_icon="🎓")

def load_model():
    return joblib.load('model/model_rf_deploy.pkl')

model = load_model()

# UI HEADER
st.title("🎓 Student Success Predictor")
st.caption("Predicting student outcomes based on academic and financial indicators.")

# SIDEBAR
with st.sidebar:
    st.header("Help & Info")
    st.info("""
    Isi data mahasiswa di samping kanan untuk mendapatkan prediksi.
    Model ini menggunakan 10 fitur utama yang paling berpengaruh terhadap kelulusan.
    """)
    st.divider()
    st.write("v1.0.0 | Created by [Nama Lu]")

# INPUT FORM
st.subheader("Student Profile")
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        s2_approved = st.number_input("SKS Lulus Sem 2", 0, 30, 5)
        s2_grade = st.number_input("IPK Sem 2", 0.0, 20.0, 12.0)
        s1_approved = st.number_input("SKS Lulus Sem 1", 0, 30, 5)
        s1_grade = st.number_input("IPK Sem 1", 0.0, 20.0, 12.0)
        app_mode = st.number_input("Application Mode (Code)", 1, 100, 1)

    with col2:
        age = st.number_input("Usia Saat Daftar", 15, 80, 20)
        tuition = st.radio("Uang Kuliah Lunas?", ["Ya", "Tidak"], horizontal=True)
        scholarship = st.radio("Penerima Beasiswa?", ["Ya", "Tidak"], horizontal=True)
        debtor = st.radio("Ada Tunggakan Utang?", ["Ya", "Tidak"], horizontal=True)
        gender = st.selectbox("Gender", ["Wanita", "Pria"])

# PREDICTION LOGIC
if st.button("Run Analysis", type="primary", use_container_width=True):
    # Mapping input ke format model
    data = {
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
    
    df_input = pd.DataFrame([data])
    prediction = model.predict(df_input)[0]
    
    st.divider()
    
    # Result Display
    if prediction == 1:
        st.error("### 🚨 Result: Potential Dropout")
        st.write("Mahasiswa ini masuk kategori berisiko tinggi. Disarankan untuk segera dilakukan pendampingan akademik.")
    else:
        st.success("### ✅ Result: Likely to Graduate")
        st.write("Performa mahasiswa terpantau stabil dan berpotensi besar untuk lulus tepat waktu.")