from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Volunteer, Event, EventVolunteer
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
from twilio.rest import Client
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_nainjas.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['EVENT_IMAGES_FOLDER'] = os.path.join('static', 'images', 'events')
app.config['VOLUNTEER_PHOTOS_FOLDER'] = os.path.join('static', 'uploads', 'volunteers')
app.config['VOLUNTEER_DOCS_FOLDER'] = os.path.join('static', 'uploads', 'documents')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure all required directories exist
for folder in [app.config['UPLOAD_FOLDER'], 
               app.config['EVENT_IMAGES_FOLDER'],
               app.config['VOLUNTEER_PHOTOS_FOLDER'],
               app.config['VOLUNTEER_DOCS_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
TWILIO_CONTENT_SID = os.getenv('TWILIO_CONTENT_SID')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@login_manager.user_loader
def load_user(user_id):
    return Volunteer.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create new tables with updated schema
    print("Database tables recreated successfully!")

def send_whatsapp_message(to_number, event_title, event_date, event_time, whatsapp_group_link):
    """Send WhatsApp message using Twilio template"""
    try:
        # Format the number to WhatsApp format
        to_whatsapp = f"whatsapp:{to_number}"
        
        # Create message using template
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            content_sid=TWILIO_CONTENT_SID,
            content_variables=json.dumps({
                "1": event_date,
                "2": event_time,
                "3": event_title,
                "4": whatsapp_group_link
            }),
            to=to_whatsapp
        )
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return False

# Admin login required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in') or session.get('admin_email') != 'abhaychoudhary888888@gmail.com':
            flash('Please login as admin to access this page', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Single admin user credentials
        ADMIN_EMAIL = 'abhaychoudhary888888@gmail.com'
        ADMIN_PASSWORD = 'Choudhary0211@1983'
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_email'] = email
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_events = Event.query.count()
    total_volunteers = Volunteer.query.count()
    total_registrations = EventVolunteer.query.count()
    recent_events = Event.query.order_by(Event.date.desc()).limit(5).all()
    recent_registrations = EventVolunteer.query.order_by(EventVolunteer.registered_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_events=total_events,
                         total_volunteers=total_volunteers,
                         total_registrations=total_registrations,
                         recent_events=recent_events,
                         recent_registrations=recent_registrations,
                         now=datetime.now())

@app.route('/admin/events')
@admin_required
def admin_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('admin_events.html', events=events, now=datetime.now())

@app.route('/admin/events/create', methods=['GET', 'POST'])
@admin_required
def admin_create_event():
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title')
            description = request.form.get('description')
            date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
            time = request.form.get('time')
            location = request.form.get('location')
            whatsapp_group_link = request.form.get('whatsapp_group_link')
            
            # Handle image upload
            image = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Create a secure filename with timestamp
                    filename = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(file.filename)}"
                    # Create the full path for saving
                    file_path = os.path.join(app.config['EVENT_IMAGES_FOLDER'], filename)
                    # Save the file
                    file.save(file_path)
                    # Store just the filename for database
                    image = filename
                    print(f"Image saved to: {file_path}")  # Debug print
            
            # Create new event
            event = Event(
                title=title,
                description=description,
                date=date,
                time=time,
                location=location,
                image=image,
                whatsapp_group_link=whatsapp_group_link
            )
            
            db.session.add(event)
            db.session.commit()
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('admin_events'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating event: {str(e)}")  # Debug print
            flash(f'Error creating event: {str(e)}', 'error')
            return redirect(url_for('admin_create_event'))
    
    return render_template('admin_create_event.html')

@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        event.location = request.form.get('location')
        event.whatsapp_group_link = request.form.get('whatsapp_group_link')
        
        # Handle image upload
        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('images/events', filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            event.image = image_path
        
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin_edit_event.html', event=event)

@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def admin_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin_events'))

@app.route('/admin/volunteers')
@admin_required
def admin_volunteers():
    volunteers = Volunteer.query.all()
    return render_template('admin_volunteers.html', volunteers=volunteers)

@app.route('/admin/volunteers/<int:volunteer_id>')
@admin_required
def admin_view_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    return render_template('admin_view_volunteer.html', volunteer=volunteer)

@app.route('/admin/volunteers/<int:volunteer_id>/toggle', methods=['POST'])
@admin_required
def admin_toggle_volunteer_status(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    volunteer.is_verified = not volunteer.is_verified
    db.session.commit()
    flash(f'Volunteer {volunteer.name} has been {"verified" if volunteer.is_verified else "unverified"}', 'success')
    return redirect(url_for('admin_volunteers'))

@app.route('/')
def home():
    # Get upcoming events (events with dates in the future)
    upcoming_events = Event.query.filter(Event.date >= datetime.now().date()).order_by(Event.date).all()
    
    # Get past events (events with dates in the past)
    past_events = Event.query.filter(Event.date < datetime.now().date()).order_by(Event.date.desc()).all()
    
    return render_template('index.html', 
                         upcoming_events=upcoming_events, 
                         past_events=past_events)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Handle file uploads
            photo = request.files['photo']
            doc_front = request.files['document_front']
            doc_back = request.files['document_back']
            
            # Generate unique filenames
            photo_filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(photo.filename)}"
            doc_front_filename = f"doc_front_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(doc_front.filename)}"
            doc_back_filename = f"doc_back_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(doc_back.filename)}"
            
            # Save files with proper paths
            photo_path = os.path.join(app.config['VOLUNTEER_PHOTOS_FOLDER'], photo_filename)
            doc_front_path = os.path.join(app.config['VOLUNTEER_DOCS_FOLDER'], doc_front_filename)
            doc_back_path = os.path.join(app.config['VOLUNTEER_DOCS_FOLDER'], doc_back_filename)
            
            photo.save(photo_path)
            doc_front.save(doc_front_path)
            doc_back.save(doc_back_path)

            # Create new volunteer with relative paths
            volunteer = Volunteer(
                name=request.form['name'],
                phone=request.form['phone'],
                email=request.form['email'],
                document_type=request.form['document_type'],
                document_number=request.form['document_number'],
                whatsapp_number=request.form['whatsapp_number'],
                photo=os.path.join('uploads', 'volunteers', photo_filename),
                document_front=os.path.join('uploads', 'documents', doc_front_filename),
                document_back=os.path.join('uploads', 'documents', doc_back_filename)
            )
            volunteer.set_password(request.form['password'])

            db.session.add(volunteer)
            db.session.commit()
            flash('Registration successful! Please wait for verification.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        volunteer = Volunteer.query.filter_by(email=email).first()
        if volunteer and volunteer.check_password(password):
            login_user(volunteer)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    volunteer = current_user
    registered_events = volunteer.registered_events
    return render_template('dashboard.html', volunteer=volunteer, registered_events=registered_events)

@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if volunteer is already registered
    if event in current_user.registered_events:
        flash('You are already registered for this event!', 'warning')
        return redirect(url_for('home'))
    
    # Create new registration
    registration = EventVolunteer(
        event=event,
        volunteer=current_user,
        status='registered'
    )
    db.session.add(registration)
    db.session.commit()
    
    # Send WhatsApp message
    if current_user.whatsapp_number:
        try:
            # Format the number to WhatsApp format
            to_whatsapp = f"whatsapp:{current_user.whatsapp_number}"
            
            # Create message using template
            message = twilio_client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                content_sid=TWILIO_CONTENT_SID,
                content_variables=json.dumps({
                    "1": event.date.strftime('%B %d, %Y'),
                    "2": event.time,
                    "3": event.title,
                    "4": event.whatsapp_group_link
                }),
                to=to_whatsapp
            )
            flash(f'Successfully registered! WhatsApp confirmation sent to {current_user.whatsapp_number}', 'success')
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            flash(f'Successfully registered! Join the WhatsApp group: {event.whatsapp_group_link}', 'success')
    else:
        flash('Successfully registered! Please add your WhatsApp number in your profile to receive group updates.', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 