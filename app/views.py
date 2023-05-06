from urllib.parse import urlparse, urljoin

import uuid0
from flask import render_template, request, send_from_directory, redirect, url_for
from flask_login import login_required, LoginManager, login_user, current_user, UserMixin, logout_user

from app import app, db_models, db, login_manager
from .db_models import User, set_password, Report
from .models import ModelTreat
from app import report_maker
from app.forms.LoginForm import LoginForm, RegistrationForm


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/report', methods=['GET', 'POST'])
def report():
    model_treat = ModelTreat()
    req_params = request.get_json('report', silent=True)  # принимаем результаты в формате json
    if req_params is not None:
        print(req_params)
        try:
            handled_values = report_maker.handle_values_R_nadezh(req_params)
            filename = report_maker.excelmaker(handled_values, 'A14')
            report_maker.save_report(filename)
        except Exception as e:
            print('def report')
            print(e)
    return render_template('report.html',
                           model=model_treat)


@app.route('/gost_69420')
@login_required
def index():
    return render_template('index.html')


@app.route('/download')
@app.route('/download/<filename>')
@login_required
def download(filename):
    file = Report.query.filter(
        Report.name == filename
    ).first()
    download_string = report_maker.readreport(file.file, file.name)
    return send_from_directory(download_string, file.name)


@app.route('/personal_account')
@login_required
def personal_account():
    user_reports = Report.query.filter(
        Report.owner == current_user.name
    ).all()
    user = current_user
    return render_template('personal_account.html', user=user, reports=user_reports)


@app.route('/')
@app.route('/main')
@login_required
def main_page():
    return render_template('main_page.html')


@app.route('/login', defaults={'errors': None}, methods=['GET', 'POST'])
@app.route('/login/<errors>')
def login(errors=None):
    form = LoginForm()

    return render_template('login.html', title='Вход', form=form, error=errors)


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        auth = User.query.filter(
            User.name == name
        ).first()
        if auth is not None and auth.check_password(password):
            login_user(auth)
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('login', errors="Неверный логин или пароль"))


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            newuser = User()
            newuser.name = form.username.data
            newuser.password = set_password(form.password.data)
            newuser.UUID = str(uuid0.generate())
            u: User = db_models.User(name=newuser.name, password=newuser.password, UUID=newuser.UUID)  # type: ignore
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('main_page'))
        except Exception as e:
            print(e)
    return render_template('register.html', title='Регистрация', form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
