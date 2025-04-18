import os
from flask import (
    Flask, render_template, url_for, send_from_directory,
    request, redirect, flash
)
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'substitua_por_uma_chave_secreta_forte'

# Diretórios
PHOTO_DIR = os.path.join(app.static_folder, 'photos')
THUMB_DIR = os.path.join(PHOTO_DIR, 'thumbs')

# Garante que a pasta de thumbnails exista
os.makedirs(THUMB_DIR, exist_ok=True)

def generate_thumbnails():
    """Gera thumbnails 300×300 pra cada imagem nova."""
    for fn in os.listdir(PHOTO_DIR):
        src_path = os.path.join(PHOTO_DIR, fn)
        thumb_path = os.path.join(THUMB_DIR, fn)
        if not fn.lower().endswith(('.png','.jpg','jpeg','gif')): 
            continue
        if os.path.exists(thumb_path):
            continue  # já existe
        try:
            img = Image.open(src_path)
            img.thumbnail((300,300))
            img.save(thumb_path)
            print(f"[thumb] {fn}")
        except Exception as e:
            print(f"Erro thumbnail {fn}: {e}")

# Gera ao iniciar
generate_thumbnails()

@app.route('/')
def gallery():
    # Lista arquivos originais
    filenames = sorted(
        fn for fn in os.listdir(PHOTO_DIR)
        if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    )
    photos = []
    for fn in filenames:
        photos.append({
            'filename': fn,
            'url':        url_for('static', filename=f'photos/{fn}'),
            'thumb_url':  url_for('static', filename=f'photos/thumbs/{fn}')
        })
    return render_template('gallery.html', photos=photos)

@app.route('/download/<filename>')
def download(filename):
    # força cache (30 dias)
    return send_from_directory(PHOTO_DIR, filename, as_attachment=True, cache_timeout=2592000)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
