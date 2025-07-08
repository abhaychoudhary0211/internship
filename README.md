# Event Nainjas - Event Management Platform

Event Nainjas is a comprehensive event management platform that connects event organizers with volunteers. The platform facilitates event discovery, volunteer registration, and event management in a user-friendly environment.

## 🌟 Features

### For Volunteers
- User registration and profile management
- Document verification system
- Event discovery and registration
- WhatsApp group integration for event communication
- Dashboard to track registered events
- Profile photo and document upload

### For Administrators
- Event creation and management
- Volunteer verification system
- Event statistics and analytics
- Registration management
- Document verification
- WhatsApp group management

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug
- **Styling**: Custom CSS with responsive design
- **Communication**: WhatsApp API integration

## 📱 Responsive Design

The platform is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- Print media

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/abhaychoudhary0211/event-nainjas.git
cd event-nainjas
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
FLASK_SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
```

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## 📁 Project Structure

```
event-nainjas/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
├── templates/
├── models.py
├── app.py
├── requirements.txt
└── README.md
```

## 🔒 Security Features

- Password hashing using Werkzeug
- Document verification system
- Secure file upload handling
- Protected admin routes
- Input validation and sanitization

## 📱 Mobile Responsiveness

The platform is optimized for all screen sizes:
- Desktop (>1200px)
- Large tablets (992px-1200px)
- Tablets (768px-992px)
- Mobile phones (<768px)
- Small mobile phones (<576px)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

Designed & Developed with ❤️ by [Abhay Choudhary](https://github.com/abhaychoudhary0211)

## 🙏 Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- All contributors and supporters 