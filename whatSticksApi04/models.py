from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, \
    Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import json
from datetime import datetime

with open(r'C:\Users\captian2020\Documents\config_files\config_whatSticks01.json') as config_file:
    config = json.load(config_file)


Base = declarative_base()
engine = create_engine(config.get('SQL_URI'), echo = True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
sess = Session()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(Text, unique = True, nullable = False)
    password = Column(Text, nullable = False)
    lat = Column(Float)
    lon = Column(Float)
    location_id = Column(Integer, ForeignKey('locations.id'))#one
    oura_token_id = Column(Integer, ForeignKey('oura_token.id'))#one
    oura_sleep = relationship('Oura_sleep_descriptions', backref='Oura_sleep', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email}, location_id: {self.location_id})'

class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key = True)
    city = Column(Text)
    region = Column(Text)
    country = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    users = relationship('Users', backref = 'location', lazy = True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Locations(id: {self.id}, city: {self.city}, lat: {self.lat}, ' \
            f'lon: {self.lon})'

class Oura_token(Base):
    __tablename__ = 'oura_token'
    id = Column(Integer, primary_key = True)
    token = Column(Text)
    users = relationship('Users', backref = 'oura_token', lazy = True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Oura_token(id: {self.id}, token: {self.token})'

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key = True)
    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    city_location_name = Column(Text)
    region_name = Column(Text)
    country_name = Column(Text)
    tz_id = Column(Text)
    localtime_epoch = Column(Integer)
    localtime = Column(Text)

# Air Quality Endpoint
    co = Column(Float)# Carbon Monoxide (μg/m3)
    o3 = Column(Float)# Ozone (μg/m3)
    no2 = Column(Float)# Nitrogen dioxide (μg/m3)
    so2 = Column(Float)# Sulphur dioxide (μg/m3)
    pm2_5 = Column(Float)# PM2.5 (μg/m3)
    pm10 = Column(Float)# PM10 (μg/m3)
    us_epa_index = Column(Integer)#  	US - EPA standard. 
    gb_defra_index = Column(Integer)# UK Defra Index

# Realtime API i.e. this is the weather
    last_updated = Column(Text)
    last_updated_epoch = Column(Text)
    temp_c = Column(Float)
    temp_f = Column(Float)
    feelslike_c = Column(Float)
    feelslike_f = Column(Float)
    condition_text = Column(Text)
    condition_icon = Column(Text)
    condition_code = Column(Integer)
    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_dir = Column(String)
    pressure_mb = Column(Float)
    pressure_in = Column(Float)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    humidity = Column(Integer)
    cloud = Column(Integer)
    is_day = Column(Integer)
    uv = Column(Float)
    gust_mph = Column(Float)
    gust_kph = Column(Float)

# Astronomy API
    sunrise = Column(Text)
    sunset = Column(Text)
    moonrise = Column(Text)
    moonset = Column(Text)
    moon_phase = Column(Text)
    moon_illumination = Column(Integer)

    note = Column(Text)
    
    def __repr__(self):
        return f"Weather(id: {self.id}, " \
            f"city_location_name: {self.city_location_name}, temp_c: {self.temp_c})"


class Oura_sleep_descriptions(Base):
    __tablename__ = 'oura_sleep_descriptions'
    id = Column(Integer, primary_key = True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
    summary_date = Column(Text)
    period_id = Column(Integer)
    is_longest = Column(Integer)
    timezone = Column(Integer)
    bedtime_end = Column(Text)
    bedtime_start = Column(Text)
    breath_average = Column(Float)
    duration = Column(Integer)
    total = Column(Integer)
    awake = Column(Integer)
    rem = Column(Integer)
    deep = Column(Integer)
    light = Column(Integer)
    midpoint_time = Column(Integer)
    efficiency = Column(Integer)
    restless = Column(Integer)
    onset_latency = Column(Integer)
    rmssd = Column(Integer)
    score = Column(Integer)
    score_alignment = Column(Integer)
    score_deep = Column(Integer)
    score_disturbances = Column(Integer)
    score_efficiency = Column(Integer)
    score_latency = Column(Integer)
    score_rem = Column(Integer)
    score_total = Column(Integer)
    temperature_deviation = Column(Float)
    bedtime_start_delta = Column(Integer)
    bedtime_end_delta = Column(Integer)
    midpoint_at_delta = Column(Integer)
    temperature_delta = Column(Float)
    hr_lowest = Column(Integer)
    hr_average = Column(Float)
    # temperature_trend_deviation=Column(Float)

    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Oura_sleep_descriptions(id: {self.id}, user_id: {self.user_id}," \
            f"summary_date:{self.summary_date}," \
            f"score: {self.score}, score_total: {self.score_total}," \
            f"hr_lowest: {self.hr_lowest}, hr_average: {self.hr_average}," \
            f"bedtime_start: {self.bedtime_start}, bedtime_end: {self.bedtime_end}," \
            f"duration: {self.duration}, onset_latency: {self.onset_latency})"


#Build db
if 'users' in inspect(engine).get_table_names():
    print('db already exists')
else:
    Base.metadata.create_all(engine)
    print('NEW db created.')