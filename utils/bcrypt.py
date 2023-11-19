import bcrypt
import base64

# Fungsi untuk membuat hash dari password
def hash_password(password) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Encode hash sebagai string menggunakan base64
    encoded_password = base64.b64encode(hashed_password).decode('utf-8')
    
    return encoded_password

# Fungsi untuk memverifikasi password dari string yang dienkripsi
def verify_password(entered_password, stored_encoded_password) -> bool:
    stored_hashed_password = base64.b64decode(stored_encoded_password)
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)