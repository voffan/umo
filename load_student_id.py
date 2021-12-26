from umo_project.wsgi import application
from umo.models import GroupList


def load_students(csv_file):
    students = open(csv_file).read().split('\n')
    students = [student.split(';') for student in students]

    for student in students:
        if len(student) > 0:
            fio = student[1]
            if len(student[2]) > 0:
                sl = GroupList.objects.filter(group__Name=student[0], student__FIO=fio).first()
                if sl is not None:
                    st = sl.student
                    st.student_id = student[2]
                    st.save()
                else:
                    print(student[0], student[1], 'student not found!')
            else:
                print(student[0], student[1], 'has no id!')
            '''
            if len(sl) == 1:
                sl[0].student.student_id = student[4]
                sl[0].student.save()
            else:
                print(student)'''


if __name__ == '__main__':
    load_students('bak21.csv')
    load_students('mag21.csv')