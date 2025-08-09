from io import BytesIO

from utils.colombia_processor import ColombiaSalary


def process_salary(days_data: list, employee_data: dict) -> BytesIO:
    colombia_salary = ColombiaSalary()
    processed_salary = colombia_salary.create_salary_file(days_data, employee_data)
    return processed_salary
