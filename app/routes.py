from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, SpellForm, HistoryForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Qqquery
from werkzeug.urls import url_parse
from subprocess import check_output


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_two_factor(form.two_factor.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, success  you are now a registered user!')
        return redirect(url_for('login'))
    flash('failure')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        if not user.check_two_factor(form.two_factor.data):
            flash('failure Two-factor')
            return redirect(url_for('login'))
        flash('Success login')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def get_shell_script_output_using_check_output(spelling):
    stdout = check_output(['./a.out', './dictionary.txt', spelling]).decode('utf-8')
    return stdout


@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spell_check():
    form = SpellForm()
    if form.validate_on_submit():
        original = form.spell.data
        result = get_shell_script_output_using_check_output(original)
        new_query = Qqquery(data=original,
                            user_id=current_user.id,
                            output=result
                            )
        db.session.add(new_query)
        db.session.commit()
        flash('Success spell check')
        return redirect(url_for('index'))
    result = "no results"
    return render_template('spell_check.html', title='Spell Check', form=form, spell=result)


@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    form = HistoryForm()
    queries = Qqquery.query.filter_by(user_id=current_user.id)
    if current_user.admin:
        queries = Qqquery.query.all()
    if form.validate_on_submit():
        original = form.username.data
        user = User.query.filter_by(username=original).first()
        queries = Qqquery.query.filter_by(user_id=user.id)
    return render_template('history.html', title='History', form=form, queries=queries)


@app.route('/history/query<int:query_id>', methods=['GET'])
@login_required
def query(query_id):
    result = Qqquery.query.filter_by(id=query_id, user_id=current_user.id).first()
    if current_user.admin:
        result = Qqquery.query.filter_by(id=query_id).first()
    if result:
        return render_template('qqquery.html', title='Query Show', qqquery=result, user=current_user)
    else:
        return redirect(url_for('history'))


@app.route('/login_history', methods=['GET'])
@login_required
def logins():
    return render_template('login_history.html', title='Login History')
