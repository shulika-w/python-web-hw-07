from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import Base, Group, Teacher, Subject, Student, Grade
from faker import Faker
import random
import os
from my_select import select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, select_10, select_11, select_12

dbfile = 'university.db'
engine = create_engine(f'sqlite:///{dbfile}', echo=False)

def create_tables():
    Base.metadata.create_all(engine)


def create_fake_data():
    fake = Faker()
    Session = sessionmaker(bind=engine)
    session = Session()

    groups = [Group(name=f'Group {chr(65 + i)}') for i in range(3)]
    session.add_all(groups)

    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)

    subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'History']
    teachers_per_subject = random.sample(teachers, len(subjects))

    subjects_objs = [Subject(name=subject, teacher=teacher) for subject, teacher in zip(subjects, teachers_per_subject)]
    session.add_all(subjects_objs)

    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)]
    session.add_all(students)

    for student in students:
        for subject in subjects_objs:
            for _ in range(5):
                grade = random.randint(1, 12)
                date_received = fake.date_this_year()
                session.add(Grade(student=student, subject=subject, grade=grade, date_received=date_received))

    session.commit()
    session.close()


def main():

    if dbfile not in os.listdir():
        create_tables()
        create_fake_data()

    while True:
        script_number = input('Enter query number [1-12]: ')
        func_name = 'select_' + script_number
        print(f'Query: {func_name}')

        if script_number.lower() == 'exit':
            break

        
        Session = sessionmaker(bind=engine)
        session = Session()
        result = globals()[func_name](session)
        
        for row in result:
            print(row)

        session.close()


if __name__ == '__main__':
    main()