from django.db import transaction
from umo.models import EduOrg, Kafedra, EduProg, Specialization, Discipline, \
    DisciplineDetails, Profile, Year, Semestr, Teacher, Control, Position, ControlType
from umo.objgens import check_edu_org
import xml.etree.ElementTree as ET
import re


def get_qualification(name):
    name = name.lower()
    if 'специали' in name:
        return 1
    elif 'бакалавр' in name:
        if 'академ' in name:
            return 4
        elif 'приклад' in name:
            return 5
        return 2
    elif 'магистр' in name:
        return 3
    return 0


def get_education_level(name):
    name = name.lower()
    if 'спо' in name:
        return 1
    elif 'впо' in name:
        return 2
    return 0


@transaction.atomic
def parseRUP(filename):
    #name_file_xml = os.path.join('upload', filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    title = root[0][0]
    #Уровень образования
    level = root[0].get('УровеньОбразования')
    #тэг Специальность получение названия спец
    specs = title.find('Специальности')
    spec_name = ' '.join(specs[0].get('Название').split()[1:])
    #тэг Специальность ном2 получения названия профиль
    if len(specs) > 1:
        profile_name = ' '.join(specs[1].get('Название').split()[1:])
    else:
        profile_name = 'Общий'
    #qual = root[0][0][7][0] #тэг Квалификация получения квалиф
    qual_name = title.find('Квалификации')[0].get('Название')
    #code = root[0][0] #тэг План получения КодКафедры и ПоследнийШифр
    name_institute = title.get('ИмяВуза2')
    name_university = re.findall('(?<=\").*(?=\")',title.get('ИмяВуза'))
    if len(name_university) > 1:
        name_university = name_university[0]
    elif len(re.findall('(?<=«).*(?=»)',title.get('ИмяВуза')))>0:
        name_university = re.findall('(?<=«).*(?=»)',title.get('ИмяВуза'))
    else:
        name_university = title.get('ИмяВуза')
    code_kaf = title.get('КодКафедры')
    code = title.get('ПоследнийШифр')
    yearp = title.get('ГодНачалаПодготовки')

    institute = check_edu_org(name_institute, name_university)

    kaf, created = Kafedra.objects.get_or_create(number=code_kaf, defaults={'name':'', 'institution':institute})
    year, created = Year.objects.get_or_create(year=yearp)

    sp, created = Specialization.objects.get_or_create(code=code, defaults={
        'name': spec_name,
        'briefname': '',
        'qual': get_qualification(qual_name),
        'level': get_education_level(level)
    })
    profile, created = Profile.objects.get_or_create(name=profile_name, defaults={'spec':sp})

    edu_prog, created = EduProg.objects.get_or_create(specialization=sp, profile=profile, cathedra=kaf, year=year)

    for elem in root[0][1]:
        disname = elem.get('Дис')
        code_dis = elem.get('ИдетификаторДисциплины')

        dis, created = Discipline.objects.get_or_create(Name=disname, code=code_dis, program=edu_prog)

        for details in elem.findall('Сем'):
            #if details is ('Ном' and 'Пр' and 'КСР' and 'СРС' and 'ЗЕТ') or ('Ном' and 'КСР' and 'СРС' and 'ЗЕТ') or ('Ном' and 'Лек' and 'Пр' and 'КСР' and 'СРС' and 'ЗЕТ') or ('Ном' and 'Лек' and 'Пр' and 'ЗЕТ') or ('Ном' and 'Лек' and 'Лаб' and 'КСР' and 'СРС' and 'ЗЕТ') or ('Ном' and 'Лек' and 'Лаб' and 'Пр' and 'КСР' and 'СРС' and 'ЗЕТ') or ('Ном' and 'Пр') or ('Ном' and 'СРС'):
            data = {'101':0,'102':0,'103':0,'106':0,'107':0,'108':0}
            total_h = 0
            for vz in details.findall('VZ'):
                if 'H' in vz.attrib.keys():
                    data[vz.get("ID")] = int(vz.get('H'))
                    total_h += int(vz.get('H'))
            if total_h < 1:
                continue

            #semestr_nom = '1'
            semestr_nom = details.get('Ном','1')
            zet = details.get('ЗЕТ','1')
            z = details.get('Зач', None)
            exam = details.get('Экз', None)
            zO = details.get('ЗачО', None)
            CW = details.get('КР', None)

            smstr, created = Semestr.objects.get_or_create(name=semestr_nom)
            defaults={'Credit':int(zet),
                                                                  'Lecture' : data['101'],
                                                                  'Practice' : data['103'],
                                                                  'Lab' : data['102'],
                                                                  'KSR' : data['106'],
                                                                  'SRS' : data['107']}
            d, created = DisciplineDetails.objects.get_or_create(discipline=dis,
                                                        semestr=smstr,
                                                        defaults=defaults)
            if z is not None:
                control_type, created = ControlType.objects.get_or_create(name='Зачет')
                c, created = Control.objects.update_or_create(discipline_detail=d, controltype=control_type, defaults={'control_hours': data['108']})
            if exam is not None:
                control_type, created = ControlType.objects.get_or_create(name='Экзамен')
                c, created = Control.objects.update_or_create(discipline_detail=d, controltype=control_type, defaults={'control_hours': data['108']})
            if zO is not None:
                control_type, created = ControlType.objects.get_or_create(name='Зачет с оценкой')
                c, created = Control.objects.update_or_create(discipline_detail=d, controltype=control_type, defaults={'control_hours': data['108']})
            if CW is not None:
                control_type, created = ControlType.objects.get_or_create(name='Курсовая работа')
                c, created = Control.objects.update_or_create(discipline_detail=d, controltype=control_type, defaults={'control_hours': data['108']})
