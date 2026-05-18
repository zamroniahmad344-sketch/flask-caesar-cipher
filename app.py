from flask import Flask, render_template, request, session, jsonify
from datetime import datetime

application = Flask(__name__)
application.secret_key = 'kode_rahasia_anda_123'

def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        namaDepan = request.form['namaDepan'].strip()
        namaBelakang = request.form['namaBelakang'].strip()
        nama = f"{namaDepan} {namaBelakang}"
        
        session['nama_asli'] = nama
        session['waktu_daftar'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        nama_terenkripsi = caesar_cipher(nama, 3)
        
        histori = session.get('histori', [])
        histori.append({
            'nama': nama,
            'enkripsi': nama_terenkripsi,
            'waktu': session['waktu_daftar']
        })
        session['histori'] = histori[-5:]
        
        return render_template('response.html', 
                             nama=nama,
                             nama_terenkripsi=nama_terenkripsi,
                             shift=3)
    
    return render_template('form.html')

@application.route('/histori')
def histori():
    histori = session.get('histori', [])
    return render_template('histori.html', histori=histori)

@application.route('/dekripsi', methods=['POST'])
def dekripsi():
    teks_enkripsi = request.form['teks_enkripsi']
    shift = int(request.form['shift'])
    teks_dekripsi = caesar_decipher(teks_enkripsi, shift)
    return render_template('dekripsi.html', hasil=teks_dekripsi)

@application.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()
    text = data.get('text', '')
    shift = data.get('shift', 3)
    result = caesar_cipher(text, shift)
    return jsonify({'status': 'success', 'encrypted': result, 'shift': shift})

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)