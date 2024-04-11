import argparse
from confa.models import Grade, Teacher, Student, Group, Subject
from confa.db import session
from faker import Faker


def seed_database():
    fake = Faker()

    groups = [Group(name=fake.word()) for _ in range(3)]
    session.add_all(groups)

    teachers = [Teacher(fullname=fake.name()) for _ in range(3)]
    session.add_all(teachers)

    subjects = [Subject(name=fake.word()) for _ in range(5)]
    session.add_all(subjects)

    students = [Student(fullname=fake.name(), group_id=fake.random_element(groups).id) for _ in range(30)]
    session.add_all(students)

    for student in students:
        for subject in subjects:
            session.add(Grade(value=fake.random_int(min=1, max=100),
                              student_id=student.id,
                              subject_id=subject.id,
                              teacher_id=fake.random_element(teachers).id))

    session.commit()
    print("Database seeded successfully.")


def main():
    parser = argparse.ArgumentParser(description="CRUD operations with the database.")
    parser.add_argument(
        "--action",
        "-a",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action: create, list, update, or remove.",
    )
    parser.add_argument(
        "--model",
        "-m",
        choices=["Teacher", "Group", "Grade", "Student", "Subject"],
        required=True,
        help="Model to perform CRUD operations on: Grade, Teacher, Student, Group, Subject.",
    )
    parser.add_argument(
        "--id", type=int, help="ID of the record for update or removal."
    )
    parser.add_argument("--name", "-n", type=str, help="Name for creation or update.")
    parser.add_argument("--seed", action="store_true", help="Seed the database.")

    args = parser.parse_args()

    model_classes = {
        "Grade": Grade,
        "Teacher": Teacher,
        "Subject": Subject,
        "Student": Student,
        "Group": Group,
    }

    model = model_classes.get(args.model)
    if model is None:
        print("Invalid model.")
        return

    if args.seed:
        seed_database()
        return

    if args.action == "create":
        create(args, model)
    elif args.action == "list":
        list(args, model)
    elif args.action == "update":
        update(args, model)
    elif args.action == "remove":
        remove(args, model)
    else:
        print("Invalid action or model.")


def create(args, model):
    if model == Teacher or Student:
        model = model(fullname=args.name)
    else:
        model = model(name=args.name)
    session.add(model)
    session.commit()
    print(f"in model '{model}' '{args.name}' created successfully.")


def list(args, model):
    models = session.query(model).all()
    for model in models:
        print(f"ID: {model.id}, Name: {args.name}")


def update(args, model):
    model = session.query(model).filter_by(id=args.id).first()
    if model == Teacher or Student:
        name = model.fullname
    else:
        name = model.name
    if model:
        name = args.name
        session.commit()
        print(f"{model} with ID {args.id} updated successfully.")
    else:
        print(f"{model} with ID {args.id} not found.")


def remove(args, model):
    model = session.query(model).filter_by(id=args.id).first()
    if model:
        session.delete(model)
        session.commit()
        print(f"{model} with ID {args.id} removed successfully.")
    else:
        print(f"{model} with ID {args.id} not found.")


if __name__ == "__main__":
    main()