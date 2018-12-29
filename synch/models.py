from django.db import models


class YSUMainModel(models.Model):
    class Meta:
        managed = False
        abstract = True


class PeopleList(YSUMainModel):
    id_people = models.IntegerField(primary_key=True, null=False)
    surname = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    patronymic = models.CharField(max_length=30)
    oldsurname = models.CharField(max_length=30)
    oldname = models.CharField(max_length=30)
    oldpatronymic = models.CharField(max_length=30)
    marriage = models.BooleanField(null=False)
    sex = models.CharField(max_length=1, null=False)
    borndate = models.DateTimeField(null=False)
    bornplace = models.CharField(max_length=100, null=False)
    id_doc = models.SmallIntegerField(null=False)
    docserial = models.CharField(max_length=10, null=False)
    docno = models.CharField(max_length=30, null=False)
    docdistributed = models.CharField(max_length=150, null=False)
    docdate = models.DateTimeField()
    docdepartmentcode = models.CharField(max_length=50)
    id_sitizen = models.SmallIntegerField(null=False)
    photo = models.ImageField()
    other = models.TextField()
    is_webimported = models.BooleanField(null=False)
    id_web = models.IntegerField()
    fio = models.CharField(max_length=96, null=False)
    fio2 = models.CharField(max_length=125)
    msrepl_tran_version = models.CharField(max_length=32, null=False)
    surnamerp = models.CharField(max_length=30)
    namerp = models.CharField(max_length=30)
    patronymicrp = models.CharField(max_length=30)
    id_nationality_old = models.IntegerField()
    id_nationality = models.IntegerField()
    uid = models.IntegerField()
    uid_stat = models.IntegerField()
    uid_sok = models.IntegerField()
    uid_zo = models.IntegerField()
    inn_old = models.BigIntegerField()
    ssn = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)

    class Meta(YSUMainModel.Meta):
        db_table = 'people_List'


class PeoplePln(YSUMainModel):
    id_peoplepln = models.IntegerField(primary_key=True, null=False)
    id_people = models.ForeignKey('PeopleList', db_column='id_people', on_delete=models.CASCADE)
    id_pln = models.ForeignKey('PlnEduProgYear', db_column='id_pln', on_delete=models.CASCADE)
    id_group = models.ForeignKey('PlnGroupStud', db_column='id_group', on_delete=models.CASCADE)
    id_status = models.SmallIntegerField(null=False)
    cardno = models.CharField(max_length=20)
    regno = models.CharField(max_length=30)
    datein = models.DateTimeField()
    dateout = models.DateTimeField()
    id_enrollreason = models.SmallIntegerField()
    diplom_serial = models.CharField(max_length=10)
    diplom_no = models.CharField(max_length=20)
    diplom_date = models.DateTimeField()
    diplom_euroattach = models.BooleanField()
    diplom_subject = models.CharField(max_length=250)
    prev_id_ppln = models.IntegerField()
    changedate = models.DateTimeField()
    enddate = models.DateTimeField()
    id_prikaz = models.IntegerField()
    disable_trg = models.BooleanField(null=False)
    isgotf26 = models.DateTimeField()
    id_consultant = models.CharField(max_length=24)
    no_history = models.BooleanField()
    id_priorityprofile = models.IntegerField()
    transferfrom = models.IntegerField()
    transferto = models.IntegerField()
    is_webimported = models.BooleanField()
    is_school_applicate = models.BooleanField()
    dateagreement = models.DateTimeField()
    custompriority = models.IntegerField()

    class Meta(YSUMainModel.Meta):
        db_table = 'people_Pln'


class PlnEduProg(YSUMainModel):
    id_dop = models.IntegerField(primary_key=True, null=False)
    id_spec = models.ForeignKey('PlnSprSpecializ', db_column='id_spec', on_delete=models.CASCADE)
    id_studyform = models.SmallIntegerField(null=False)
    real_studyform = models.SmallIntegerField(null=False)
    duration = models.CharField(max_length=25)
    id_qualify = models.SmallIntegerField(null=False)
    id_eduprogtype = models.SmallIntegerField(null=False)
    addinfo = models.CharField(max_length=50)
    docprefix = models.CharField(max_length=10)
    rip = models.BooleanField(null=False)
    id_eduqualifylevel = models.SmallIntegerField(null=False)
    id_edupaper = models.SmallIntegerField(null=False)
    id_regdoclicence = models.IntegerField()
    id_regdocattest = models.IntegerField()
    id_regdocaccredit = models.IntegerField()
    id_regdocenable = models.IntegerField()
    id_regdocregister = models.IntegerField()
    id_spr_organization = models.IntegerField(null=False)
    id_foreign_organisation = models.IntegerField()
    id_edutechnol = models.IntegerField(null=False)
    id_edusystem = models.IntegerField(null=False)
    id_eduentertypemin = models.SmallIntegerField(null=False)
    id_studyprogram = models.SmallIntegerField(null=False)
    id_placerealiz = models.IntegerField(null=False)
    id_placepredstav = models.IntegerField(null=False)
    id_addinfo = models.IntegerField(null=False)
    durationrecomend = models.CharField(max_length=5, null=False)
    durationset = models.CharField(max_length=5, null=False)
    id_kafedra = models.CharField(max_length=24)
    id_institute = models.CharField(max_length=24)
    id_realizatflag = models.CharField(max_length=24)
    id_predstavflag = models.CharField(max_length=24)
    isduty = models.BooleanField(null=False)
    durnew = models.IntegerField()
    id_edusphere = models.IntegerField()
    id_gosstandart = models.IntegerField()
    programdescription = models.TextField()

    class Meta(YSUMainModel.Meta):
        db_table = 'pln_EduProg'


class PlnEduProgYear(YSUMainModel):
    id_pln = models.IntegerField(primary_key=True, null=False)
    id_dop = models.ForeignKey('PlnEduProg', db_column='id_dop', on_delete=models.CASCADE)
    id_plany_link = models.CharField(max_length=255)
    year = models.SmallIntegerField(null=False)
    refertotip = models.IntegerField(null=False)
    rip = models.BooleanField(null=False)
    id_statusprog = models.IntegerField(null=False)
    educode = models.CharField(max_length=20, null=False)
    datebegin = models.DateTimeField(null=False)
    dateend = models.DateTimeField(null=False)
    refertoenrollment = models.IntegerField()
    descriptionhtml = models.TextField()

    class Meta(YSUMainModel.Meta):
        db_table = 'pln_EduProgYear'


class PlnGroupStud(YSUMainModel):
    id_group = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=30, null=False)
    number_in_group = models.IntegerField(null=False)
    id_pln = models.ForeignKey('PlnEduProgYear', db_column='id_pln', on_delete=models.CASCADE)
    codestream = models.IntegerField(null=False)
    id_structure = models.IntegerField(null=False)
    rip = models.BooleanField(null=False)
    div_id = models.IntegerField()

    class Meta(YSUMainModel.Meta):
        db_table = 'pln_group_Stud'


class PlnSprSpecializ(YSUMainModel):
    id_spec = models.IntegerField(primary_key=True, null=False)
    id_specialn = models.IntegerField(null=False)
    name = models.CharField(max_length=250, null=False)
    shortname = models.CharField(max_length=20, null=False)
    code = models.CharField(max_length=20, null=False)
    specialn = models.BooleanField()
    spec = models.BooleanField()
    isnapr = models.BooleanField()

    class Meta(YSUMainModel.Meta):
        db_table = 'pln_spr_Specializ'
