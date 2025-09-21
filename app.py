from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# 1. Buat instance ekstensi terlebih dahulu
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login' # Mengarahkan ke route 'login' jika akses ditolak

# 2. Buat aplikasi Flask
app = Flask(__name__)
app.config.from_object(Config)

# 3. Hubungkan ekstensi dengan aplikasi
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User # Impor di dalam fungsi
    return User.query.get(int(user_id))

@app.route('/')
def index():
    # Mengarahkan ke halaman tes jika sudah login, atau ke login jika belum
    if current_user.is_authenticated:
        return redirect(url_for('test_page'))
    return redirect(url_for('login'))

@app.route('/test')
@login_required # Mengamankan halaman ini
def test_page():
    return f"<h1>Hello, {current_user.username}! This is a protected page.</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('test_page'))
    
    from forms import LoginForm
    from models import User # Impor di dalam fungsi
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}!')
        return redirect(url_for('test_page'))
        
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('test_page'))
        
    from forms import RegistrationForm
    from models import User # Impor di dalam fungsi
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)