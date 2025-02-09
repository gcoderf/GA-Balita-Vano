from flask import Flask, render_template, request, redirect,url_for,jsonify,send_from_directory, flash
from GAmodel import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from data_handler import get_jumlah_data
from models import db, bcrypt, User

from routes import routes_bp  # Import blueprint dari routes.py
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_flask.db'
app.config['SECRET_KEY'] = 'ta-gevano'
app.config['UPLOAD_FOLDER'] = 'dataset'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Hardcoded admin usernames
ADMIN_USERS = ["admin1", "admin2", "superuser"]

# Pastikan folder uploads ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Daftarkan blueprint
app.register_blueprint(routes_bp)

@app.route("/recommendation",methods =["GET", "POST"])
def meal_plan():
    if (request.method == "POST"):
        mealplans,listNutritionTarget,best_fitness  =final(int(request.form['usia']))
        labelMenu=["Pagi", "Siang", "Malam"]
        labelNutrisi=["Karbohidrat","Lemak","Protein","Serat"]
        imageNutrisi=["karbo.jpg","fat.jpg","prot.jpg","fiber.jpg"]
        image=["https://images.unsplash.com/photo-1593100164369-e90cdff9678a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1167&q=80","https://images.unsplash.com/photo-1471938537155-7de0bd123d0c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80","https://images.unsplash.com/photo-1629822937307-ce27f951e385?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1169&q=80",]
        totCaloriesMealPlan=[round(mealplans[0]['Energi (kal)'].sum(),1), 
                             round(mealplans[1]['Energi (kal)'].sum(),1),
                             round(mealplans[2]['Energi (kal)'].sum(),1)]
        return render_template('orangtua/recommendation.html', listMealPlan=mealplans, labelMenu=labelMenu, imageList=image, listNutritionTarget=listNutritionTarget,labelNutrisi=labelNutrisi,imageNutrisi=imageNutrisi,totCaloriesMealPlan=totCaloriesMealPlan,bestFitness=round(best_fitness, 2))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload-akg', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = "akg.csv"  # Nama file statis
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)  # File otomatis menimpa jika ada
            flash("File berhasil di import!", "success")
            return redirect(url_for("routes.data_akg"))
        else:
            flash("File tidak valid. Harap unggah file CSV.", "error")
            return redirect(request.url)

    return render_template('admin/data_akg.html')

@app.route('/upload-makanan', methods=['GET', 'POST'])
def upload_file_makanan():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = "bahan_pangan_eleminated.csv"  # Nama file statis
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)  # File otomatis menimpa jika ada
            flash("File berhasil di import!", "success")
            return redirect(url_for("routes.data_makanan"))
        else:
            flash("File tidak valid. Harap unggah file CSV.", "error")
            return redirect(request.url)

    return render_template('admin/data_akg.html')


@app.route('/dataset/<filename>')
def get_file(filename):
    return send_from_directory('dataset', filename)




@app.route('/recommendation')
def recommendations():
    if current_user.username == 'admin':
        return redirect(url_for('unauthorized'))
    else:
        return render_template('recommendation.html')
    

# Handler untuk error 404
@app.errorhandler(404)
def page_not_found(e):
    # Pastikan untuk memanggil file template di folder yang sesuai
    return render_template('misc/404.html'), 404

# Handler untuk error 403
@app.route("/unauthorized")
def unauthorized():
    return render_template("misc/403_not_authorized.html"), 403

# Tentukan handler untuk unauthorized (pengguna yang belum login)
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('unauthorized'))  # Arahkan ke halaman unauthorize


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000,debug=True) 