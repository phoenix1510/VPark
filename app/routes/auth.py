from flask import Flask , request, redirect , render_template , url_for ,session, Blueprint, flash
from werkzeug.security import generate_password_hash , check_password_hash
from app.db.db_operations import get_user_by_email, insert_user_into_db
from functools import wraps
from app.routes.wtfforms import LoginForm , SignupForm

auth_bp = Blueprint('auth',__name__, url_prefix='/auth')

@auth_bp.route('/login',methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = get_user_by_email(email)

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = user['name']
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            flash('Successfully logged in!','success')
            return redirect(url_for('user.user_dashboard'))
        else:
            flash('Incorrect username/password','danger')

    return render_template('login.html',form=form)


@auth_bp.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        session.pop('user_id',None)
        session.pop('role',None)
        flash("Successfully logged out!",'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone_num = form.phone_number.data
        password_hash = generate_password_hash(password)

        user = get_user_by_email(email)

        if user:
            flash('User already exists!','danger')
        else:
            insert_user_into_db(name, email, password_hash, phone_num,role='user')
            return redirect(url_for('auth.login'))
    return render_template('signup.html',form=form)
        
@auth_bp.route('/login/admin',methods=['GET','POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = get_user_by_email(email)

        if user and check_password_hash(user['password_hash'], password):
            if user['role'] == 'admin':
                session['username'] = user['name']
                session['user_id'] = user['user_id']
                session['role'] = user['role']
                flash('Successfully logged in!','success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Not an admin!!','danger')
        else:
            flash('Username/Password is incorrect!', 'danger')
    return render_template('admin_login.html',form=form)


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))

        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('user.user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function