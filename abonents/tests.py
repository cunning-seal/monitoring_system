from django.test import TestCase
from abonents.models import Abonent

class AbonentTestCase(TestCase):
    def setUp(self):
        Abonent.objects.create(computer_id=5050,name="Device_1")
        Abonent.objects.create(computer_id=6060, name="Device_2")
        try:
            Abonent.objects.create(computer_id="any string")
        except:
            print("Bad information passed to computer_id")

    def check(self):
        a = Abonent.objects.get(computer_id=5050)
        b = Abonent.objects.get(computer_id=6060)
        self.assertEqual(a.name, "Device_1")
        self.assertEqual(b.name, "Device_2")

# Create your tests here.
