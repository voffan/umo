from django.core.exceptions import ValidationError, FieldError
from django.db import IntegrityError
from django.test import TestCase
from hours.import_data import get_qualification, get_edu_level, add_institute, add_cathedra, add_edu_program, \
    add_course, add_supervision_hours, add_practice_hours, add_other_hours, add_contingent, add_group_student, \
    group_student_form
from umo.models import EduOrg, Kafedra, Year, Group, Specialization, EduProgram, Profile, Discipline, Semester, \
    Position, Teacher, EduPeriod
from hours.models import DisciplineSetting, SupervisionHours, PracticeHours, OtherHours
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
        imi = EduOrg()

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
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

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

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        # sync_models.PlnGroupStud.objects.all().delete()

    def test_1(self):
        k = Kafedra.objects.get()
        spec_code = '02.03.02'
        year = Year.objects.get()

        result = add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
            id_pln__id_dop__id_institute=1118,
            id_pln__id_dop__id_spec__code=spec_code,
            id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

        self.assertEqual(result.specialization, Specialization.objects.get())
        self.assertEqual(result.profile, Profile.objects.get())
        self.assertEqual(result.year, year)
        self.assertEqual(result.cathedra, k)

    def test_2(self):
        with self.assertRaises(ValidationError):
            k = 'abc'
            spec_code = '02.03.02'
            year = Year.objects.get()
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_3(self):
        with self.assertRaises(ValidationError):
            k = Kafedra.objects.get()
            spec_code = '02.03.02'
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
            spec_code = '02.03.02'
            year = 'abc'
            add_edu_program(k, 38, year, sync_models.PlnGroupStud.objects.filter(
                id_pln__id_dop__id_institute=1118,
                id_pln__id_dop__id_spec__code=spec_code,
                id_pln__datebegin__gte=datetime.date(year.year, 9, 1).strftime('%Y-%m-%d')))

    def test_6(self):
        with self.assertRaises(ValidationError):
            k = None
            spec_code = '02.03.02'
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
            spec_code = '02.03.02'
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

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'М-ИВТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

        s = Semester()
        s.name = "8"

        d = Discipline()
        d.Name = "Разработка мобильных приложений"
        d.code = "Б1.В.ДВ.03.01"
        d.program = edu
        d.save()
        dd = DisciplineSetting()
        dd.Credit = 0
        dd.Lecture = 1
        dd.Practice = 1
        dd.Lab = 1
        dd.KSR = 1
        dd.SRS = 1
        dd.semester = s
        dd.discipline = d

    @classmethod
    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.objects.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()

    def test_1(self):
        g = Group.objects.get()
        k = Kafedra.objects.get()
        dd = DisciplineSetting().objects.get()
        result = add_course(g, k, dd, 1, 1, 1, 1, 1)
        self.assertEqual(result.group, g)
        self.assertEqual(result.k, k)
        self.assertEqual(result.dd, dd)
        self.assertEqual(result.value_lecture, 1)
        self.assertEqual(result.value_practice, 1)
        self.assertEqual(result.value_lab, 1)
        self.assertEqual(result.value_control, 1)
        self.assertEqual(result.value_SRS, 1)
        #TODO спросить про это

    def test_2(self):
        with self.assertRaises(ValidationError):
            g = 'abc'
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_3(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = 'abc'
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_4(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = 'abc'
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_5(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 'abc', 1, 1, 1, 1)

    def test_6(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 'abc', 1, 1, 1)

    def test_7(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 'abc', 1, 1)

    def test_8(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 'abc', 1)

    def test_9(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, 'abc')

    def test_10(self):
        with self.assertRaises(ValidationError):
            g = None
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_11(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = None
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_12(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = None
            add_course(g, k, dd, 1, 1, 1, 1, 1)

    def test_13(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, None, 1, 1, 1, 1)

    def test_14(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, None, 1, 1, 1)

    def test_15(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, None, 1, 1)

    def test_16(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, None, 1)

    def test_17(self):
        with self.assertRaises(ValidationError):
            g = Group.objects.get()
            k = Kafedra.objects.get()
            dd = DisciplineSetting().objects.get()
            add_course(g, k, dd, 1, 1, 1, 1, None)
            #TODO Спросить, что делать с контролями


class AddSupervisionHours(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        p = Position()
        p.name = 'старший преподаватель'
        p.rate = 1

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        t = Teacher()
        t.position = p
        t.cathedra = k
        t.title = 0

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

        # period = EduPeriod()
        # period.begin_year = y
        # period.end_year = y
        # period.active = True
        #
        # superv = SupervisionHours
        # superv.teacher = t
        # superv.group = g
        # superv.students = 15
        # superv.supervision_type = 1
        # superv.hours = 10
        # superv.edu_period = period
        # superv.cathedra = k
        #TODO Спросить про случаи, когда создвать не нужно



    @classmethod
    def tearDownClass(cls):
        Position.objects.all().delete()
        Teacher.objects.all().delete()
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.objects.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()
        # SupervisionHours.objects.all().delete()
        # EduPeriod.objects.all().delete()

    def test_1(self):
        teacher = Teacher.objects.get()
        group = Group.objects.get()
        cathedra = Kafedra.objects.get()
        supervision_type = 1
        superv = None
        result = add_supervision_hours(teacher, group, cathedra, supervision_type, superv)
        self.assertEqual(result.teacher, teacher)
        self.assertEqual(result.group, group)
        self.assertEqual(result.cathedra, cathedra)
        self.assertEqual(result.supervision_type, supervision_type)
        self.assertEqual(result.superv, superv)

    def test_2(self):
        with self.assertRaises(ValidationError):
            teacher = 'abc'
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_3(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = 'abc'
            cathedra = Kafedra.objects.get()
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_4(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = 'abc'
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_5(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            supervision_type = 'abc'
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_6(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            supervision_type = 1
            superv = 'abc'
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_7(self):
        with self.assertRaises(ValidationError):
            teacher = None
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_8(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = None
            cathedra = Kafedra.objects.get()
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_9(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = None
            supervision_type = 1
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)

    def test_10(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            supervision_type = None
            superv = None
            add_supervision_hours(teacher, group, cathedra, supervision_type, superv)


class AddPracticeHours(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        p = Position()
        p.name = 'старший преподаватель'
        p.rate = 1

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        t = Teacher()
        t.position = p
        t.cathedra = k
        t.title = 0

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

        # period = EduPeriod()
        # period.begin_year = y
        # period.end_year = y
        # period.active = True
        #
        # practice = PracticeHours()
        # practice.teacher = t
        # practice.group = g
        # practice.students = 15
        # practice.practice_type = 1
        # practice.hours = 10
        # practice.edu_period = period
        # practice.cathedra = k

    @classmethod
    def tearDownClass(cls):
        Position.objects.all().delete()
        Teacher.objects.all().delete()
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.objects.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()
        # PracticeHours.objects.all().delete()
        # EduPeriod.objects.all().delete()

    def test_1(self):
        teacher = Teacher.objects.get()
        group = Group.objects.get()
        cathedra = Kafedra.objects.get()
        practice_type = 1
        practice = None
        result = add_practice_hours(teacher, group, cathedra, practice_type, practice)
        self.assertEqual(result.teacher, teacher)
        self.assertEqual(result.group, group)
        self.assertEqual(result.cathedra, cathedra)
        self.assertEqual(result.practice_type, practice_type)
        self.assertEqual(result.practice, practice)

    def test_2(self):
        with self.assertRaises(ValidationError):
            teacher = 'abc'
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_3(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = 'abc'
            cathedra = Kafedra.objects.get()
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_4(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = 'abc'
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_5(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            practice_type = 'abc'
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_6(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            practice_type = 1
            practice = 'abc'
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_7(self):
        with self.assertRaises(ValidationError):
            teacher = None
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_8(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = None
            cathedra = Kafedra.objects.get()
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_9(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = None
            practice_type = 1
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)

    def test_10(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            practice_type = None
            practice = None
            add_practice_hours(teacher, group, cathedra, practice_type, practice)


class AddOtherHours(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        p = Position()
        p.name = 'старший преподаватель'
        p.rate = 1

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        t = Teacher()
        t.position = p
        t.cathedra = k
        t.title = 0

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

        # period = EduPeriod()
        # period.begin_year = y
        # period.end_year = y
        # period.active = True
        #
        # other = OtherHours()
        # other.teacher = t
        # other.group = g
        # other.students = 15
        # other.other_type = 1
        # other.hours = 10
        # other.edu_period = period
        # other.cathedra = k

    @classmethod
    def tearDownClass(cls):
        Position.objects.all().delete()
        Teacher.objects.all().delete()
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.objects.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()
        # OtherHours.objects.all().delete()
        # EduPeriod.objects.all().delete()

    def test_1(self):
        teacher = Teacher.objects.get()
        group = Group.objects.get()
        cathedra = Kafedra.objects.get()
        other_type = 1
        other = None
        result = add_other_hours(teacher, group, cathedra, other_type, other)
        self.assertEqual(result.teacher, teacher)
        self.assertEqual(result.group, group)
        self.assertEqual(result.cathedra, cathedra)
        self.assertEqual(result.other_type, other_type)
        self.assertEqual(result.other, other)

    def test_2(self):
        with self.assertRaises(ValidationError):
            teacher = 'abc'
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_3(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = 'abc'
            cathedra = Kafedra.objects.get()
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_4(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = 'abc'
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_5(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            other_type = 'abc'
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_6(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            other_type = 1
            other = 'abc'
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_7(self):
        with self.assertRaises(ValidationError):
            teacher = None
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_8(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = None
            cathedra = Kafedra.objects.get()
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_9(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = None
            other_type = 1
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)

    def test_10(self):
        with self.assertRaises(ValidationError):
            teacher = Teacher.objects.get()
            group = Group.objects.get()
            cathedra = Kafedra.objects.get()
            other_type = None
            other = None
            add_other_hours(teacher, group, cathedra, other_type, other)


class AddContingent(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()

    def test_1(self):
        group = Group.objects.get()
        name_group = 'ФИИТ-22'
        subgroup_number = 1
        total = 20
        edu_type = 1
        result = add_contingent(group, name_group, subgroup_number, total, edu_type)
        self.assertEqual(result.group, group)
        self.assertEqual(result.name_group, name_group)
        self.assertEqual(result.subgroup_number, subgroup_number)
        self.assertEqual(result.total, total)
        self.assertEqual(result.edu_type, edu_type)

    def test_2(self):
        with self.assertRaises(ValidationError):
            group = 'abc'
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_3(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 123
            subgroup_number = 1
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_4(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 'abc'
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_5(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 'abc'
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_6(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = 'abc'
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_7(self):
        with self.assertRaises(ValidationError):
            group = None
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_8(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = None
            subgroup_number = 1
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_9(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = None
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_10(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 100
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_11(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = -1
            total = 20
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_12(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = None
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_13(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = -1
            edu_type = 1
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_14(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = None
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_15(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = 100
            add_contingent(group, name_group, subgroup_number, total, edu_type)

    def test_16(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            subgroup_number = 1
            total = 20
            edu_type = -1
            add_contingent(group, name_group, subgroup_number, total, edu_type)


class AddGroupStudent(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()

    def test_1(self):
        group = Group.objects.get()
        name_group = 'ФИИТ-22'
        rf = 1
        rsa = 1
        d = 1
        result = add_group_student(group, name_group, rf, rsa, d)
        self.assertEqual(result.group, group)
        self.assertEqual(result.name_group, name_group)
        self.assertEqual(result.rf, rf)
        self.assertEqual(result.rsa, rsa)
        self.assertEqual(result.d, d)
        #TODO Переделать(функцию внимательно изучить!!!)

    def test_2(self):
        with self.assertRaises(ValidationError):
            group = 'abc'
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_3(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 123
            rf = 1
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_4(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 'abc'
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_5(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 'abc'
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_6(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 1
            d = 'abc'
            add_group_student(group, name_group, rf, rsa, d)

    def test_7(self):
        with self.assertRaises(ValidationError):
            group = None
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_8(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = None
            rf = 1
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_9(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = None
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_10(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = None
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_11(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 1
            d = None
            add_group_student(group, name_group, rf, rsa, d)

    def test_12(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = -1
            rsa = 1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_13(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = -1
            d = 1
            add_group_student(group, name_group, rf, rsa, d)

    def test_14(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            name_group = 'ФИИТ-22'
            rf = 1
            rsa = 1
            d = -1
            add_group_student(group, name_group, rf, rsa, d)


class GroupStudentForm(TestCase):
    @classmethod
    def setUpClass(cls):
        e = EduOrg()
        e.uni = ''
        e.name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
        e.save()

        imi = EduOrg()
        imi.uni = e.name
        imi.name = 'Институт математики и информатики'
        imi.save()

        k = Kafedra()
        k.number = 39
        k.name = 'Информационные технологии'
        k.institution = imi

        y = Year()
        y.year = 2022

        s = Specialization()
        s.name = "Фундаментальная информатика и инфомармационные технологии"
        s.brief_name = "ФИИТ"
        s.code = "02.03.02"
        s.qual = 2
        s.level = 2
        s.save()

        p = Profile()
        p.spec = s
        p.name = "Фундаментальная информатика и информационные технологии"

        edu = EduProgram()
        edu.name = 'abc'
        edu.specialization = s
        edu.profile = p
        edu.year = y
        edu.cathedra = k

        g = Group()
        g.Name = 'ФИИТ-22'
        g.begin_year = y
        g.cathedra = k
        g.program = edu

    def tearDownClass(cls):
        EduOrg.objects.all().delete()
        Kafedra.objects.all().delete()
        Year.objects.all().delete()
        Specialization.all().delete()
        Profile.objects.all().delete()
        EduProgram.objects.all().delete()
        Group.objects.all().delete()

    def test_1(self):
        group = Group.objects.get()
        rf = 1
        rsa = 1
        d = 1
        budget_type = 0
        result = group_student_form(group, rf, rsa, d, budget_type)
        self.assertEqual(result.group, group)
        self.assertEqual(result.rf, rf)
        self.assertEqual(result.rsa, rsa)
        self.assertEqual(result.d, d)
        self.assertEqual(result.budget_type, budget_type)

    def test_2(self):
        with self.assertRaises(ValidationError):
            group = 'abc'
            rf = 1
            rsa = 1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_3(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 'abc'
            rsa = 1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_4(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 'abc'
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_5(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = 'abc'
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_6(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = 1
            budget_type = 'abc'
            group_student_form(group, rf, rsa, d, budget_type)

    def test_7(self):
        with self.assertRaises(ValidationError):
            group = None
            rf = 1
            rsa = 1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_8(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = None
            rsa = 1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_9(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = None
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_10(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = None
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_11(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = 1
            budget_type = None
            group_student_form(group, rf, rsa, d, budget_type)

    def test_12(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = -1
            rsa = 1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_13(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = -1
            d = 1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_14(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = -1
            budget_type = 0
            group_student_form(group, rf, rsa, d, budget_type)

    def test_15(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = 1
            budget_type = -1
            group_student_form(group, rf, rsa, d, budget_type)

    def test_16(self):
        with self.assertRaises(ValidationError):
            group = Group.objects.get()
            rf = 1
            rsa = 1
            d = 1
            budget_type = 99
            group_student_form(group, rf, rsa, d, budget_type)


class ImportStudents(TestCase):
    def test_1(self):
        pass


class GetBeginRowCol(TestCase):
    def test_1(self):
        pass


class ParseContTitle(TestCase):
    def test_1(self):
        pass
