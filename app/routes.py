from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import FikrForm
from .models import Fikr
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/')
@login_required
def index():
    fikrs = Fikr.query.order_by(Fikr.created_at.desc()).all()
    return render_template('index.html', fikrs=fikrs)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_fikr():
    form = FikrForm()
    if form.validate_on_submit():
        fikr = Fikr(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(fikr)
        db.session.commit()
        flash('Fikr muvaffaqiyatli qoʻshildi!', category='success')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=form)

@bp.route('/read/<int:id>')
@login_required
def read_fikr(id):
    fikr = Fikr.query.get_or_404(id)
    return render_template('read.html', fikr=fikr)
