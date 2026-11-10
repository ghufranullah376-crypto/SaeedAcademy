import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
import json

app = create_app()

with app.test_client() as c:
    r = c.get('/')
    print('Homepage:', r.status_code)

    r = c.get('/about')
    print('About:', r.status_code)

    r = c.get('/courses')
    print('Courses:', r.status_code)

    r = c.get('/ceo')
    print('CEO:', r.status_code)

    r = c.get('/contact')
    print('Contact:', r.status_code)

    r = c.get('/admission')
    print('Admission:', r.status_code)

    r = c.get('/api/courses')
    data = json.loads(r.data)
    print('API /api/courses:', r.status_code, '| courses count:', len(data.get('courses', [])))

    r = c.get('/admin/login')
    print('Admin Login:', r.status_code)

    r = c.post('/api/admin/login',
               data=json.dumps({'username': 'admin', 'password': 'admin123'}),
               content_type='application/json')
    data = json.loads(r.data)
    print('Admin API Login:', r.status_code, '| success:', data.get('success'))

    r = c.post('/api/admissions',
               data=json.dumps({
                   'student_name': 'Ahmad Test',
                   'guardian_name': 'Father Test',
                   'phone': '03001234567',
                   'course': 'English Language Course',
                   'qualification': 'Matric',
                   'address': 'Mandi Bakakhel, Wazir'
               }),
               content_type='application/json')
    data = json.loads(r.data)
    print('POST /api/admissions:', r.status_code, '| success:', data.get('success'))

    r = c.post('/api/contact',
               data=json.dumps({
                   'name': 'Test User',
                   'phone': '03001234567',
                   'subject': 'Test Subject',
                   'message': 'This is a test message for the contact form.'
               }),
               content_type='application/json')
    data = json.loads(r.data)
    print('POST /api/contact:', r.status_code, '| success:', data.get('success'))

print('\nAll tests completed.')
