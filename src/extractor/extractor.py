"""Extract data."""
import inspect

from sqlmodel import Session, SQLModel, create_engine, select


class Extractor:
    def __init__(self, model, db_uri: str) -> None:
        self.load_model(model)
        self.engine = create_engine(db_uri, echo=False)
        SQLModel.metadata.create_all(self.engine)

    def load_model(self, model) -> None:
        for k, v in inspect.getmembers(model, inspect.isclass):
            if not v.__module__ is model.__name__:
                continue
            setattr(self, k, v)

    def select_table(self, table: str) -> list:
        selected_table = getattr(self, table, None)
        if selected_table is None:
            return list()
        with Session(self.engine) as session:
            return session.exec(select(selected_table)).all()
