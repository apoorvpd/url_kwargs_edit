from django.test import Client, TestCase
from django.urls import reverse
from notes_app.models import Diary, Category
from datetime import datetime


class EditNoteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Diary.objects.create(
            note="Test note",
            date_time_issued=datetime.now(),
            day=datetime.now().strftime("%A"),
            category=Category.objects.create(name="Test category")
        )
        self.edit_url = reverse('edit_note', kwargs={'id': self.note.id})

    def test_get(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_project.html')
        self.assertEqual(response.context['note'], self.note)

    def test_post(self):
        data = {
            'note': 'Updated test note',
            'date_issued': '2023-05-04T14:30',
            'category': 'Test category'
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_project.html')
        self.assertEqual(response.context['user_message'], "note updated successfully")
        self.note.refresh_from_db()
        self.assertEqual(self.note.note, 'Updated test note')
        self.assertEqual(self.note.date_time_issued.strftime('%Y-%m-%d %H:%M'), '2023-05-04 14:30')
        self.assertEqual(self.note.day, 'Wednesday')
        self.assertEqual(self.note.category.name, 'Test category')
