import os
from dotenv import load_dotenv

# Menentukan direktori dasar proyek
basedir = os.path.abspath(os.path.dirname(__file__))
# Memuat file .env dari direktori dasar tersebut
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Mengatur variabel konfigurasi Flask dari file .env."""
    
    # Kunci rahasia untuk keamanan (misalnya, untuk sesi dan cookies)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-secret-key-that-is-not-secure'
    
    # Alamat koneksi ke database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        
    # Menonaktifkan fitur Flask-SQLAlchemy yang tidak kita perlukan
    SQLALCHEMY_TRACK_MODIFICATIONS = False