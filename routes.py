from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from data_handler import get_jumlah_data
from logic import *
from flask_bcrypt import bcrypt
from models import db, bcrypt, User

# Buat blueprint untuk rute
routes_bp = Blueprint('routes', __name__)

# Rute untuk halaman login
@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    return get_login()

# Rute untuk halaman register
@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    return get_register()

@routes_bp.route('/keluar')
def logout():
    return get_logout()

# Rute untuk halaman login
@routes_bp.route('/')
def index():
    # Mengembalikan halaman HTML menggunakan fungsi render_template
    return redirect(url_for("routes.login"))



# Rute untuk halaman dashboard
@routes_bp.route('/dashboard')
@login_required
def home():
    return get_home()


@routes_bp.route('/data-makanan')
@login_required
def data_makanan():
    return get_data_makanan()


@routes_bp.route('/data-akg')
@login_required
def data_akg():
    return get_data_akg()

@routes_bp.route('/data-ortu')
@login_required
def data_ortu():
    return get_data_ortu()
    
