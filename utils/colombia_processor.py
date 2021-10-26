from configparser import ConfigParser
from datetime import datetime, timedelta
from io import BytesIO

from openpyxl import Workbook
from workalendar.america import Colombia


class ColombiaSalary:

    def __init__(self) -> None:
        self.__set_params()
        self.__set_working_time_map()

    def __set_params(self) -> None:
        config = ConfigParser()
        config.read('utils/colombia_params.ini')
        self.NORMAL_HOLIDAY = config.getfloat('normal', 'holiday')
        self.SURCHARGE_WEEK = config.getfloat('surcharge', 'week')
        self.SURCHARGE_HOLIDAY = config.getfloat('surcharge', 'holiday')
        self.EXTRA_WEEK_DAY = config.getfloat('extra', 'week_day')
        self.EXTRA_WEEK_NIGHT = config.getfloat('extra', 'week_night')
        self.EXTRA_HOLIDAY_DAY = config.getfloat('extra', 'holiday_day')
        self.EXTRA_HOLIDAY_NIGHT = config.getfloat('extra', 'holiday_night')
        self.SATURDARY = config.getint('work', 'saturday')
        self.NIGHT = config.getint('work', 'night')
        self.WORKING_MINS = config.getint('work', 'working_mins')
        self.ADDITIONAL_HOURS = config.getint('work', 'additional_hours')
        self.ADDITIONAL_MINS = config.getint('work', 'additional_mins')

    def __set_working_time_map(self):
        self.working_time_map = {
            'normal_hours': {
                'week_day': {
                    'day': {
                        'hours': 'normal_week_day_hours',
                        'value': 'normal_week_day_value',
                        'multiplier': 1
                    },
                    'night': {
                        'hours': 'surcharge_week_hours',
                        'value': 'surcharge_week_value',
                        'multiplier': self.SURCHARGE_WEEK
                    }
                },
                'holiday': {
                    'day': {
                        'hours': 'normal_holiday_day_hours',
                        'value': 'normal_holiday_day_value',
                        'multiplier': self.NORMAL_HOLIDAY
                    },
                    'night': {
                        'hours': 'surcharge_holiday_hours',
                        'value': 'surcharge_holiday_value',
                        'multiplier': self.SURCHARGE_HOLIDAY
                    }
                }
            },
            'extra_hours': {
                'week_day': {
                    'day': {
                        'hours': 'extra_week_day_hours',
                        'value': 'extra_week_day_value',
                        'multiplier': self.EXTRA_WEEK_DAY
                    },
                    'night': {
                        'hours': 'extra_week_night_hours',
                        'value': 'extra_week_night_value',
                        'multiplier': self.EXTRA_WEEK_NIGHT
                    }
                },
                'holiday': {
                    'day': {
                        'hours': 'extra_holiday_day_hours',
                        'value': 'extra_holiday_day_value',
                        'multiplier': self.EXTRA_HOLIDAY_DAY
                    },
                    'night': {
                        'hours': 'extra_holiday_night_hours',
                        'value': 'extra_holiday_night_value',
                        'multiplier': self.EXTRA_HOLIDAY_NIGHT
                    }
                }
            }
        }

    def __get_type_hour_data_names(self) -> list:
        type_hour_data_names = [
            {
                'Horas Ordinarias': {
                    'hours': 'normal_week_day_hours',
                    'value': 'normal_week_day_value'
                }
            },
            {
                'Horas Extras Diurnas': {
                    'hours': 'extra_week_day_hours',
                    'value': 'extra_week_day_value'
                }
            },
            {
                'Horas Extras Nocturna': {
                    'hours': 'extra_week_night_hours',
                    'value': 'extra_week_night_value'
                }
            },
            {
                'Recargos Nocturnos': {
                    'hours': 'surcharge_week_hours',
                    'value': 'surcharge_week_value'
                }
            },
            {
                'Horas Domin y Fest': {
                    'hours': 'normal_holiday_day_hours',
                    'value': 'normal_holiday_day_value'
                }
            },
            {
                'Horas Extras Diurnas Domin y Fest': {
                    'hours': 'extra_holiday_day_hours',
                    'value': 'extra_holiday_day_value'
                }
            },
            {
                'Horas Extras Nocturnas Domin y Fest': {
                    'hours': 'extra_holiday_night_hours',
                    'value': 'extra_holiday_night_value'
                }
            },
            {
                'Recargos Nocturnos Domin y Fest': {
                    'hours': 'surcharge_holiday_hours',
                    'value': 'surcharge_holiday_value'
                }
            }
        ]
        return type_hour_data_names

    def __get_working_time(self, a_date: datetime, num_mins: int) -> dict:
        type_hour = 'normal_hours' if num_mins <= self.WORKING_MINS else 'extra_hours'

        week_day = a_date.weekday() == self.SATURDARY or Colombia().is_working_day(a_date)
        type_day = 'week_day' if week_day else 'holiday'

        type_time = 'day' if a_date.hour < self.NIGHT else 'night'

        return self.working_time_map[type_hour][type_day][type_time]


    def __compute_salary_by_hours(self, days_data: list, employee_data: dict):
        print('Calculando nomina...')
        for day in days_data:
            id = day['id']
            employee = employee_data.get(id)
            value_minute = employee['salary_base'] / 240 / 60
            start_on: datetime = day['start_on']
            end_on: datetime = day['end_on']
            num_mins = 1
            while start_on < end_on:
                working_time = self.__get_working_time(start_on, num_mins)

                employee_data[id][working_time['hours']] += 1 / 60
                employee_data[id][working_time['value']] += (
                    value_minute * working_time['multiplier']
                )

                start_on += timedelta(minutes=1)
                num_mins += 1
        
        for id in employee_data.keys():
            employee_data[id]['normal_week_day_hours'] += self.ADDITIONAL_HOURS
            employee_data[id]['normal_week_day_value'] += value_minute * self.ADDITIONAL_MINS

        return employee_data

    def create_salary_file(self, days_data: list, employee_data: dict):
        type_hour_data_names_list = self.__get_type_hour_data_names()

        employee_data = self.__compute_salary_by_hours(days_data, employee_data)

        wb = Workbook()
        ws = wb.active
        ws.title = 'salarios calculados'
        for key, employee in employee_data.items():
            ws.append(['CEDULA', '', key])
            ws.append(['NOMBRE', '', employee['name']])
            ws.append(['Descripción', 'Horas', 'Valor Horas'])
            for type_hour_data_names in type_hour_data_names_list:
                for type_hour, data_names in type_hour_data_names.items():
                    if employee[data_names['hours']] == 0:
                        continue

                    hours = round(employee[data_names['hours']], 2)
                    hours_value = round(employee[data_names['value']], 2)
                    row = [type_hour, hours, hours_value]
                    ws.append(row)

            ws.append(['', '', ''])

        processed_salary = BytesIO()
        wb.save(processed_salary)
        processed_salary.seek(0)
        print('Calculo de nomina hecha!')
        return processed_salary