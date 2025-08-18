from sqlalchemy import create_engine, MetaData, Table, update
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import get_session, engine

session = get_session()
metadata = MetaData()
model_table = Table('grandmed_qms_analytics', metadata, autoload_with=engine)


def convert_date_format(date_str):
    try:
        # Парсим исходную дату
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # Преобразуем в новый формат
        return dt.strftime("%d-%m-%Y")
    except ValueError:
        # Если формат не совпадает, возвращаем исходное значение
        return date_str


records = session.query(model_table).all()

# Обновляем каждую запись
for n, record in enumerate(records, 1):
    old_date = record.episode_end_date
    new_date = convert_date_format(old_date)

    print(f"\rОбработка... {n}/{len(records)}", end="", flush=True)

    if new_date != old_date:
        # Обновляем запись в базе данных
        stmt = update(model_table) \
            .where(model_table.c.id == record.id) \
            .values(episode_end_date=new_date)
        session.execute(stmt)

print()
session.commit()
session.close()
