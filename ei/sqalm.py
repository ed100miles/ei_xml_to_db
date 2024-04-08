from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


db_file = "ei.db"
engine = create_engine(f"sqlite:///{db_file}", echo=True)


class Base(DeclarativeBase):
    pass


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[str] = mapped_column(
        primary_key=True
    )  # I'll make this same as filename for now
    filename: Mapped[str]
    activity_name: Mapped[str]
    included_activities_start: Mapped[str]
    included_activities_end: Mapped[str]
    general_comments: Mapped[str]
    classification_system: Mapped[str]
    classification_value: Mapped[str]
    geography_shortname: Mapped[str]
    # geography_comments: Mapped[str]
    time_period_start_data: Mapped[str]
    time_period_end_data: Mapped[str]
    time_period_is_data_valid_for_entire_period: Mapped[str]
    # time_period_comments: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.activity_name!r})"


class IntermediateExchange(Base):
    __tablename__ = "intermediate_exchange"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # I'll do activity filename + plus intermediate exchange id
    activity = mapped_column(ForeignKey("activity.id"))
    exchange_name: Mapped[str]
    amount: Mapped[float]
    unit_name: Mapped[str]
    comment: Mapped[str]

    def __repr__(self) -> str:
        return f"IntermediateExchange(id={self.id!r}, exchange_name={self.exchange_name!r})"

class ElementaryExchange(Base):
    __tablename__ = "elementary_exchange"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # I'll do activity filename + plus intermediate exchange id
    activity = mapped_column(ForeignKey("activity.id"))
    exchange_name: Mapped[str]
    amount: Mapped[float]
    unit_name: Mapped[str]
    comment: Mapped[str]

    def __repr__(self) -> str:
        return f"ElementaryExchange(id={self.id!r}, exchange_name={self.exchange_name!r})"

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
