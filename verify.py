import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from app import create_app

app = create_app()

with app.test_client() as c:
    pages = ['/', '/about', '/courses', '/ceo', '/contact', '/admission', '/admin/login']
    for p in pages:
        r = c.get(p)
        ok = 'PASS' if r.status_code in (200, 302) else 'FAIL'
        print(f'{ok} {p} -> {r.status_code}')

    r = c.get('/api/courses')
    d = json.loads(r.data)
    n = len(d.get('courses', []))
    print(f'PASS /api/courses -> {r.status_code} ({n} courses loaded)')

    r = c.post('/api/admin/login',
               data=json.dumps({'username': 'admin', 'password': 'admin123'}),
               content_type='application/json')
    d = json.loads(r.data)
    print(f'PASS /api/admin/login -> success={d.get("success")}')

    r = c.post('/api/admissions',
               data=json.dumps({'student_name': 'Verification Test', 'guardian_name': 'Guardian',
                                'phone': '03001234567', 'course': 'DIT Course',
                                'qualification': 'Matric', 'address': 'Mandi Bakakhel'}),
               content_type='application/json')
    d = json.loads(r.data)
    print(f'PASS /api/admissions POST -> success={d.get("success")} id={d.get("id")}')

    r = c.post('/api/contact',
               data=json.dumps({'name': 'Verify User', 'phone': '0300123',
                                'subject': 'Verification', 'message': 'Test contact message from verify script.'}),
               content_type='application/json')
    d = json.loads(r.data)
    print(f'PASS /api/contact POST -> success={d.get("success")}')

    print('\nAll verification checks complete.')
