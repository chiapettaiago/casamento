import os
from itsdangerous import URLSafeSerializer
from flask import (
    Flask, render_template, url_for, send_from_directory,
    request, redirect, flash
)
from werkzeug.utils import secure_filename
from PIL import Image
from functools import lru_cache
import time

app = Flask(__name__)
app.secret_key = 'substitua_por_uma_chave_secreta_forte'

serializer = URLSafeSerializer(app.secret_key)

# Diretórios
PHOTO_DIR = os.path.join(app.static_folder, 'photos')
THUMB_DIR = os.path.join(PHOTO_DIR, 'thumbs')

# Garante que a pasta de thumbnails exista
os.makedirs(THUMB_DIR, exist_ok=True)

def generate_thumbnail(filename):
    """Gera thumbnail 300×300 para uma imagem específica."""
    src_path = os.path.join(PHOTO_DIR, filename)
    thumb_path = os.path.join(THUMB_DIR, filename)
    
    if not filename.lower().endswith(('.png','.jpg','.jpeg','.gif')): 
        return False
        
    if os.path.exists(thumb_path):
        return True  # já existe
        
    try:
        img = Image.open(src_path)
        img.thumbnail((300,300))
        img.save(thumb_path)
        print(f"[thumb] {filename}")
        return True
    except Exception as e:
        print(f"Erro thumbnail {filename}: {e}")
        return False

@lru_cache(maxsize=1)
def get_photos_list():
    """Retorna lista de fotos com cache."""
    photos = []
    for entry in os.scandir(PHOTO_DIR):
        if not entry.is_file():
            continue
        if not entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            continue
            
        # Gera thumbnail se necessário
        generate_thumbnail(entry.name)
            
        photos.append({
            'filename': entry.name,
            'url': url_for('static', filename=f'photos/{entry.name}'),
            'thumb_url': url_for('static', filename=f'photos/thumbs/{entry.name}')
        })
    return sorted(photos, key=lambda x: x['filename'])

@app.route('/')
def gallery():
    photos = get_photos_list()
    return render_template('gallery.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        flash('Nenhum arquivo selecionado', 'warning')
        return redirect(url_for('gallery'))
        
    file = request.files['photo']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'warning')
        return redirect(url_for('gallery'))
        
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(PHOTO_DIR, filename)
        file.save(filepath)
        
        # Gera thumbnail apenas para a nova imagem
        generate_thumbnail(filename)
        
        # Limpa o cache da lista de fotos
        get_photos_list.cache_clear()
        
        flash('Imagem enviada com sucesso!', 'success')
    else:
        flash('Tipo de arquivo não permitido', 'danger')
        
    return redirect(url_for('gallery'))

@app.route('/download/<filename>')
def download(filename):
    # força cache (30 dias)
    return send_from_directory(PHOTO_DIR, filename, as_attachment=True, cache_timeout=2592000)

@app.route('/view/<token>')
def view_photo(token):
    try:
        filename = serializer.loads(token)
        photo_path = os.path.join(PHOTO_DIR, filename)
        if not os.path.exists(photo_path):
            raise FileNotFoundError
        return render_template('view.html', filename=filename)
    except Exception:
        flash('Link inválido ou imagem não encontrada.', 'danger')
        return redirect(url_for('gallery'))
    
@app.route('/generate-token/<filename>')
def generate_token(filename):
    token = serializer.dumps(filename)
    link = url_for('view_photo', token=token, _external=True)
    return link

@app.route('/edit/<filename>', methods=['GET','POST'])
def edit(filename):
    src_path = os.path.join(PHOTO_DIR, filename)
    if not os.path.exists(src_path):
        flash('Arquivo não encontrado.', 'danger')
        return redirect(url_for('gallery'))
    if request.method == 'POST':
        new_name = secure_filename(request.form['new_name'])
        if new_name:
            ext = os.path.splitext(filename)[1]
            new_filename = new_name + ext
            os.rename(src_path, os.path.join(PHOTO_DIR, new_filename))
            # atualiza thumbnail também
            os.rename(
                os.path.join(THUMB_DIR, filename),
                os.path.join(THUMB_DIR, new_filename)
            )
            flash('Imagem renomeada!', 'success')
            return redirect(url_for('gallery'))
        flash('Nome inválido.', 'warning')
    return render_template('edit.html', filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
