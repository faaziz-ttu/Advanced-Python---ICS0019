from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

#  Create SQLite database DINERS
Base = declarative_base()
engine = create_engine('sqlite:///diners_2.db', echo=True)
Session = sessionmaker(bind=engine)



# Create PROVIDER and CANTEEN tables
class Provider(Base):
    __tablename__ = 'PROVIDER'
    id = Column(Integer, primary_key=True)
    provider_name = Column(String)

    canteens = relationship('Canteen', back_populates='provider')


class Canteen(Base):
    __tablename__ = 'CANTEEN'
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('PROVIDER.id'))
    name = Column(String)
    location = Column(String)
    time_open = Column(String)
    time_closed = Column(String)

    provider = relationship('Provider', back_populates='canteens')

Base.metadata.create_all(engine)

# 2) Insert IT College canteen data by separate statement, other canteens as one list
session = Session()

provider_name = "Bitt OÜ"
# check if "Bitt OÜ" already exists in PROVIDER table
provider = session.query(Provider).filter_by(provider_name=provider_name).first()
if not provider:
    provider = Provider(provider_name=provider_name)
    session.add(provider)
    session.commit()

canteen_name = "bitStop KOHVIK"
# check if "bitStop KOHVIK" already exists in CANTEEN table
new_canteen = session.query(Canteen).filter_by(name=canteen_name).first()
if not new_canteen:
    new_canteen = Canteen(provider=provider, name= canteen_name, location="IT College, Raja 4c",
                          time_open="9:30", time_closed="16:00")
    session.add(new_canteen)
    session.commit()

canteen_data = [
    ("Rahva Toit", "Economics- and social science building canteen", "Akadeemia tee 3", "8:30", "18:30"),
    ("Rahva Toit", "Library canteen", "Akadeemia tee 1/Ehitajate tee 7", "8:30", "19:00"),
    ("Baltic Restaurants Estonia AS", "Main building Deli cafe", "Ehitajate tee 5, U01 building", "9:00", "16:30"),
    ("Baltic Restaurants Estonia AS", "Main building Daily lunch restaurant", "Ehitajate tee 5, U01 building", "9:00",
     "16:30"),
    ("Rahva Toit", "U06 building canteen", "", "9:00", "16:00"),
    ("Baltic Restaurants Estonia AS", "Natural Science building canteen", "Akadeemia tee 15, SCI building", "9:00",
     "16:00"),
    ("Baltic Restaurants Estonia AS", "ICT building canteen", "Raja 15/Mäepealse 1", "9:00", "16:00"),
    ("TTÜ Sport OÜ", "Sports building canteen", "Männiliiva 7, S01 building", "11:00", "20:00")
]

#inserting data into canteen and provider table
for provider_name, canteen_name, location, time_open, time_closed in canteen_data:
    # check if Provider_name already exists in PROVIDER table for not adding duplicate data to database
    provider = session.query(Provider).filter_by(provider_name=provider_name).first()
    if not provider:
        provider = Provider(provider_name=provider_name)
        session.add(provider)
        session.commit()
    # check if canteen_name already exists in CANTEEN table for not adding duplicate data to database
    canteen = session.query(Canteen).filter_by(name=canteen_name).first()
    if not canteen:
        canteen = Canteen(name=canteen_name, location=location, time_open=time_open, time_closed=time_closed)
        canteen.provider = provider
        session.add(canteen)
        session.commit()

# 3) Query canteens that are open from 09.00 to 16.20

results = session.query(Canteen).filter(Canteen.time_open <= '09:00', Canteen.time_closed >= '16:20').all()
print(end="\n\n")
for row in results:
    print(row.id, row.name, row.location, row.time_open, row.time_closed, row.provider.provider_name)



# 4) Create query for canteens which are serviced by Baltic Restaurants Estonia AS.
results = session.query(Canteen).join(Provider).filter(Provider.provider_name == "Baltic Restaurants Estonia AS").all()
print(end="\n\n")
for row in results:
    print(row.id, row.name, row.location, row.time_open, row.time_closed, row.provider.provider_name)
