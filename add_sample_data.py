from app import app, db
from models import Event, Volunteer, EventVolunteer
from datetime import datetime, timedelta

def add_sample_events():
    # Add past events
    past_events = [
        Event(
            title="Diwali Festival Celebration 2023",
            description="A grand celebration of Diwali with cultural performances, food stalls, and fireworks. Volunteers helped with crowd management, cultural program coordination, and safety measures. The event was a huge success with over 5000 attendees.",
            date=datetime.now() - timedelta(days=30),
            time="6:00 PM - 10:00 PM",
            location="Central Park, Jaipur",
            image="images/events/diwali.jpg",
            whatsapp_group_link="https://chat.whatsapp.com/diwali2023"
        ),
        Event(
            title="Jaipur Marathon 2023",
            description="Annual marathon event with 5000+ participants. Volunteers helped with water stations, medical aid, and route guidance. The event featured multiple categories including full marathon, half marathon, and 5K run.",
            date=datetime.now() - timedelta(days=45),
            time="5:00 AM - 11:00 AM",
            location="SMS Stadium, Jaipur",
            image="images/events/marathon.jpg",
            whatsapp_group_link="https://chat.whatsapp.com/marathon2023"
        ),
        Event(
            title="Art Exhibition: Modern Masters",
            description="A month-long exhibition showcasing works of local artists. Volunteers assisted with exhibition setup, visitor guidance, and sales. The event featured paintings, sculptures, and digital art from 50+ artists.",
            date=datetime.now() - timedelta(days=60),
            time="10:00 AM - 6:00 PM",
            location="Jawahar Kala Kendra",
            image="images/events/art.jpg",
            whatsapp_group_link="https://chat.whatsapp.com/art2023"
        ),
        Event(
            title="Tech Startup Meetup",
            description="Networking event for tech entrepreneurs and startups. Volunteers helped with registration, event coordination, and technical support. Featured panel discussions and startup pitches.",
            date=datetime.now() - timedelta(days=75),
            time="2:00 PM - 7:00 PM",
            location="Jaipur Tech Hub",
            image="images/events/tech.jpg",
            whatsapp_group_link="https://chat.whatsapp.com/tech2023"
        ),
        Event(
            title="Heritage Walk: Old City",
            description="Guided heritage walk through the Pink City's historic lanes. Volunteers assisted with group management, photography, and cultural information sharing. Covered major landmarks and hidden gems.",
            date=datetime.now() - timedelta(days=90),
            time="7:00 AM - 10:00 AM",
            location="City Palace, Jaipur",
            image="images/events/heritage.jpg",
            whatsapp_group_link="https://chat.whatsapp.com/heritage2023"
        )
    ]
    
    # Add events to database
    for event in past_events:
        db.session.add(event)
    
    # Create some sample volunteers and registrations
    sample_volunteers = [
        Volunteer(
            name="Rahul Sharma",
            phone="+919876543210",
            email="rahul@example.com",
            whatsapp_number="+919876543210",
            document_type="Aadhar",
            document_number="123456789012",
            is_verified=True
        ),
        Volunteer(
            name="Priya Patel",
            phone="+919876543211",
            email="priya@example.com",
            whatsapp_number="+919876543211",
            document_type="PAN",
            document_number="ABCDE1234F",
            is_verified=True
        ),
        Volunteer(
            name="Amit Kumar",
            phone="+919876543212",
            email="amit@example.com",
            whatsapp_number="+919876543212",
            document_type="DL",
            document_number="DL123456789",
            is_verified=True
        )
    ]
    
    for volunteer in sample_volunteers:
        volunteer.set_password("password123")
        db.session.add(volunteer)
    
    db.session.commit()
    
    # Add registrations for past events
    for event in past_events:
        for volunteer in sample_volunteers:
            registration = EventVolunteer(
                event=event,
                volunteer=volunteer,
                status='completed',
                registered_at=event.date - timedelta(days=7)
            )
            db.session.add(registration)
    
    db.session.commit()

if __name__ == '__main__':
    add_sample_events() 