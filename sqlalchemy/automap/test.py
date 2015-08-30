from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer
from sqlalchemy.schema import Sequence

Base = automap_base()


class Test(Base):
    __tablename__ = 'test'

    id_no = Column('id', Integer, Sequence('id_seq'), primary_key=True)


engine = create_engine('sqlite:///test.sqlite', echo=True)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
# Test = Base.classes.test

session = Session(engine)

try:

    ins = Test(m_no="1", a_no="2", c_no="3")
    inslst = []
    ins1 = Test(m_no="1", a_no="2", c_no="3")
    ins2 = Test(m_no="1", a_no="2", c_no="3")
    ins3 = Test(m_no="1", a_no="2", c_no="3")
    inslst.append(ins1)
    inslst.append(ins2)
    inslst.append(ins3)

    session.add(ins)
    session.commit()
    session.add_all(inslst)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
