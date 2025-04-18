import os
from flask import Flask, render_template, url_for, send_from_directory, request, redirect, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'substitua_por_uma_chave_secreta_forte'

PHOTO_DIR = os.path.join(app.static_folder, 'photos')

@app.route('/')
def gallery():
    filenames = sorted(
        fn for fn in os.listdir(PHOTO_DIR)
        if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    )
    photos = [
        {
            'filename': fn,
            'url': url_for('static', filename=f'photos/{fn}')
        }
        for fn in filenames
    ]
    return render_template('gallery.html', photos=photos)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        PHOTO_DIR, filename, as_attachment=True
    )

@app.route('/edit/<filename>', methods=['GET', 'POST'])
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
            dst_path = os.path.join(PHOTO_DIR, new_filename)
            os.rename(src_path, dst_path)
            flash('Imagem renomeada com sucesso!', 'success')
            return redirect(url_for('gallery'))
        else:
            flash('Nome inválido.', 'warning')
    return render_template('edit.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)