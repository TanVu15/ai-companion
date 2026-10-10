@echo off
REM Chạy "người bạn" trên Windows. Lần đầu sẽ tự tạo môi trường và cài thư viện.
cd /d "%~dp0"
if not exist .venv (
  python -m venv .venv
  call .venv\Scripts\activate
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate
)
if not exist .env copy .env.example .env
echo.
echo Mo trinh duyet: http://localhost:8000
echo Tren iPhone (cung wifi): http://[IP may tinh]:8000  - xem IP bang lenh ipconfig
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
