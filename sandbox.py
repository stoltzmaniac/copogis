import json

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from geoalchemy2 import Geometry, WKTElement

#TODO: make json table for "lookup" (rather than 'name' column) to hold all of the ['properites'] data (metadata)
# Future user input
table_name = 'my_geom'

# Database stuff
engine = create_engine('postgresql://gis:gis@localhost:5433/gis', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Opening file
with open('sample_data/Highway Mileposts in Colorado.geojson') as f:
    data = json.load(f)


geom_type = data['features'][0]['geometry']['type'].upper()
class MyGeom(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    geom = Column(Geometry(geom_type))

try:
    MyGeom.__table__.create(engine)
except ProgrammingError:
    print('Table already Created')


data_i = []
for i in data['features']:
    coords = str(tuple(i['geometry']['coordinates'])).replace(',','')
    print(f'{geom_type}{coords}')
    d = MyGeom(name='blahblah', geom=WKTElement(f'{geom_type}{coords}'))
    data_i.append(d)
try:
    session.add_all(data_i)
    session.commit()
except Exception as e:
    print(str(e))
    session.rollback()

