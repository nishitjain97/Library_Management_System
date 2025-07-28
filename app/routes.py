from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Book, db, User
from . import login_manager
from .forms import BookForm, RegisterForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('main.add_book'))
        else:
            return redirect(url_for('main.search_books'))

    return """
        <h1>Welcome to the BeeBee Library.</h1>
        <a href='/login'>Login</a> | <a href='/register'>Register</a>
    """

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('main.register'))
        
        user = User(email=form.email.data, password=form.password.data, role='member')
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Form validated")
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful.')
            if user.role == 'admin':
                return redirect(url_for('main.add_book'))
            else:
                return redirect(url_for('main.search_books'))
        flash('Invalid credentials.')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('main.login'))

@main.route('/search-books')
@login_required
def search_books():
    print("Search books route hit.")
    return render_template('search_books.html')

@main.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            genre=form.genre.data,
            publisher=form.publisher.data,
            year=form.year.data,
            copies=form.copies.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('main.add_book'))
    return render_template('add_book.html', form=form)