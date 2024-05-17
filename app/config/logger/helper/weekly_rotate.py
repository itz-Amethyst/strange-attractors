import logging
from datetime import date

from app.config.settings.helper import PROJECT_DIR

class WeeklyRotating(logging.FileHandler):
    def __init__(self):
        self.path = PROJECT_DIR / 'logs'
        self.path.mkdir(parents=True, exist_ok=True)

        self.week = self.get_week()
        filename = str(self.path / f'{self.week}.log')

        super().__init__(filename, 'a', 'utf-8')

    def get_week(self):
        today = date.today()
        return (today.month * 4) + (today.day // 7)

    def emit(self, record):
        try:
            week = self.get_week()

            if week != self.week:
                if self.stream:
                    self.stream.close()
                    self.stream = None

                self.path.mkdir(parents=True, exist_ok=True)
                self.baseFilename = str(self.path / f'{week}.log')

                self.week = week
                if not self.delay:
                    self.stream = self._open()

            super().emit(record)

        except Exception:
            self.handleError(record)