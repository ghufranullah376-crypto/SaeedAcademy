import os
import unittest
from app import create_app, db
from models.student import Admission
from models.course import Course
from models.contact import ContactMessage
from models.admin import AdminUser


class SaeedAcademyTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('development')

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    # ── 1. Page Routes Test ───────────────────────────────────
    def test_all_pages_render_successfully(self):
        routes = ['/', '/about', '/courses', '/ceo', '/contact', '/admission', '/admin/login']
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with {res.status_code}")
            self.assertIn(b'Saeed', res.data)

    # ── 2. CEO Photo Test ─────────────────────────────────────
    def test_ceo_photo_installed(self):
        ceo_path = os.path.join(self.app.root_path, 'static', 'images', 'academy', 'ceo.jpg')
        self.assertTrue(os.path.exists(ceo_path), "CEO image file does not exist")
        self.assertGreater(os.path.getsize(ceo_path), 10000, "CEO image file is too small or empty")

    # ── 3. Course API Test ────────────────────────────────────
    def test_courses_api_returns_seeded_courses(self):
        res = self.client.get('/api/courses')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['courses']), 4)
        names = [c['course_name'] for c in data['courses']]
        self.assertIn('English Language Course', names)
        self.assertIn('DIT Course', names)
        self.assertIn('CIT Course', names)
        self.assertIn('CIT 2.0 Course', names)

    # ── 4. Online Admission Submission & Receipt Test ────────
    def test_admission_submission_and_receipt(self):
        # Validation failure on missing fields
        bad_res = self.client.post('/api/admissions', json={'student_name': 'Ali'})
        self.assertEqual(bad_res.status_code, 400)

        # Valid submission
        valid_payload = {
            'student_name': 'Farhan Ullah',
            'father_name': 'Nemat Ullah',
            'phone': '03319898199',
            'whatsapp': '03319898199',
            'course': 'English Language Course',
            'qualification': 'Intermediate (FSc)',
            'institution': 'Govt Degree College Mandi Bakakhel',
            'passing_year': '2024',
            'computer_experience': 'Basic',
            'preferred_timing': 'Evening (4:30 PM - 6:30 PM)',
            'address': 'Main Market, Mandi Bakakhel',
            'city': 'Mandi Bakakhel',
            'district': 'Wazir',
            'date_of_birth': '2005-04-12',
            'gender': 'Male'
        }
        res = self.client.post('/api/admissions', json=valid_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])
        app_no = data['application_number']
        self.assertTrue(app_no.startswith('SELCA-'))

        # Receipt lookup endpoint
        rec_res = self.client.get(f'/api/admissions/receipt/{app_no}')
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.get_json()
        self.assertTrue(rec_data['success'])
        self.assertEqual(rec_data['receipt']['student_name'], 'Farhan Ullah')
        self.assertEqual(rec_data['receipt']['father_name'], 'Nemat Ullah')

    # ── 5. Contact Message Test ───────────────────────────────
    def test_contact_submission(self):
        payload = {
            'name': 'Kamran Khan',
            'phone': '03331234567',
            'subject': 'Admission Enquiry for DIT',
            'message': 'Assalam o Alaikum, I would like to know if classes are available on weekend.'
        }
        res = self.client.post('/api/contact', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])

    # ── 6. Admin Authentication & Management Test ─────────────
    def test_admin_security_and_management(self):
        # 6a. Ensure at least one admission exists
        if Admission.query.count() == 0:
            test_adm = Admission(
                application_number='SELCA-2026-9999',
                student_name='Test Student',
                father_name='Test Father',
                phone='03319898199',
                address='Mandi Bakakhel',
                qualification='Matric'
            )
            db.session.add(test_adm)
            db.session.commit()

        # 6b. Unauthorized access should be blocked
        unauth_res = self.client.get('/api/admin/admissions')
        self.assertEqual(unauth_res.status_code, 401)

        # 6c. Valid login
        good_login = self.client.post('/api/admin/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(good_login.status_code, 200)
        self.assertTrue(good_login.get_json()['success'])

        # 6d. Authorized dashboard stats
        stats_res = self.client.get('/api/admin/dashboard')
        self.assertEqual(stats_res.status_code, 200)
        stats = stats_res.get_json()['stats']
        self.assertGreaterEqual(stats['total_admissions'], 1)

        # 6e. Admin fetch admissions list
        adm_list_res = self.client.get('/api/admin/admissions')
        self.assertEqual(adm_list_res.status_code, 200)
        admissions = adm_list_res.get_json()['admissions']
        self.assertGreaterEqual(len(admissions), 1)

        # 6f. Admin update admission status
        first_adm_id = admissions[0]['id']
        upd_res = self.client.put(f'/api/admin/admissions/{first_adm_id}', json={
            'admission_status': 'Approved'
        })
        self.assertEqual(upd_res.status_code, 200)
        self.assertEqual(upd_res.get_json()['admission']['admission_status'], 'Approved')

        # 6g. Admin course creation, update and delete
        new_course_res = self.client.post('/api/admin/courses', json={
            'course_name': 'Web Development Bootcamp',
            'description': 'Full-stack web development with Python and HTML/CSS.',
            'duration': '4 Months',
            'fee': 'PKR 4,000 / Month',
            'eligibility': 'Matric or CIT',
            'syllabus': 'HTML, CSS, JS, Flask, SQLite'
        })
        self.assertEqual(new_course_res.status_code, 201)
        created_course_id = new_course_res.get_json()['course']['id']

        # Update course
        upd_course_res = self.client.put(f'/api/admin/courses/{created_course_id}', json={
            'fee': 'PKR 4,500 / Month'
        })
        self.assertEqual(upd_course_res.status_code, 200)

        # Delete course
        del_course_res = self.client.delete(f'/api/admin/courses/{created_course_id}')
        self.assertEqual(del_course_res.status_code, 200)

        # 6h. Admin logout
        logout_res = self.client.post('/api/admin/logout')
        self.assertEqual(logout_res.status_code, 200)

        # 6i. After logout, access is revoked
        after_logout = self.client.get('/api/admin/admissions')
        self.assertEqual(after_logout.status_code, 401)


if __name__ == '__main__':
    unittest.main()
