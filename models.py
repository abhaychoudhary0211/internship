from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Volunteer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    photo = db.Column(db.String(200))  # Path to passport size photo
    document_type = db.Column(db.String(20), nullable=False)  # Aadhar, PAN, DL, Voter ID
    document_number = db.Column(db.String(50), nullable=False)
    document_front = db.Column(db.String(200))  # Path to document front photo
    document_back = db.Column(db.String(200))  # Path to document back photo
    whatsapp_number = db.Column(db.String(15), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    registered_events = db.relationship('Event', secondary='event_volunteer', backref='registered_volunteers')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))
    whatsapp_group_link = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EventVolunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, confirmed, completed
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('Event', backref=db.backref('volunteer_registrations', cascade='all, delete-orphan'))
    volunteer = db.relationship('Volunteer', backref=db.backref('event_registrations', cascade='all, delete-orphan')) 