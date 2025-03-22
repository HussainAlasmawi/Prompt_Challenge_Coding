from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from forms import RegistrationForm, LoginForm, BookingForm
from models import db, User, Booking
from data import DESTINATIONS, PACKAGES, generate_ai_tip, get_available_dates, dynamic_price

app = Flask(__name__)
app.config['SECRET_KEY'] = 'futuristicsecret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///space_travel.db'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300))

def create_sample_data():
    if Package.query.count() == 0:
        sample_packages = [
            Package(name='Economy Shuttle', base_price=5000, description='Basic orbital shuttle experience.'),
            Package(name='Luxury Cabin', base_price=15000, description='Spacious cabin with private view dome.'),
            Package(name='VIP Zero-Gravity Experience', base_price=30000, description='Zero-G fun with luxury service.')
        ]
        db.session.bulk_save_objects(sample_packages)
        db.session.commit()
        print("✅ Sample travel packages added.")

initialized = False

@app.before_request
def initialize():
    global initialized
    if not initialized:
        db.create_all()
        create_sample_data()
        initialized = True


@app.route('/')
def home():
    return render_template('home.html', packages=PACKAGES)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    tip = generate_ai_tip()
    return render_template('dashboard.html', bookings=bookings, tip=tip)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookingForm()
    form.destination.choices = [(dest, dest) for dest in DESTINATIONS]
    form.departure_date.choices = [(date, date) for date in get_available_dates()]
    if form.validate_on_submit():
        price = dynamic_price(form.departure_date.data, form.seat_class.data)
        booking = Booking(
            destination=form.destination.data,
            departure_date=form.departure_date.data,
            seat_class=form.seat_class.data,
            price=price,
            user_id=current_user.id
        )
        db.session.add(booking)
        db.session.commit()
        flash('Trip booked successfully!', 'success')
        return redirect(url_for('confirmation', booking_id=booking.id))
    return render_template('book_trip.html', form=form)

@app.route('/confirmation/<int:booking_id>')
@login_required
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirmation.html', booking=booking)

@app.route('/compare')
def compare():
    return render_template('compare.html', packages=PACKAGES)

if __name__ == '__main__':
    app.run(debug=True)
