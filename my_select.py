from sqlalchemy.orm import Session
from sqlalchemy import func, text
from models import Base, Group, Teacher, Subject, Student, Grade


def select_1(session):
   
    desc = '-- Знайти 5 студентів із найбільшим середнім балом'
    print(desc)
    subquery = session.query(
        Student.name.label('student_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade, Student.id == Grade.student_id).group_by(Student.name).subquery()
 
    query = session.query(subquery.c.student_name, subquery.c.average_grade).order_by(subquery.c.average_grade.desc()).limit(5)

    result = query.all()
    return result


def select_2(session):
    
    desc = '-- Знайти студента із найвищим середнім балом з Biology'
    print(desc)
    subquery = session.query(
        Student.name.label('student_name'),
        func.avg(Grade.grade).label('avg_grade')
    ).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).filter(Subject.name == 'Biology').group_by(Student.id, Student.name).subquery()

    query = session.query(subquery.c.student_name, subquery.c.avg_grade).order_by(subquery.c.avg_grade.desc()).limit(1)

    result = query.all()
    return result


def select_3(session):
    
    desc = '-- Знайти середній бал у групах з Math'
    print(desc)
    subquery = session.query(
        Group.name.label('group_name'),
        Subject.name.label('subject_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Student, Group.id == Student.group_id).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).filter(Subject.name == 'Math').group_by(Group.id, Subject.id).subquery()

    query = session.query(subquery.c.group_name, subquery.c.subject_name, subquery.c.average_grade).order_by(subquery.c.group_name, subquery.c.subject_name)

    result = query.all()
    return result


def select_4(session):
    
    desc = '-- Найти середній бал на потоці (по всій таблиці оцінок)'
    print(desc)
    query = session.query(func.avg(Grade.grade).label('average_grade'))

    result = query.first()
    return result


def select_5(session):

    teacher = 'Brian Proctor'
    desc = f'-- Знайти які предмети читає певний викладач, {teacher}'
    print(desc)
    query = session.query(Subject.name.label('subject_name')).join(Teacher, Subject.teacher_id == Teacher.id).filter(Teacher.name == teacher)

    result = query.all()
    return result


def select_6(session):
    
    group = 'Group A'
    desc = f'-- Знайти список студентів у певній групі, {group}'
    print(desc)
    query = session.query(Student.name.label('student_name')).join(Group, Student.group_id == Group.id).filter(Group.name == group)

    result = query.all()
    return result


def select_7(session):
    
    group = 'Group A'
    subj = 'Math'
    desc = f'-- Знайти оцінки студентів у окремій групі з певного предмета. {group}, {subj}'
    print(desc)
    query = session.query(
        Student.name.label('student_name'),
        Grade.grade,
        Subject.name.label('subject_name'),
        Group.name.label('group_name')
    ).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).join(Group, Student.group_id == Group.id).filter(Group.name == group, Subject.name == subj)

    result = query.all()
    return result


def select_8(session):
    
    teacher = 'Brian Proctor'
    desc = f'-- Знайти середній бал, який ставить певний викладач, {teacher}'
    print(desc)
    subquery = session.query(
        Teacher.name.label('teacher_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject, Teacher.id == Subject.teacher_id).join(Grade, Subject.id == Grade.subject_id).filter(Teacher.name == teacher).group_by(Teacher.id, Teacher.name).subquery()

    query = session.query(subquery.c.teacher_name, subquery.c.average_grade).order_by(subquery.c.average_grade.desc())

    result = query.all()
    return result


def select_9(session):
    
    student = 'Ruth Pruitt'
    desc = f'-- Знайти список предметів, по якім певний студент має оцінки, {student}'
    print(desc)
    query = session.query(Subject.name.label('subject_name')).join(Grade, Subject.id == Grade.subject_id).join(Student, Grade.student_id == Student.id).filter(Student.name == student).distinct()

    result = query.all()
    return result


def select_10(session):
    
    student = 'Ruth Pruitt'
    teacher = 'Brian Proctor'
    desc = f'-- Список курсів, які певному студенту, {student} читає певний викладач, {teacher}'
    print(desc)
    query = session.query(Subject.name.label('subject_name')).join(Grade, Subject.id == Grade.subject_id).join(Student, Grade.student_id == Student.id).join(Teacher, Subject.teacher_id == Teacher.id).filter(Student.name == student, Teacher.name == teacher).distinct()

    result = query.all()
    return result


def select_11(session):
    
    student = 'Ruth Pruitt'
    teacher = 'Brian Proctor'
    desc = f'-- Середній бал, який певний викладач, {teacher} ставить певному студентові, {student}'
    print(desc)
    subquery = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject, Grade.subject_id == Subject.id).join(Teacher, Subject.teacher_id == Teacher.id).join(Student, Grade.student_id == Student.id).filter(Student.name == student, Teacher.name == teacher)

    query = session.query(subquery.scalar())

    result = query.first()
    return result


def select_12(session):

    group = 'Group A'
    subj = 'Math'
    desc = f'-- Остання Оцінка кожного студента у певній групі, {group}, з певного предмета, {subj}'
    print(desc)
    query = session.query(
        Student.name.label('student_name'),
        Subject.name.label('subject_name'),
        Grade.grade,
        func.max(Grade.date_received).label('last_grade_date')
    ).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).join(Group, Student.group_id == Group.id).filter(Group.name == group, Subject.name == subj).group_by(Student.id, Student.name, Subject.id).order_by(func.max(Grade.date_received).desc())

    result = query.all()
    return result