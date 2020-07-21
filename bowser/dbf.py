import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from shelper import pgconnstring


Base = declarative_base()
class TextList(Base):
    __tablename__ = 'tbl_txtlist'
    t_id = Column(Integer,primary_key=True)
    t_text = Column(String)
    t_type = Column(String)
    t_remarks = Column(String)



def return_session_textlist():
    connstring_remote = pgconnstring()
    remote_engine = create_engine(connstring_remote)
    remote_session = sessionmaker(bind=remote_engine)
    table_objects = [Base.metadata.tables['tbl_txtlist']]
    Base.metadata.create_all(remote_engine,tables=table_objects)
    remotesession = remote_session()
    return remote_engine,remotesession


def return_txt_comp(sessionobj=None,filter=None):
    """this function returns all the text from the db"""
    all_data = None
    sessionengine = None
    if sessionobj is None:
        sessionengine,sessionobj = return_session_textlist()
    
    if filter is None:
        all_data = sessionobj.query(TextList).with_for_update(nowait=True) #pylint: disable=maybe-no-member
    else:
        all_data = sessionobj.query(TextList).with_for_update(nowait=True).filter(TextList.t_type==filter) #pylint: disable=maybe-no-member

    if sessionengine is not None:
        sessionengine.dispose()
    sessionobj.close()
    return all_data
    


if __name__ == "__main__":
    data = return_txt_comp()
    input(type(data))
    for row in data:
        print(row.t_id)

