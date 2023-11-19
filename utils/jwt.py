import jwt
import datetime

# Fungsi untuk membuat JWT
def generate_token(secret_key, payload):
    # Tambahkan waktu kadaluwarsa token (contoh: 1 jam)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    # Tambahkan informasi waktu kadaluwarsa ke payload
    payload['exp'] = expiration_time

    # Generate token
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token

# Fungsi untuk memverifikasi JWT
def verify_token(token, secret_key):
    try:
        # Verifikasi token dan dekode payload
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Verifikasi waktu kadaluwarsa
        current_time = datetime.datetime.utcnow()
        
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            
            # Konversi timestamp UNIX menjadi objek datetime
            exp_datetime = datetime.datetime.utcfromtimestamp(exp_timestamp)
            
            if exp_datetime < current_time:
                return None  # Token telah kedaluwarsa
        
        return payload  # Token valid, kembalikan payload

    except jwt.ExpiredSignatureError:
        return None  # Token telah kedaluwarsa

    except jwt.InvalidTokenError:
        return None  # Token tidak valid