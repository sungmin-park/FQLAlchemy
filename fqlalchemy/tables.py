from sqlalchemy import Column, Text, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fqlalchemy.types import ID

engine = create_engine('fql:///')
session_maker = sessionmaker(bind=engine)
Session = scoped_session(session_maker)
Base = declarative_base()
Base.query = Session.query_property()


class FBPage(Base):
    __tablename__ = 'page'
    page_id = Column(ID, primary_key=True)
    name = Column(Text)
    username = Column(Text)
