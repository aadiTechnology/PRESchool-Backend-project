@echo off
cd E:\Smartkidz\PRESchool-Backend-project

echo Activating virtual environment...
call venv\\Scripts\\activate

echo Starting FastAPI server...
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4

echo.
echo Press any key to close...
pause > nul