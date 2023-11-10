from django.core.exceptions import ValidationError, FieldError
from django.db import IntegrityError
from django.test import TestCase
from hours.import_data import get_qualification, get_edu_level, add_institute, add_cathedra, add_edu_program
from umo.models import EduOrg, Kafedra, Year, Group
import synch.models as sync_models
import datetime


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
        with self.assertRaises(ValidationError):
            add_institute({'id': 1119, 'name': None})

    def test_3(self):
        with self.assertRaises(FieldError):
            add_institute({'id': 1118, 'title': "Институт математики и информатики"})

    def test_4(self):
        with self.assertRaises(ValidationError):
            add_institute({'id': 1118, 'name': 1})

    def test_5(self):
        with self.assertRaises(IntegrityError):
            add_institute({'id': 1118, 'name': 1})


class TestAddCathedra(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.name = 'Институт математики и информатики'
        e.save()

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()

    def test_1(self):
        e = EduOrg.objects.get()
        cathedras = {"38": "Информационные технологии"}
        result = add_cathedra(e, 38)
        self.assertEqual(result.institution, e)
        self.assertEqual(result.number, 38)
        self.assertEqual(result.name, cathedras[1])

    def test_2(self):
        e = 'abc'
        with self.assertRaises(ValidationError):
            add_cathedra(e, 38)

    def test_3(self):
        e = EduOrg.objects.get()
        with self.assertRaises(ValidationError):
            add_cathedra(e, 500)

    def test_4(self):
        e = EduOrg.objects.get()
        with self.assertRaises(ValidationError):
            add_cathedra(e, 'abc')

    def test_5(self):
        e = None
        with self.assertRaises(ValidationError):
            add_cathedra(e, 38)

    def test_6(self):
        e = EduOrg.objects.get()
        with self.assertRaises(ValidationError):
            add_cathedra(e, int())


class TestEduProgram(TestCase):

    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = None
        e.name = "Северо-Восточный федеральный университет имени М.К. Аммосова"
        e.save()

        k = Kafedra()
        k.number = 38
        k.name = 'Информационные технологии'
        k.institution = e
        k.save()

        y = Year()
        y.year = 2022
        y.save()

        #TODO Добавить Specialization

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        # sync_models.PlnGroupStud.objects.all().delete()

    def test_1(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = '39.20.01'
            year = Year.objects.get()

            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_2(self):
        with self.assertRaises(ValidationError):
            k = 'abc'
            spec_code = '39.20.01'
            year = Year.objects.get()
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_3(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = '39.20.01'
            year = Year.objects.get()
            add_edu_program(k, 38, year, 'abc')

    def test_4(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = 39
            year = Year.objects.get()
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_5(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = '39.20.01'
            year = 'abc'
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_6(self):
        with self.assertRaises(ValidationError):
            k = None
            spec_code = '39.20.01'
            year = Year.objects.get()
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_7(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = None
            year = Year.objects.get()
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_8(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = '39.20.01'
            year = None
            add_edu_program(k, 38, year.year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_9(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            add_edu_program(k, 38, Year.objects.get().year, None)


class TestAddCourse(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = None
        e.name = "Северо-Восточный федеральный университет имени М.К. Аммосова"
        e.save()

        k = Kafedra()
        k.number = 39
        k.name = 'Информатика и вычислительная техника'
        k.institution = e
        k.save()

        y = Year()
        y.year = 2022

        #TODO Добавить EduProgram

        # g = Group()
        # g.Name = 'М-ИВТ-22'
        # g.begin_year = y
        # g.cathedra = k
        # g.program =

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
