from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user
from .forms import LoginForm
from .models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('Siz muvaffaqiyatli tizimga kirdingiz!', category='success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('routes.index'))
        else:
            flash('Foydalanuvchi nomi yoki parol noto‘g‘ri', category='danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Siz tizimdan chiqdingiz.', category='info')
    return redirect(url_for('routes.index'))
