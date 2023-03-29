from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Event,Guest
from datetime import datetime

class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name='测试训练营1', address='软件大道',start_time=datetime.now(),limits=1000)
        Event.objects.create(name='测试训练营2', address='软件大道',start_time=datetime.now(),limits=500)

    def test_event_address(self):
        event1=Event.objects.get(name='测试训练营1')
        event2=Event.objects.get(name='测试训练营2')
        self.assertEqual(event1.address,'软件大道')
        self.assertEqual(event2.address,'软件大道')
    def test_event_limits(self):
        event1=Event.objects.get(name='测试训练营1')
        event2=Event.objects.get(name='测试训练营2')
        self.assertEqual(event1.limits,1000)
        self.assertEqual(event2.limits,500)
    def test_address_update(self):
        event1=Event.objects.get(name='测试训练营1')
        event1.address='花神大道'
        event1.save()
        self.assertEqual(event1.address,'花神大道')
    def test_delete(self):
        # 删前列出所有
        event_list1=Event.objects.all()
        event1=Event.objects.get(name='测试训练营1')
        self.assertIn(event1,event_list1)  # 检查
        # 删除
        event1.delete()
        # 删后列出所有
        event_list2=Event.objects.all()
        self.assertNotIn(event1,event_list2)