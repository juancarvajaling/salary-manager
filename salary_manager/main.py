from io import BytesIO

from fastapi import FastAPI, File, UploadFile, Request, status
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.salary_calculator import process_salary
from utils.source_data import read_days_data, read_employee_data

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/calculate-salary/', response_class=HTMLResponse)
async def calculate_salary_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/calculate-salary/', response_class=StreamingResponse)
async def calculate_salary_post(request: Request, upload_file: UploadFile = File(...)):
    file_content = await upload_file.read()
    salary_file = BytesIO(file_content)

    employee_data = read_employee_data(salary_file)
    days_data, errors = read_days_data(salary_file, employee_data)
    if errors:
        return templates.TemplateResponse(
            'index.html', {'request': request, 'errors': errors},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    processed_salary = process_salary(days_data, employee_data)

    headers = {
        'Content-Disposition': 'attachment; filename="nomina.xlsx"'
    }
    return StreamingResponse(processed_salary, headers=headers)
