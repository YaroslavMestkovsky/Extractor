from app.models import get_session, Specialist
from app.source_to_db_relations import SPECIALISTS
from sqlalchemy import select
import re
import pandas as pd


class PostgresManager:
    """Менеджер для загрузки данных в постгрес."""

    def __init__(self, logger):
        self.logger = logger
        self.session = get_session()

    def upload(self, df, is_analytics):
        """Загрузка в постгрю."""

        if is_analytics:
            self._upload_analytics(df)
        else:
            self._upload_specialists(df)

    def _upload_analytics(self, df):
        """Загрузка аналитик."""

    def _upload_specialists(self, df):
        """Загрузка специалистов."""
        columns_to_keep = [col for col in df.columns if col in SPECIALISTS]
        df = df[columns_to_keep]
        df = df.rename(columns=SPECIALISTS)
        
        # Обработка поля patient_age - извлекаем только цифры
        if 'patient_age' in df.columns:
            df['patient_age'] = df['patient_age'].apply(
                lambda x: int(re.search(r'\d+', str(x)).group())
                if pd.notna(x) and re.search(r'\d+', str(x))
                else None
            )
        
        # Получаем список существующих записей
        existing_numbers = set(
            number[0] for number in 
            self.session.execute(select(Specialist.material_number)).all()
        )

        # Фильтруем только новые записи
        new_records = df[~df['material_number'].isin(existing_numbers)]
        
        if new_records.empty:
            self.logger.info("Нет новых записей для загрузки")
        else:
            # Конвертируем записи в список словарей
            records_to_insert = new_records.to_dict('records')

            # Создаем объекты Specialist и добавляем их в сессию
            specialists = [Specialist(**record) for record in records_to_insert]
            self.session.add_all(specialists)

            try:
                self.session.commit()
                self.logger.info(f"Успешно загружено {len(specialists)} новых записей специалистов.")
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Ошибка при загрузке данных: {str(e)}")
                raise
