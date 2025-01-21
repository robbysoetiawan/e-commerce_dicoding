# Proyek Analisis Data - Dashboard ✨

Proyek ini adalah analisis data penjualan pada suatu e-commerce di Brazil, tools yang digunakan adalah python(jupyter notebook) untuk pembersihan dan analisis data, serta streamlit untuk pembuatan dashboard interaktif.

## Setup Environment
1. **Buat Virtual Environment**  
   Untuk memulai, buat virtual environment dengan Python:  
   `python -m venv venv`

2. **Aktifkan Virtual Environment**  
   Aktifkan virtual environment yang telah dibuat:  
   - Di Windows:  
     `.\\venv\\Scripts\\activate`  
   - Di macOS/Linux:  
     `source venv/bin/activate`

3. **Install Dependencies**  
   Install dependencies yang diperlukan untuk proyek ini menggunakan pip:  
   `pip install -r requirements.txt`

## Menjalankan Streamlit App  
Setelah environment siap, jalankan aplikasi Streamlit dengan perintah berikut:  
`streamlit run latihan.py`  
Aplikasi Streamlit akan terbuka di browser dengan alamat default `http://localhost:8501`.

## Struktur Proyek  
proyek_analisis_data/  
│  
├── venv/                  # Virtual environment  
├── dashboard.py           # File utama untuk Streamlit Dashboard  
├── requirements.txt       # Daftar dependencies  
├── data/                  # Folder untuk data yang digunakan  
└── README.md              # Dokumentasi proyek  

## Requirements  
Berikut adalah daftar pustaka yang digunakan dalam proyek ini, yang perlu diinstall melalui `requirements.txt`:  
`streamlit`, `pandas`, `streamlit-option-menu`,`plotly`,`Pillow`,`Babel`, `numpy`, `seaborn`, `warnings`, `matplotlib`, `sklearn`