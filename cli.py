import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Teacher, Grade, Subject, Group

def create_record(session, model, **kwargs):
    new_record = model(**kwargs)
    session.add(new_record)
    session.commit()
    print(f"{model.__name__} '{kwargs.get('name', '')}' added successfully.")


def remove_record(session, model, identifier):
    record = session.query(model).get(identifier)
    if record:
        session.delete(record)
        session.commit()
        print(f"{model.__name__} with id {identifier} removed successfully.")
    else:
        print(f"{model.__name__} with id {identifier} not found.")


def update_record(session, model, identifier, **kwargs):
    record = session.get(model, identifier)
    if record:
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        print(f"{model.__name__} with id {identifier} updated successfully.")
    else:
        print(f"{model.__name__} with id {identifier} not found.")


def list_records(session, model):
    records = session.query(model).all()
    print(f"List of {model.__name__}s:")
    for record in records:
        print(f"ID: {record.id}, Name: {record.name}")


def main():
    dbfile = 'university.db'
    engine = create_engine(f'sqlite:///{dbfile}', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    parser = argparse.ArgumentParser(description="CLI for CRUD operations on the database")
    parser.add_argument("--action", "-a", choices=["create", "list", "update", "remove"], required=True, help="CRUD action")
    parser.add_argument("--model", "-m", choices=["Student", "Teacher", "Grade", "Subject", "Group"], required=True, help="Model on which operation will be performed")
    parser.add_argument("--id", type=int, help="ID to be removed, updated, or listed")
    parser.add_argument("--name", "-n", help="Name to be added, removed, or updated")

    args = parser.parse_args()

    if args.action == "create":
        model_class = globals().get(args.model)
        if model_class and args.name:
            create_record(session, model_class, name=args.name)
        else:
            print("Invalid combination of action and model.")

    elif args.action == "remove":
        model_class = globals().get(args.model)
        if model_class:
            if args.id:
                remove_record(session, model_class, identifier=args.id)
            elif args.name:
                remove_record(session, model_class, identifier=args.name)
            else:
                print("Please provide either --id or --name for removal.")
        else:
            print("Invalid combination of action and model.")

    elif args.action == "list":
        model_class = globals().get(args.model)
        if model_class:
            list_records(session, model_class)
        else:
            print("Invalid combination of action and model.")
            
    elif args.action == "update":
        model_class = globals().get(args.model)
        if model_class and args.id and args.name:
            update_record(session, model_class, identifier=args.id, name=args.name)
        else:
            print("Invalid combination of action, model, --id, and --name for updating.")

if __name__ == "__main__":
    main()