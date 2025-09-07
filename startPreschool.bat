@echo off
cd /d "C:\Users\lenovo\AadiTech\AadiPortal\PreschoolERP\PRESchool-Backend-project"

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
pip install fastapi uvicorn sqlalchemy python-dotenv passlib[bcrypt] pyodbc pydantic[email] python-jose pydantic-settings python-multipart

:: Run the server
uvicorn app.main:app --reload

:: Keep window open
echo.
echo ============================
echo Server stopped or crashed.
echo Press any key to close...
pause > nul
