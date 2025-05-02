import streamlit as st
import pandas as pd
import joblib
import mysql.connector
import hashlib
import time
import base64
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="Sistem Prediksi Komplikasi Hemodialisis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to add background image
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://png.pngtree.com/background/20210711/original/pngtree-geometric-gradient-creative-blood-donation-poster-background-material-picture-image_1127152.jpg");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
# Custom CSS for better styling
def add_custom_styling():
    st.markdown("""
    <style>
    /* Main background styling */
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
    }
    
    /* Header styling */
    h1 {
        color: #1E3A8A;
        text-align: center;
        padding: 20px 0;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #1E3A8A;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #4169E1;
        border: none;
    }
    
    /* Input field styling */
    div[data-baseweb="input"] {
        border-radius: 5px;
    }
    
    /* Sidebar styling - FIXED */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A;
        background-image: url('https://img.freepik.com/free-photo/medical-banner-with-doctor-working_23-2149611217.jpg');
        background-size: cover;
        background-position: center;
        color: white !important;
    }
    
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(30, 58, 138, 0.85); /* Semi-transparent blue overlay */
        z-index: -1;
    }
    
    [data-testid="stSidebar"] h1 {
        color: white !important;
        background-color: transparent;
    }
    
    [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    /* Make the radio text white */
    [data-testid="stSidebar"] .stRadio div {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio div:first-of-type {
        color: white !important;
    }
    
    /* Make the radio buttons bigger and more visible */
    [data-testid="stSidebar"] .stRadio label span {
        color: white !important;
        font-weight: bold;
        font-size: 18px !important;
        margin: 10px 0 !important;
    }
    
    /* Logo container in sidebar */
    .sidebar-logo {
        background-color: white;
        border-radius: 50%;
        padding: 10px;
        margin: 20px auto;
        width: 150px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Container styling */
    div.stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        padding: 25px;
        border-radius: 5px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Success message styling */
    div.stSuccess {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    
    /* Error message styling */
    div.stError {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    
    /* Info message styling */
    div.stInfo {
        background-color: #cce5ff;
        color: #004085;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #0d6efd;
    }
    
    /* Warning message styling */
    div.stWarning {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #ddd;
        font-size: 16px;
    }
    
    .dataframe th {
        background-color: #1E3A8A;
        color: white;
        text-align: left;
        padding: 12px;
    }
    
    .dataframe td {
        border: 1px solid #ddd;
        padding: 12px;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        margin-left: 10px;
    }

    /* Form container styling */
    .form-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Result container styling */
    .result-container {
        background-color: #e8f4ff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        border-left: 5px solid #1E3A8A;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
        border: 1px solid #e9ecef;
        border-bottom: none;
        padding: 10px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #1E3A8A;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply background image and custom styling
add_bg_from_url()
add_custom_styling()

# Load model
model = joblib.load('model_parameter5b.sav')

# Koneksi ke Database MySQL Online (Freedb)
def get_db_connection():
    return mysql.connector.connect(
        host="kopicast.web.id",
        user="kopicast_userrangga",
        password="Venusku123",
        database="kopicast_hemodialysis_db"
    )

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Simpan user baru
def register_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hash_password(password)))
    conn.commit()
    conn.close()
    return True

# Cek login
def check_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Simpan hasil prediksi ke database
def save_prediction(nama_pasien, jenis_kelamin, usia, sistolik, diastolik, 
                    hemoglobin, si_tibc, ureum, kreatinin, epo_3000, epo_2000, 
                    tron_sucrose, lama_hemodialisis, riwayat_penyakit_keluarga, 
                    riwayat_penyakit, prediksi, user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Konversi nilai boolean/string ke integer untuk database
    epo_3000_val = 1 if epo_3000 == 'ya' else 0
    epo_2000_val = 1 if epo_2000 == 'ya' else 0
    
    # Tanggal dan waktu prediksi
    tanggal_prediksi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # SQL untuk menyimpan hasil prediksi
    sql = """
    INSERT INTO prediksi_pasien (
        nama_pasien, jenis_kelamin, usia, sistolik, diastolik, 
        hemoglobin, si_tibc, ureum, kreatinin, epo_3000, epo_2000,
        tron_sucrose, lama_hemodialisis, riwayat_penyakit_keluarga,
        riwayat_penyakit, hasil_prediksi, user_email, tanggal_prediksi
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        nama_pasien, jenis_kelamin, usia, sistolik, diastolik, 
        hemoglobin, si_tibc, ureum, kreatinin, epo_3000_val, epo_2000_val, 
        tron_sucrose, lama_hemodialisis, riwayat_penyakit_keluarga, 
        riwayat_penyakit, prediksi, user_email, tanggal_prediksi
    )
    
    cursor.execute(sql, values)
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id

# Simpan hasil prediksi batch dari file
def save_batch_predictions(data, predictions, user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tanggal dan waktu prediksi
    tanggal_prediksi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Menambahkan kolom untuk total baris yang tersimpan
    saved_count = 0
    
    for i, row in data.iterrows():
        try:
            # Pastikan nama pasien ada
            nama_pasien = row.get('Nama_Pasien', f'Pasien File #{i+1}')
            
            # Konversi nilai EPO
            epo_3000_val = 1 if row['EPO_3000'] == 'ya' else 0
            epo_2000_val = 1 if row['EPO_2000'] == 'ya' else 0
            
            # SQL untuk menyimpan hasil prediksi
            sql = """
            INSERT INTO prediksi_pasien (
                nama_pasien, jenis_kelamin, usia, sistolik, diastolik, 
                hemoglobin, si_tibc, ureum, kreatinin, epo_3000, epo_2000,
                tron_sucrose, lama_hemodialisis, riwayat_penyakit_keluarga,
                riwayat_penyakit, hasil_prediksi, user_email, tanggal_prediksi
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                nama_pasien, row['Jenis_Kelamin'], row['usia'], row['Sistolik'], row['Diastolik'], 
                row['Hemoglobin'], row['SI-TIBC_(%)'], row['Ureum'], row['Kreatinin'], epo_3000_val, epo_2000_val, 
                row['TRON_SUCROSE'], row['lama_hemodialisis(bulan)'], row['Riwayat_penyakit_keluarga'], 
                row['Riwayat_penyakit'], predictions[i], user_email, tanggal_prediksi
            )
            
            cursor.execute(sql, values)
            saved_count += 1
        except Exception as e:
            st.error(f"Error saat menyimpan data baris {i+1}: {str(e)}")
            continue
    
    conn.commit()
    conn.close()
    return saved_count

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Fungsi untuk mengubah halaman
def change_page(page):
    st.session_state['page'] = page
    st.rerun()

# Logo dan judul aplikasi
def display_app_header():
    st.markdown("""
    <div class="logo-container">
        <span style="font-size: 40px;">🏥</span>
        <span class="logo-text">SISTEM PREDIKSI KOMPLIKASI HEMODIALISIS</span>
    </div>
    """, unsafe_allow_html=True)

# Halaman login
def login_page():
    display_app_header()
    
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 20px;">Login</h2>
    """, unsafe_allow_html=True)
    
    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔒 Password", type="password", key="login_password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", key="login_button"):
            if check_login(email, password):
                st.session_state['authenticated'] = True
                st.session_state['user'] = email
                st.session_state['page'] = 'main'
                st.success("✅ Login berhasil!")
                st.rerun()
            else:
                st.error("❌ Email atau password salah")
    
    with col2:
        if st.button("🆕 Buat Akun Baru", key="create_account_button"):
            st.session_state['page'] = 'register'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 0; width: 100%; background-color: #1E3A8A; padding: 10px; text-align: center; color: white;">
        © 2025 Sistem Prediksi Hemodialisis. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

# Halaman registrasi
def register_page():
    display_app_header()
    
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 20px;">Buat Akun Baru</h2>
    """, unsafe_allow_html=True)
    
    email = st.text_input("📧 Email", key="register_email")
    password = st.text_input("🔒 Password", type="password", key="register_password")
    confirm_password = st.text_input("🔁 Konfirmasi Password", type="password", key="confirm_password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Daftar", key="register_button"):
            if password == confirm_password:
                if register_user(email, password):
                    st.success("✅ Akun berhasil dibuat! Silakan login.")
                    st.session_state['page'] = 'login'
                    st.rerun()
                else:
                    st.error("❌ Email sudah terdaftar!")
            else:
                st.error("❌ Password tidak cocok!")
    
    with col2:
        if st.button("↩️ Kembali ke Login", key="back_to_login"):
            st.session_state['page'] = 'login'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 0; width: 100%; background-color: #1E3A8A; padding: 10px; text-align: center; color: white;">
        © 2025 Sistem Prediksi Hemodialisis. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

# Halaman utama setelah login
def main_page():
    with st.sidebar:
        # Use HTML for better visibility in sidebar with kidney image
        st.markdown("""
        <div style="text-align: center; position: relative; z-index: 10;">
            <div class="sidebar-logo">
                <img src="https://cdn-icons-png.flaticon.com/512/2297/2297894.png" width="110">
            </div>
            <h1 style="color: white; font-size: 24px; margin-top: 10px;">MENU</h1>
            <p style="color: white; font-size: 16px;">👤 Selamat datang, <b>{}</b></p>
        </div>
        <hr style="margin: 20px 0; border-color: rgba(255, 255, 255, 0.3);">
        """.format(st.session_state['user']), unsafe_allow_html=True)
        
        # Use custom radio with better visibility
        menu_option = st.radio(
            "",
            ["📊 Prediksi", "📋 Riwayat Prediksi", "🚪 Logout"],
            key="main_menu",
            label_visibility="collapsed"
        )
    
    if menu_option == "📊 Prediksi":
        prediction_page()
    elif menu_option == "📋 Riwayat Prediksi":
        prediction_history_page()
    elif menu_option == "🚪 Logout":
        st.session_state.clear()
        # Reinitialize session state
        st.session_state['page'] = 'login'
        st.session_state['authenticated'] = False
        st.rerun()

# Halaman riwayat prediksi
def prediction_history_page():
    display_app_header()
    
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 20px;">Riwayat Prediksi</h2>
    """, unsafe_allow_html=True)
    
    # Ambil data prediksi dari database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Filter berdasarkan email pengguna saat ini
    cursor.execute("""
    SELECT id, nama_pasien, jenis_kelamin, usia, hasil_prediksi, tanggal_prediksi 
    FROM prediksi_pasien 
    WHERE user_email = %s
    ORDER BY tanggal_prediksi DESC
    """, (st.session_state['user'],))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        st.info("Belum ada data prediksi. Silakan lakukan prediksi terlebih dahulu.")
    else:
        # Konversi ke DataFrame untuk tampilan yang lebih baik
        history_df = pd.DataFrame(results)
        
        # Format tanggal untuk tampilan yang lebih baik
        if 'tanggal_prediksi' in history_df.columns:
            history_df['tanggal_prediksi'] = pd.to_datetime(history_df['tanggal_prediksi']).dt.strftime('%d-%m-%Y %H:%M:%S')
        
        st.dataframe(history_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Detail prediksi
            if st.button("🔍 Lihat Detail Lengkap", key="view_details"):
                conn = get_db_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                SELECT * FROM prediksi_pasien 
                WHERE user_email = %s
                ORDER BY tanggal_prediksi DESC
                """, (st.session_state['user'],))
                
                detailed_results = cursor.fetchall()
                conn.close()
                
                detailed_df = pd.DataFrame(detailed_results)
                if 'tanggal_prediksi' in detailed_df.columns:
                    detailed_df['tanggal_prediksi'] = pd.to_datetime(detailed_df['tanggal_prediksi']).dt.strftime('%d-%m-%Y %H:%M:%S')
                
                st.dataframe(detailed_df, use_container_width=True)
        
        with col2:
            # Export ke CSV
            if st.button("📥 Export ke CSV", key="export_csv"):
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"prediksi_hemodialisis_{st.session_state['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Mapping fitur kategori
jenis_kelamin_mapping = {'laki-laki': 0, 'perempuan': 1}
riwayat_penyakit_keluarga_mapping = {
    'hipertensi': 5, 'tidak ada': 9, 'lambung': 8, 'asam urat': 1,
    'diabetes': 3, 'asam lambung': 0, 'jantung': 7, 'batu ginjal': 2,
    'hipotensi': 6, 'genetik': 4
}
riwayat_penyakit_mapping = {
    'hipertensi': 6, 'diabetes': 4, 'tidak ada': 13, 'jantung koroner': 9,
    'asam urat': 2, 'batu ginjal': 3, 'sesak nafas': 12, 'lambung': 11,
    'gagal ginjal': 5, 'asam lambung': 1, 'hipotensi': 7, 'kelainan darah': 10,
    'anemia': 0, 'jantung': 8
}

# Fungsi pra-pemrosesan data
def preprocess_data(data):
    data = data.copy()
    feature_cols = [
        'Jenis_Kelamin', 'usia', 'Sistolik', 'Diastolik', 'Hemoglobin', 'SI-TIBC_(%)',
        'Ureum', 'Kreatinin', 'EPO_3000', 'EPO_2000', 'TRON_SUCROSE',
        'lama_hemodialisis(bulan)', 'Riwayat_penyakit_keluarga', 'Riwayat_penyakit'
    ]
    
    # Pastikan semua kolom yang diperlukan ada di dataframe
    for col in feature_cols:
        if col not in data.columns:
            st.error(f"Kolom {col} tidak ditemukan pada data. Mohon periksa format file.")
            return None
    
    # Filter kolom yang diperlukan
    data = data[feature_cols]
    
    # Map kategori ke angka
    data['Jenis_Kelamin'] = data['Jenis_Kelamin'].map(jenis_kelamin_mapping)
    data['Riwayat_penyakit_keluarga'] = data['Riwayat_penyakit_keluarga'].map(riwayat_penyakit_keluarga_mapping)
    data['Riwayat_penyakit'] = data['Riwayat_penyakit'].map(riwayat_penyakit_mapping)
    
    # Map EPO fields from 'ya'/'tidak' to 1/0
    data['EPO_3000'] = data['EPO_3000'].map({'ya': 1, 'tidak': 0})
    data['EPO_2000'] = data['EPO_2000'].map({'ya': 1, 'tidak': 0})
    
    return data

# Halaman Prediksi
def prediction_page():
    display_app_header()
    
    # Tab untuk pemilihan input file atau manual
    tab1, tab2 = st.tabs(["📁 Upload File", "📝 Input Manual"])
    
    # Tab Upload File
    with tab1:
        st.markdown("""
        <div class="form-container">
            <h3 style="color: #1E3A8A; margin-bottom: 15px;">Upload Data Pasien</h3>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx"], key="file_uploader")
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                st.write("📊 Data yang diupload:")
                st.dataframe(data.head(), use_container_width=True)
                
                # Verifikasi kolom yang diperlukan
                missing_columns = []
                required_columns = ['Jenis_Kelamin', 'usia', 'Sistolik', 'Diastolik', 'Hemoglobin', 
                                   'SI-TIBC_(%)', 'Ureum', 'Kreatinin', 'EPO_3000', 'EPO_2000', 
                                   'TRON_SUCROSE', 'lama_hemodialisis(bulan)', 'Riwayat_penyakit_keluarga', 
                                   'Riwayat_penyakit']
                
                for col in required_columns:
                    if col not in data.columns:
                        missing_columns.append(col)
                
                if missing_columns:
                    st.error(f"Kolom berikut tidak ditemukan di file: {', '.join(missing_columns)}")
                    st.info("Pastikan file memiliki semua kolom yang diperlukan untuk prediksi.")
                else:
                    # Cek jika kolom nama pasien ada
                    if 'Nama_Pasien' not in data.columns:
                        st.warning("Kolom 'Nama_Pasien' tidak ditemukan. Akan menggunakan nomor ID sebagai nama pasien.")
                        data['Nama_Pasien'] = [f"Pasien #{i+1}" for i in range(len(data))]
                    
                    # Proses data
                    processed_data = preprocess_data(data)
                    
                    save_option = st.checkbox("Simpan hasil prediksi ke database", value=True)
                    
                    if st.button("⚡ Prediksi dari File", key="predict_from_file"):
                        with st.spinner("🔄 Memproses prediksi..."):
                            time.sleep(1)  # Simulasi proses
                            
                            # Prediksi
                            predictions = model.predict(processed_data)
                            complications = {0: '🚫 Tidak Ada', 1: '⚠ Hipertensi', 2: '⚠ Hipotensi', 3: '⚠ Gastrointestinal'}
                            text_predictions = [complications[pred] for pred in predictions]
                            data['Predicted_Komplikasi'] = text_predictions
                            
                            # Tampilkan hasil
                            st.success("✅ Prediksi selesai!")
                            
                            st.markdown("""
                            <div class="result-container">
                                <h3 style="color: #1E3A8A; margin-bottom: 15px;">Hasil Prediksi</h3>
                            """, unsafe_allow_html=True)
                            
                            result_df = data[['Nama_Pasien', 'Predicted_Komplikasi']].copy() if 'Nama_Pasien' in data.columns else data[['Predicted_Komplikasi']].copy()
                            st.dataframe(result_df, use_container_width=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            # Simpan ke database jika dipilih
                            if save_option:
                                try:
                                    saved_count = save_batch_predictions(data, text_predictions, st.session_state['user'])
                                    st.success(f"✅ Berhasil menyimpan {saved_count} data prediksi ke database.")
                                except Exception as e:
                                    st.error(f"❌ Gagal menyimpan data: {str(e)}")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memproses file: {str(e)}")
                
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab Input Manual
    with tab2:
        st.markdown("""
        <div class="form-container">
            <h3 style="color: #1E3A8A; margin-bottom: 15px;">Input Data Pasien</h3>
        """, unsafe_allow_html=True)
        
        # Tambahkan field nama pasien
        nama_pasien = st.text_input("👤 Nama Pasien", key="nama_pasien")
        
        # Form input
        col1, col2 = st.columns(2)
        
        with col1:
            jenis_kelamin = st.selectbox("👫 Jenis Kelamin", list(jenis_kelamin_mapping.keys()), key="jenis_kelamin")
            usia = st.number_input("🔢 Usia", min_value=1, max_value=100, step=1, value=30, key="usia")
            sistolik = st.number_input("💓 Sistolik (mmHg)", min_value=50, max_value=200, value=120, key="sistolik")
            diastolik = st.number_input("💓 Diastolik (mmHg)", min_value=30, max_value=150, value=80, key="diastolik")
            hemoglobin = st.number_input("🩸 Hemoglobin (g/dL)", min_value=3.0, max_value=20.0, value=10.0, key="hemoglobin")
            si_tibc = st.number_input("🧪 SI-TIBC (%)", min_value=0.0, max_value=100.0, value=30.0, key="si_tibc")
            ureum = st.number_input("🧪 Ureum (mg/dL)", min_value=10.0, max_value=300.0, value=30.0, key="ureum")
        
        with col2:
            kreatinin = st.number_input("🧪 Kreatinin (mg/dL)", min_value=20.0, max_value=500.0, value=100.0, key="kreatinin")
            epo_3000 = st.selectbox("💉 EPO 3000", ['ya', 'tidak'], key="epo_3000")
            epo_2000 = st.selectbox("💉 EPO 2000", ['ya', 'tidak'], key="epo_2000")
            tron_sucrose = st.number_input("💊 TRON SUCROSE", min_value=0.0, max_value=10.0, value=1.0, key="tron_sucrose")
            lama_hemodialisis = st.number_input("⏱️ Lama Hemodialisis (bulan)", min_value=1, max_value=100, value=36, key="lama_hemodialisis")
            riwayat_penyakit_keluarga = st.selectbox("👪 Riwayat Penyakit Keluarga", list(riwayat_penyakit_keluarga_mapping.keys()), key="riwayat_keluarga")
            riwayat_penyakit = st.selectbox("🩺 Riwayat Penyakit", list(riwayat_penyakit_mapping.keys()), key="riwayat_penyakit")
        
        save_option = st.checkbox("💾 Simpan hasil prediksi ke database", value=True, key="save_manual_pred")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            predict_button = st.button("🔮 Prediksi Komplikasi", key="predict_manual", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if predict_button:
            if not nama_pasien.strip():
                st.warning("⚠️ Mohon isi nama pasien terlebih dahulu.")
            else:
                manual_data = pd.DataFrame({
                    'Jenis_Kelamin': [jenis_kelamin],
                    'usia': [usia],
                    'Sistolik': [sistolik],
                    'Diastolik': [diastolik],
                    'Hemoglobin': [hemoglobin],
                    'SI-TIBC_(%)': [si_tibc],
                    'Ureum': [ureum],
                    'Kreatinin': [kreatinin],
                    'EPO_3000': [epo_3000],
                    'EPO_2000': [epo_2000],
                    'TRON_SUCROSE': [tron_sucrose],
                    'lama_hemodialisis(bulan)': [lama_hemodialisis],
                    'Riwayat_penyakit_keluarga': [riwayat_penyakit_keluarga],
                    'Riwayat_penyakit': [riwayat_penyakit]
                })
                
                manual_data_processed = preprocess_data(manual_data)
                
                with st.spinner("🔄 Memproses prediksi..."):
                    time.sleep(1)  # Simulasi proses
                    manual_prediction = model.predict(manual_data_processed)
                    complications = {0: '🚫 Tidak Ada', 1: '⚠ Hipertensi', 2: '⚠ Hipotensi', 3: '⚠ Gastrointestinal'}
                    manual_complication = complications[manual_prediction[0]]
                    
                    # Menentukan warna berdasarkan hasil prediksi
                    result_color = "#28a745"  # Hijau untuk tidak ada komplikasi
                    if manual_prediction[0] > 0:
                        result_color = "#ffc107"  # Kuning untuk komplikasi
                    
                    # Tampilkan hasil
                    st.markdown(f"""
                    <div class="result-container" style="border-left: 5px solid {result_color};">
                        <h3 style="color: #1E3A8A; text-align: center; margin-bottom: 15px;">Hasil Prediksi</h3>
                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                            <tr>
                                <td style="padding: 10px; font-weight: bold; width: 30%; border: 1px solid #ddd; background-color: #f8f9fa;">Nama Pasien</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{nama_pasien}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; font-weight: bold; border: 1px solid #ddd; background-color: #f8f9fa;">Jenis Kelamin</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{jenis_kelamin}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; font-weight: bold; border: 1px solid #ddd; background-color: #f8f9fa;">Usia</td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{usia} tahun</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; font-weight: bold; border: 1px solid #ddd; background-color: #f8f9fa;">Prediksi Komplikasi</td>
                                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: {result_color};">{manual_complication}</td>
                            </tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Simpan ke database jika dipilih
                    if save_option:
                        try:
                            pred_id = save_prediction(
                                nama_pasien, jenis_kelamin, usia, sistolik, diastolik, 
                                hemoglobin, si_tibc, ureum, kreatinin, epo_3000, epo_2000, 
                                tron_sucrose, lama_hemodialisis, riwayat_penyakit_keluarga, 
                                riwayat_penyakit, manual_complication, st.session_state['user']
                            )
                            st.success(f"✅ Data prediksi berhasil disimpan dengan ID: {pred_id}")
                        except Exception as e:
                            st.error(f"❌ Gagal menyimpan data: {str(e)}")

# Routing halaman berdasarkan session state
def main():
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'register':
        register_page()
    elif st.session_state['page'] == 'main' and st.session_state['authenticated']:
        main_page()
    else:
        # Fallback to login if state is inconsistent
        st.session_state['page'] = 'login'
        login_page()

# Run the application
if __name__ == "__main__":
    main()
