import configparser
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_confing = 'app/database.conf'
config = configparser.ConfigParser()
config.read(db_confing)


Base = declarative_base()
engine = create_engine(
    f"postgresql+psycopg2://"
    f"{config.get('postgresql', 'user')}:{config.get('postgresql', 'password')}@"
    f"{config.get('postgresql', 'host')}:{config.get('postgresql', 'port')}/"
    f"{config.get('postgresql', 'dbname')}"
)


class Deal(Base):
    """Модель сделок."""

    __tablename__ = 'grandmed_bitrix_deals'

    id = Column(Integer, primary_key=True)
    bitrix_id = Column(Integer, unique=True, comment='ID')

    title = Column(String, nullable=True, comment='TITLE')
    type_id = Column(String, nullable=True, comment='TYPE_ID')
    stage_id = Column(String, nullable=True, comment='STAGE_ID')
    currency_id = Column(String, nullable=True, comment='CURRENCY_ID')
    is_manual_opportunity = Column(String, nullable=True, comment='IS_MANUAL_OPPORTUNITY')
    opened = Column(String, nullable=True, comment='OPENED')
    closed = Column(String, nullable=True, comment='CLOSED')
    comments = Column(String, nullable=True, comment='COMMENTS')
    additional_info = Column(String, nullable=True, comment='ADDITIONAL_INFO')
    stage_semantic_id = Column(String, nullable=True, comment='STAGE_SEMANTIC_ID')
    is_new = Column(String, nullable=True, comment='IS_NEW')
    is_recurring = Column(String, nullable=True, comment='IS_RECURRING')
    is_return_customer = Column(String, nullable=True, comment='IS_RETURN_CUSTOMER')
    is_repeated_approach = Column(String, nullable=True, comment='IS_REPEATED_APPROACH')
    source_id = Column(String, nullable=True, comment='SOURCE_ID')
    source_description = Column(String, nullable=True, comment='SOURCE_DESCRIPTION')
    originator_id = Column(String, nullable=True, comment='ORIGINATOR_ID')
    utm_source = Column(String, nullable=True, comment='UTM_SOURCE')
    utm_medium = Column(String, nullable=True, comment='UTM_MEDIUM')
    utm_campaign = Column(String, nullable=True, comment='UTM_CAMPAIGN')
    utm_content = Column(String, nullable=True, comment='UTM_CONTENT')
    utm_term = Column(String, nullable=True, comment='UTM_TERM')

    probability = Column(Integer, nullable=True, comment='PROBABILITY')
    lead_id = Column(Integer, nullable=True, comment='LEAD_ID')
    company_id = Column(Integer, nullable=True, comment='COMPANY_ID')
    contact_id = Column(Integer, nullable=True, comment='CONTACT_ID')
    quote_id = Column(Integer, nullable=True, comment='QUOTE_ID')
    assigned_by_id = Column(Integer, nullable=True, comment='ASSIGNED_BY_ID')
    created_by_id = Column(Integer, nullable=True, comment='CREATED_BY_ID')
    modify_by_id = Column(Integer, nullable=True, comment='MODIFY_BY_ID')
    location_id = Column(Integer, nullable=True, comment='LOCATION_ID')
    category_id = Column(Integer, nullable=True, comment='CATEGORY_ID')
    parent_id_145 = Column(Integer, nullable=True, comment='PARENT_ID_145')
    parent_id_146 = Column(Integer, nullable=True, comment='PARENT_ID_146')
    parent_id_154 = Column(Integer, nullable=True, comment='PARENT_ID_154')
    parent_id_176 = Column(Integer, nullable=True, comment='PARENT_ID_176')
    parent_id_182 = Column(Integer, nullable=True, comment='PARENT_ID_182')
    parent_id_1056 = Column(Integer, nullable=True, comment='PARENT_ID_1056')
    last_activity_by = Column(Integer, nullable=True, comment='LAST_ACTIVITY_BY')
    origin_id = Column(Integer, nullable=True, comment='ORIGIN_ID')
    moved_by_id = Column(Integer, nullable=True, comment='MOVED_BY_ID')

    opportunity = Column(Float, nullable=True, comment='OPPORTUNITY')
    tax_value = Column(Float, nullable=True, comment='TAX_VALUE')

    begin_date = Column(DateTime(timezone=True), nullable=True, comment='BEGINDATE')
    close_date = Column(DateTime(timezone=True), nullable=True, comment='CLOSEDATE')
    date_create = Column(DateTime(timezone=True), nullable=True, comment='DATE_CREATE')
    date_modify = Column(DateTime(timezone=True), nullable=True, comment='DATE_MODIFY')
    moved_time = Column(DateTime(timezone=True), nullable=True, comment='MOVED_TIME')
    last_activity_time = Column(DateTime(timezone=True), nullable=True, comment='LAST_ACTIVITY_TIME')


class Contract(Base):
    """Модель контрактов."""

    __tablename__ = 'grandmed_bitrix_contracts'

    id = Column(Integer, primary_key=True)
    bitrix_id = Column(Integer, unique=True, comment='ID')
    
    post = Column(String, nullable=True, comment='POST')
    comments = Column(String, nullable=True, comment='COMMENTS')
    honorific = Column(String, nullable=True, comment='HONORIFIC')
    name = Column(String, nullable=True, comment='NAME')
    second_name = Column(String, nullable=True, comment='SECOND_NAME')
    last_name = Column(String, nullable=True, comment='LAST_NAME')
    photo = Column(String, nullable=True, comment='PHOTO')
    lead_id = Column(Integer, nullable=True, comment='LEAD_ID')
    type_id = Column(String, nullable=True, comment='TYPE_ID')
    source_id = Column(String, nullable=True, comment='SOURCE_ID')
    source_description = Column(String, nullable=True, comment='SOURCE_DESCRIPTION')
    company_id = Column(Integer, nullable=True, comment='COMPANY_ID')
    birthdate = Column(String, nullable=True, comment='BIRTHDATE')
    export = Column(String, nullable=True, comment='EXPORT')
    has_phone = Column(String, nullable=True, comment='HAS_PHONE')
    has_email = Column(String, nullable=True, comment='HAS_EMAIL')
    has_imol = Column(String, nullable=True, comment='HAS_IMOL')
    
    date_create = Column(DateTime(timezone=True), nullable=True, comment='DATE_CREATE')
    date_modify = Column(DateTime(timezone=True), nullable=True, comment='DATE_MODIFY')
    last_activity_time = Column(DateTime(timezone=True), nullable=True, comment='LAST_ACTIVITY_TIME')
    
    assigned_by_id = Column(Integer, nullable=True, comment='ASSIGNED_BY_ID')
    created_by_id = Column(Integer, nullable=True, comment='CREATED_BY_ID')
    modify_by_id = Column(Integer, nullable=True, comment='MODIFY_BY_ID')
    last_activity_by = Column(Integer, nullable=True, comment='LAST_ACTIVITY_BY')
    
    opened = Column(String, nullable=True, comment='OPENED')
    originator_id = Column(String, nullable=True, comment='ORIGINATOR_ID')
    origin_id = Column(Integer, nullable=True, comment='ORIGIN_ID')
    origin_version = Column(String, nullable=True, comment='ORIGIN_VERSION')
    face_id = Column(String, nullable=True, comment='FACE_ID')
    
    address = Column(String, nullable=True, comment='ADDRESS')
    address_2 = Column(String, nullable=True, comment='ADDRESS_2')
    address_city = Column(String, nullable=True, comment='ADDRESS_CITY')
    address_postal_code = Column(String, nullable=True, comment='ADDRESS_POSTAL_CODE')
    address_region = Column(String, nullable=True, comment='ADDRESS_REGION')
    address_province = Column(String, nullable=True, comment='ADDRESS_PROVINCE')
    address_country = Column(String, nullable=True, comment='ADDRESS_COUNTRY')
    address_loc_addr_id = Column(String, nullable=True, comment='ADDRESS_LOC_ADDR_ID')
    
    utm_source = Column(String, nullable=True, comment='UTM_SOURCE')
    utm_medium = Column(String, nullable=True, comment='UTM_MEDIUM')
    utm_campaign = Column(String, nullable=True, comment='UTM_CAMPAIGN')
    utm_content = Column(String, nullable=True, comment='UTM_CONTENT')
    utm_term = Column(String, nullable=True, comment='UTM_TERM')
    
    parent_id_145 = Column(Integer, nullable=True, comment='PARENT_ID_145')
    parent_id_172 = Column(Integer, nullable=True, comment='PARENT_ID_172')
    parent_id_185 = Column(Integer, nullable=True, comment='PARENT_ID_185')
    parent_id_1060 = Column(Integer, nullable=True, comment='PARENT_ID_1060')


class Specialist(Base):
    """Модель специалистов."""

    __tablename__ = 'grandmed_qms_specialists'

    id = Column(Integer, primary_key=True)
    material_number = Column(String, unique=True, comment='Номер материала')
    patient_type = Column(String, comment='Вид пациента')
    oocyte_assessment = Column(String, comment='Оценка ооцита')
    fertilization_method = Column(String, comment='Метод оплодотворения')
    sperm_processing = Column(String, comment='Обработка спермы')
    fertilization_assessment = Column(String, comment='Оценка оплодотворения')
    development_medium = Column(String, comment='Среда для развития')
    incubator = Column(String, comment='Инкубатор')
    date_d0 = Column(Date, comment='Дата D0')
    embryologist = Column(String, comment='Эмбриолог')
    attending_physician = Column(String, comment='Лечащий врач')
    episode_number = Column(String, comment='Номер эпизода')
    registration_number = Column(String, comment='Рег.№')
    patient_age = Column(Integer, comment='Возраст пациента')
    development_medium_alt = Column(String, comment='Среда для развития.1')


class Analytic(Base):
    """Модель аналитик."""

    __tablename__ = 'grandmed_qms_analytics'

    id = Column(Integer, primary_key=True)
    registration_number = Column(String, nullable=True, comment='Рег.№')
    full_name = Column(String, nullable=True, comment='ФИО')
    gender = Column(String, nullable=True, comment='Пол')
    age = Column(Integer, nullable=True, comment='Возр.')
    okmu_code = Column(String, nullable=True, comment='Код ОКМУ')
    service = Column(String, nullable=True, comment='Услуга')
    first_name = Column(String, nullable=True, comment='Имя')
    last_name = Column(String, nullable=True, comment='Фамилия')
    phone = Column(String, nullable=True, comment='Телефон')
    admission_type = Column(String, nullable=True, comment='Вид поступления')
    admission_purpose = Column(String, nullable=True, comment='Цель поступления')
    episode_number = Column(String, nullable=True, comment='№_эпизода')
    appointment_type = Column(String, nullable=True, comment='Тип назначения')
    episode_end_date = Column(Date, nullable=True, comment='Дата завершения эпизода')
    appointment_date = Column(String, nullable=True, comment='Дата выполнения назначения')
    appointment_time = Column(String, nullable=True, comment='Время назначения')
    underperformance = Column(String, nullable=True, comment='Недовыполнение')
    status = Column(String, nullable=True, comment='Состояние')
    cd = Column(String, nullable=True, comment='КД')
    bed_days = Column(String, nullable=True, comment='Количество койко-дней (по услуге пребывания в стационаре) за поисковый период')
    department_execution = Column(String, nullable=True, comment='Отделение.Выполнение')
    position_execution = Column(String, nullable=True, comment='Должность.Выполнение')
    specialist_execution = Column(String, nullable=True, comment='Специалист/Ресурс.Выполнение')
    specialist_specialization = Column(String, nullable=True, comment='Специализация исполнителя')
    hospitalization_department = Column(String, nullable=True, comment='Отделение госпитализации')
    tariff = Column(String, nullable=True, comment='Тариф')
    price = Column(String, nullable=True, comment='Цена')
    discount_percent = Column(String, nullable=True, comment='%Ск-ки')
    total_amount = Column(String, nullable=True, comment='Сумма')
    debt = Column(String, nullable=True, comment='Долг')
    date = Column(Date, nullable=True, comment='Дата')
    specialist_full_name = Column(String, nullable=True, comment='ФИО специалист')
    attending_physician = Column(String, nullable=True, comment='Лечащий врач')
    complex_code = Column(String, nullable=True, comment='Код комплекса')
    price_section = Column(String, nullable=True, comment='Раздел прайса, когда услуга была назначена')
    service_code = Column(String, nullable=True, comment='Код услуги по прайсу, когда услуга была назначена')
    category = Column(String, nullable=True, comment='Категория')
    execution_time = Column(String, nullable=True, comment='Время выполнения')
    set_indicator = Column(String, nullable=True, comment='Признак набора')
    physician_department_code = Column(String, nullable=True, comment='Код отделения лечащего врача')
    physician_department = Column(String, nullable=True, comment='Лечащий врач: код отделения')
    registration_number_alt = Column(String, nullable=True, comment='Рег.№.1')
    email = Column(String, nullable=True, comment='Электронная почта')
    middle_name = Column(String, nullable=True, comment='Отчество')
    birth_date = Column(Date, nullable=True, comment='ДР')


def init_tables():
    Base.metadata.create_all(engine)


def get_session():
    """Создаем сессию для работы с базой данных."""
    return sessionmaker(bind=engine)()
