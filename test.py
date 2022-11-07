import os
from sqlmodel import SQLModel, Session, create_engine, select
import model


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_tables(engine):
    SQLModel.metadata.create_all(engine)


def select_track():
    with Session(engine) as session:
        statement = select(model.Track)
        results = session.exec(statement)
        track = results.first()
        os.system("clear")
        print(track)


if __name__ == "__main__":
    create_db_tables(engine)
    select_track()
