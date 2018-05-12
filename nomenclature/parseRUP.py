from umo.models import EduProg, Discipline, DisciplineDetails, Profile, Kafedra
import xml.etree.ElementTree as ET

def parseRUP(fiit_14):
    tree = ET.parse('upload/fiit_14.xml')
    root = tree.getroot()

    specialization = root[0][0][3][0] #тэг Специальность получить наз спец
    spec_name = ' '.join(specialization.get('Название').split()[1:])

    profil = root[0][0][3][1] #тэг Спец ном2 получить профиль
    profil_name = ' '.join(profil.get('Название').split()[1:])
    print(profil_name)

    qual = root[0][0][7][0] #тэг Квалификация получить квалиф и уровень
    qual_name = ' '.join(qual.get('Название').split()[1:])
    print(qual_name)

    code = root[0][0] #тэг План получить КодКафедры и  ПоследнийШифр
    code_kaf = code.get('КодКафедры')
    cipher = code.get('ПоследнийШифр')
    print(code_kaf)
    print(cipher)

    for elem in root[0][1]:
        disname = elem.get('Дис')
        kafedra = elem.get('Кафедра')
        #kredit_dis = elem.get('КредитовНаДисцилину')
        #time_zet = elem.get('ЧасовВЗЕТ')
        #smstr_exam = elem.get('СемЭкз')
        for semestr_nom in elem.findall('Сем'):
            if hasattr(semestr_nom, 'Ном'):
                semestr_nom = semestr_nom.get('Ном')
            if hasattr(semestr_nom, 'Лек'):
                lecture = semestr_nom.get('Лек')
            if hasattr(semestr_nom, 'Пр'):
                practice = semestr_nom.get('Пр')
            if hasattr(semestr_nom, 'Лаб'):
                lab = semestr_nom.get('Лаб')
            if hasattr(semestr_nom, 'КСР'):
                ksr = semestr_nom.get('КСР')
            if hasattr(semestr_nom, 'СРС'):
                srs = semestr_nom.get('СРС')

        print(disname, kafedra, semestr_nom, lecture, practice, lab, ksr, srs, spec_name )
        p = EduProg()
        p.cathedra = Kafedra.objects.get(number=kafedra)
        p.save()













#conn.close()