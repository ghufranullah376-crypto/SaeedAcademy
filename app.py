import os
from flask import Flask, render_template, send_from_directory, jsonify

from config import config
from models import db
from models.student import Admission
from models.course import Course
from models.contact import ContactMessage
from models.admin import AdminUser


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload directory exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'static', 'uploads')), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

    # Init extensions
    db.init_app(app)

    # Register blueprints
    from routes.admissions import admissions_bp
    from routes.contacts import contacts_bp
    from routes.courses import courses_bp
    from routes.admin import admin_bp

    app.register_blueprint(admissions_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(admin_bp)

    # Global template context
    @app.context_processor
    def inject_global_data():
        return {
            'academy_name': 'Saeed English Language & Computer Academy',
            'academy_full_name': 'Ahmad Saeed English Language and Computer Academy',
            'academy_tagline': 'Learn. Improve. Succeed.',
            'academy_address': 'Habib Rahman Market, Basement Floor, Mandi Bakakhel, Wazir, Pakistan',
            'academy_phone': '0331-9898199',
            'academy_whatsapp': '03319898199',
            'academy_whatsapp_url': 'https://wa.me/923319898199',
            'academy_ceo_name': 'Saeed Wazir'
        }

    # Public page routes
    @app.route('/')
    def index():
        courses = Course.query.order_by(Course.id).all()
        return render_template('index.html', courses=courses)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/courses')
    def courses():
        courses = Course.query.order_by(Course.id).all()
        return render_template('courses.html', courses=courses)

    @app.route('/ceo')
    def ceo():
        return render_template('ceo.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/admission')
    def admission():
        courses = Course.query.order_by(Course.id).all()
        return render_template('admission.html', courses=courses)

    # Favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    # Static uploads route if needed
    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # Initialize DB and seed data
    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data():
    """Seed default admin and courses if they don't exist."""
    # Default admin
    admin = AdminUser.query.filter_by(username='admin').first()
    if not admin:
        admin = AdminUser(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

    # Default courses
    default_courses = [
        {
            'course_name': 'English Language Course',
            'description': 'A comprehensive spoken and written English course designed to help students communicate confidently. Covers grammar, phonetics, accent, conversational fluency, reading comprehension, and business correspondence.',
            'syllabus': 'Module 1: English Grammar Foundations & Vocabulary Building\nModule 2: Spoken English, Pronunciation & Accent Training\nModule 3: Daily Conversation, Public Speaking & Presentation\nModule 4: Reading Comprehension & Analytical Skills\nModule 5: Professional Writing & Email Etiquette\nModule 6: IELTS / Test Preparation & Interview Skills',
            'duration': '3 Months',
            'eligibility': 'Matric or equivalent (Grade 9+)',
            'fee': 'PKR 2,000 / Month',
            'image': '/static/images/academy/poster_english.jpg'
        },
        {
            'course_name': 'DIT Course',
            'description': 'Diploma in Information Technology — Recognized diploma covering computer fundamentals, office automation, database concepts, typing proficiency, and internet networking to prepare students for corporate jobs.',
            'syllabus': 'Module 1: Computer Fundamentals & OS Architecture\nModule 2: Microsoft Word (Professional Documents & Reports)\nModule 3: Microsoft Excel (Formulas, Functions & Data Analysis)\nModule 4: Microsoft PowerPoint (Visual Presentations)\nModule 5: English & Urdu Typing Mastery (InPage)\nModule 6: Computer Networking, Hardware Maintenance & Internet Tools\nModule 7: Practical Lab Projects & Examination',
            'duration': '6 Months',
            'eligibility': 'Matric / Middle with interest in Computers',
            'fee': 'PKR 2,500 / Month',
            'image': '/static/images/academy/ceremony_award1.jpg'
        },
        {
            'course_name': 'CIT Course',
            'description': 'Certificate in Information Technology — Intermediate IT qualification focusing on advanced office software, graphic design foundations (Adobe Photoshop, CorelDRAW), and hardware diagnostics.',
            'syllabus': 'Module 1: Advanced MS Office Productivity Suite\nModule 2: Graphic Design Foundations (Adobe Photoshop)\nModule 3: Vector Graphics & Vector Art (CorelDRAW)\nModule 4: Computer Hardware Troubleshooting & Assembling\nModule 5: Database Basics & Spreadsheets\nModule 6: Capstone Project & Portfolio Submission',
            'duration': '6 Months',
            'eligibility': 'Matriculation or equivalent',
            'fee': 'PKR 3,000 / Month',
            'image': '/static/images/academy/classroom_sitting.jpg'
        },
        {
            'course_name': 'CIT 2.0 Course',
            'description': 'The next-generation advanced computer diploma featuring AutoCAD 2D/3D architectural drafting, modern digital design, web foundations, and professional freelance readiness.',
            'syllabus': 'Module 1: AutoCAD 2D Drafting & Architectural Drawings\nModule 2: AutoCAD 3D Modeling & Rendering\nModule 3: Advanced Adobe Photoshop & Illustrator\nModule 4: Web Design Fundamentals (HTML5 & Modern CSS3)\nModule 5: Multilingual Document Publishing (Urdu InPage)\nModule 6: Freelancing Platforms & Client Project Delivery',
            'duration': '6 Months',
            'eligibility': 'CIT Diploma or Basic Computer Knowledge',
            'fee': 'PKR 3,500 / Month',
            'image': '/static/images/academy/classroom_tutoring.jpg'
        }
    ]

    for course_data in default_courses:
        existing = Course.query.filter_by(course_name=course_data['course_name']).first()
        if not existing:
            course = Course(**course_data)
            db.session.add(course)
        else:
            # ensure image is set
            if not existing.image or 'placeholder' in existing.image:
                existing.image = course_data['image']

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
