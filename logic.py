
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from data_handler import get_jumlah_data
from flask_bcrypt import Bcrypt
from models import db, User
from functools import wraps

# Inisialisasi objek bcrypt
bcrypt = Bcrypt()

# Hardcoded admin usernames
ADMIN_USERS = ["admin", "admin2", "superuser"]

# Correct decorator
def ortu_only(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.username == 'admin':
            return redirect(url_for('unauthorized'))
        return func(*args, **kwargs)
    return wrapper




# Fungsi untuk halaman register
def get_register():
    # Jika pengguna sudah login, arahkan ke halaman home
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    # Jika pengguna belum login, tampilkan halaman register
    if request.method == "POST":
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Akun berhasil dibuat! Silahkan login.', 'success')
        return redirect(url_for("routes.login"))
    return render_template("auth/page_register.html")

# Fungsi untuk halaman login
def get_login():
    # Jika pengguna sudah login, arahkan ke halaman home
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    # Jika pengguna belum login, tampilkan halaman login
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            if username in ADMIN_USERS:
                return redirect(url_for("routes.home"))
            flash("Login Berhasil!", "success")
            return redirect(url_for("routes.home"))
        else:
            flash('Username atau password salah!', 'danger')
    return render_template("auth/page_login.html")

def get_logout():
    logout_user()  # Menghapus sesi pengguna
    return redirect(url_for('routes.login'))

# halaman dashboard
def get_home():
    # Mendapatkan jumlah data dari file CSV
    file_path = 'bahan_pangan_eliminated.csv'
    jumlah_data = get_jumlah_data(file_path)
    jumlah_user = User.query.count()

    # Mengarahkan ke dashboard berdasarkan username
    if current_user.username == 'admin':
        return render_template('admin/dashboard.html', jumlah_data=jumlah_data ,jumlah_user=jumlah_user)
    else:
        return render_template('orangtua/dashboard.html', jumlah_data=jumlah_data)

# halaman data makanan
def get_data_makanan():
    if current_user.username == 'admin':
        return render_template('admin/data_makanan.html')
    else:
        return render_template('orangtua/data_makanan.html')

# halaman data akg
def get_data_akg():
    if current_user.username == 'admin':
        return render_template('admin/data_akg.html')
    else:
        return render_template('orangtua/data_akg.html')
    
def get_data_ortu():
    users = User.query.filter(~User.username.in_(ADMIN_USERS)).all()

    page = request.args.get('page', 1, type=int)  # Ambil parameter halaman, default 1
    per_page = 10  # Jumlah pengguna per halaman
    users_paginated = User.query.filter(User.username != 'admin').paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/data_orangtua.html', users=users_paginated)
    
