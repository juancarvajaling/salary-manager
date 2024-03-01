from io import BytesIO
import base64
from utils.salary_calculator import process_salary
from utils.source_data import read_days_data, read_employee_data
import json


def lambda_handler(event, context):
    print(f"Incoming event: {event}")

    b64_file = event["body"]
    b64_file_decoded = base64.b64decode(b64_file)
    salary_file = BytesIO(b64_file_decoded)

    employee_data = read_employee_data(salary_file)
    days_data, errors = read_days_data(salary_file, employee_data)
    if errors:
        return {
            "statusCode": 400,
            "body": json.dumps(errors)
        }

    processed_salary = process_salary(days_data, employee_data)

    return {
        "headers": {
            "Content-Disposition": 'attachment; filename="nomina.xlsx"',
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
        "statusCode": 200,
        "body": base64.b64encode(processed_salary.read()),
        "isBase64Encoded": True
    }
