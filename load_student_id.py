from umo_project.wsgi import application
from umo.models import GroupList

students = open('students.csv').read().split('\n')
students = [student.split(';') for student in students]

for student in students:
    fio = student[1] + ' ' + student[2]
    if len(student[3]) > 0:
        fio = fio + ' ' + student[3]
    sl = GroupList.objects.filter(group__name='ИМИ-'+student[0], student__FIO=fio).first()
    if sl is not None:
        st = sl.student
        st.student_id = student[4]
        st.save()
        '''
        if len(sl) == 1:
            sl[0].student.student_id = student[4]
            sl[0].student.save()
        else:
            print(student)'''