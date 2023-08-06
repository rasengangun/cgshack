from flask import render_template, request, redirect, url_for, flash
import os
from bullshit import db, app,login_manager
from bullshit.models import Lay, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def main():
    return render_template('first.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect('/posts')
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    return render_template('first.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.route('/posts')
@login_required
def posts():
    articles = Lay.query.order_by(Lay.id.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
@login_required
def post_page(id):
    post = Lay.query.get(id)
    return render_template("post.html", post=post)


@app.route('/posts/<int:id>/war1ace')
@login_required
def post_delete(id):
    post = Lay.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        if post.photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], post.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        flash('Лекция успешно удалена', 'success')

    except:
        flash('Ошибка при удалении лекции', 'danger')

    return render_template('posts.html')


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add_lecture():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        title = request.form['title']
        spec = request.form['spec']
        photo = None

        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = filename

        lerc = Lay(title=title, surname=surname, name=name, spec=spec,photo=photo)

        try:
            db.session.add(lerc)
            db.session.commit()
            return redirect('/posts')
        except ValueError as e:
            return render_template("add.html")
        except FileNotFoundError as e:
            return render_template("add.html")
    else:
        return render_template("add.html")


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

