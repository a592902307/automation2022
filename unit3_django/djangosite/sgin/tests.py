from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Event,Guest
from datetime import datetime

class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name='����ѵ��Ӫ1', address='������',start_time=datetime.now(),limits=1000)
        Event.objects.create(name='����ѵ��Ӫ2', address='������',start_time=datetime.now(),limits=500)

    def test_event_address(self):
        event1=Event.objects.get(name='����ѵ��Ӫ1')
        event2=Event.objects.get(name='����ѵ��Ӫ2')
        self.assertEqual(event1.address,'������')
        self.assertEqual(event2.address,'������')
    def test_event_limits(self):
        event1=Event.objects.get(name='����ѵ��Ӫ1')
        event2=Event.objects.get(name='����ѵ��Ӫ2')
        self.assertEqual(event1.limits,1000)
        self.assertEqual(event2.limits,500)
    def test_address_update(self):
        event1=Event.objects.get(name='����ѵ��Ӫ1')
        event1.address='������'
        event1.save()
        self.assertEqual(event1.address,'������')
    def test_delete(self):
        # ɾǰ�г�����
        event_list1=Event.objects.all()
        event1=Event.objects.get(name='����ѵ��Ӫ1')
        self.assertIn(event1,event_list1)  # ���
        # ɾ��
        event1.delete()
        # ɾ���г�����
        event_list2=Event.objects.all()
        self.assertNotIn(event1,event_list2)