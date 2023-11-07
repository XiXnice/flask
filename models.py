from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime

POSTGRES_DSN = f'postgresql://app:secret@127.0.0.1:5431/app'

engine = create_engine(POSTGRES_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisements(Base):
    __tablename__ = 'add_advertisements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(255), index=True, nullable=False)


Base.metadata.create_all(bind=engine)
