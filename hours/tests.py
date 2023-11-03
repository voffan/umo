from django.core.exceptions import ValidationError
from django.test import TestCase
from hours.import_data import get_qualification, get_edu_level, add_institute
from umo.models import EduOrg


class TestGetQual(TestCase):

    def test_1(self):
        result = get_qualification(3)
        self.assertEqual(result, 2)

    def test_2(self):
        result = get_qualification(4)
        self.assertEqual(result, 3)

    def test_3(self):
        result = get_qualification(5)
        self.assertEqual(result, 1)

    def test_4(self):
        result = get_qualification(22)
        self.assertEqual(result, 1)

    def test_5(self):
        result = get_qualification(23)
        self.assertEqual(result, 4)

    def test_6(self):
        result = get_qualification(24)
        self.assertEqual(result, 5)

    def test_7(self):
        result = get_qualification(16)
        self.assertEqual(result, 8)

    def test_8(self):
        result = get_qualification(0)
        self.assertEqual(result, 0)

    def test_9(self):
        result = get_qualification('abc')
        self.assertEqual(result, 0)


class TestGetLevel(TestCase):

    def test_1(self):
        result = get_edu_level(8)
        self.assertEqual(result, 1)

    def test_2(self):
        result = get_edu_level(12)
        self.assertEqual(result, 1)

    def test_3(self):
        result = get_edu_level(14)
        self.assertEqual(result, 1)

    def test_4(self):
        result = get_edu_level(15)
        self.assertEqual(result, 1)

    def test_5(self):
        result = get_edu_level(19)
        self.assertEqual(result, 1)

    def test_6(self):
        result = get_edu_level(20)
        self.assertEqual(result, 1)

    def test_7(self):
        result = get_edu_level(9)
        self.assertEqual(result, 0)

    def test_8(self):
        result = get_edu_level(0)
        self.assertEqual(result, 2)

    def test_9(self):
        result = get_edu_level('abc')
        self.assertEqual(result, 2)


class TestAddInstitute(TestCase):

    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = None
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()

    def test_1(self):
        inst = {'id': 1118, 'name': "Институт математики и информатики"}
        result = add_institute(inst)
        self.assertEqual(result.name, inst['name'])
        self.assertEqual(result.uni.name, 'Северо-Восточный федеральный университет имени М.К. Аммосова')

    def test_2(self):
        with self.assertRaises(TypeError):
            add_institute({'id': 1119, 'name': ""})

    def test_3(self):
        with self.assertRaises(TypeError):
            add_institute({'id': 1118, 'title': "Институт математики и информатики"})

    def test_4(self):
        with self.assertRaises(TypeError):
            add_institute({'id': 1118, 'name': 1})

    def test_5(self):
        with self.assertRaises(TypeError):
            add_institute({'id': 1118, 'name': 1})
