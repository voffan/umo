from umo.models import EduOrg, Kafedra, EduProg, Specialization, Discipline, DisciplineDetails, Profile, Year, Semestr, Qual, Level
import xml.etree.ElementTree as ET



def parseRUP(filename):
    #name_file_xml = os.path.join('upload', filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    specialization = root[0][0][3][0] #тэг Специальность получение названия спец
    spec_name = ' '.join(specialization.get('Название').split()[1:])
    print(spec_name)

    profil = root[0][0][3][1] #тэг Специальность ном2 получения названия профиль
    profil_name = ' '.join(profil.get('Название').split()[1:])
    print(profil_name)

    qual = root[0][0][7][0] #тэг Квалификация получения квалиф
    qual_name = ' '.join(qual.get('Название').split()[1:])
    print(qual_name)

    code = root[0][0] #тэг План получения КодКафедры и ПоследнийШифр
    name_institute = code.get('ИмяВуза2')
    name_university = code.get('ИмяВуза')
    code_kaf = code.get('КодКафедры')
    cipher = ''.join(str(i) for i in (code.get('ПоследнийШифр')).split('.'))
    yearp = code.get('ГодНачалаПодготовки')
    print(name_institute)
    print(name_university)
    print(code_kaf)
    print(cipher)
    print(yearp)

    name_inst = EduOrg.objects.filter(name=name_institute).first()
    if name_inst is None:
        name_inst = EduOrg()
        name_inst.name = name_institute
        name_inst.uni = EduOrg.objects.filter(name__icontains='свфу').first()
        name_inst.save()

    kaf = Kafedra.objects.filter(number=code_kaf).first()
    if kaf is None:
        kaf = Kafedra()
        kaf.number = code_kaf
        kaf.name = Kafedra.objects.filter(name='Информационные технологии').first()
        kaf.institution = name_inst
        kaf.save()

    e = EduProg()
    sp = EduProg.objects.filter(specialization__name=spec_name).first()
    if sp is None:
        sp = Specialization()
        sp.name = spec_name
        sp.briefname = ""
        sp.code = cipher
        qual = Qual()
        qual.name = qual_name
        qual.save()
        sp.qual = qual
        level = Level()
        level.name = ""
        level.save()
        sp.level = level
        sp.save()
    e.specialization = sp

    profil = EduProg.objects.filter(profile__name=profil_name).first()
    if profil is None:
        profil = Profile()
        profil.name = profil_name
        profil.save()
    e.profile = profil

    year = EduProg.objects.filter(year__year=yearp).first()
    if year is None:
        year = Year()
        year.year = yearp
        year.save()
    e.year = year
    #print(kaf.id)
    e.cathedra = kaf
    e.save()

    for elem in root[0][1]:
        disname = elem.get('Дис')
        code_dis = ''.join(str(i) for i in (elem.get('ИдетификаторДисциплины')).split('.'))
        time_zet = elem.get('ЧасовВЗЕТ')
        print(disname, code_dis, time_zet)

        dis = Discipline.objects.filter(Name=disname).first()
        if dis is None:
            dis = Discipline()
            dis.Name = disname
            dis.code = code_dis
            dis.program = e
            dis.lecturer = ""
            dis.control = ""
            dis.save()

        for semestr_nom in elem.findall('Сем'):
            if hasattr(semestr_nom, 'Ном'):
                semestr_nom = semestr_nom.get('Ном')
                print(semestr_nom)
            if hasattr(semestr_nom, 'Лек'):
                lecture = semestr_nom.get('Лек')
                print(lecture)
            if hasattr(semestr_nom, 'Пр'):
                practice = semestr_nom.get('Пр')
                print(practice)
            if hasattr(semestr_nom, 'Лаб'):
                lab = semestr_nom.get('Лаб')
                print(lab)
            if hasattr(semestr_nom, 'КСР'):
                ksr = semestr_nom.get('КСР')
                print(ksr)
            if hasattr(semestr_nom, 'СРС'):
                srs = semestr_nom.get('СРС')
                print(srs)
            if hasattr(semestr_nom, 'ЗЕТ'):
                zet = semestr_nom.get('ЗЕТ')
                print(zet)

            details = DisciplineDetails.objects.filter(Credit=time_zet).first()
            if details is None:
                details = DisciplineDetails()
                details.Credit = time_zet
                details.Lecture = lecture
                details.Practice = practice
                details.Lab = lab
                details.KSR = ksr
                details.SRS = srs
                details.control_hours = zet
                semestr = Semestr()
                semestr.name = semestr_nom
                semestr.save()
                details.semestr = semestr
                details.subject = dis
                details.save()







