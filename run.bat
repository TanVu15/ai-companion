@echo off
chcp 65001 >nul
title Bo - nguoi ban AI
REM Chay "nguoi ban" tren Windows. Lan dau tu tao moi truong va cai thu vien.
REM Co loi thi cua so KHONG tu tat, de Tan doc duoc loi.
cd /d "%~dp0"

REM 1. Tim Python (thu "py" truoc, roi "python"; "python" cua Microsoft Store gia thi bo qua)
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if not defined PY (
  echo.
  echo [LOI] Khong tim thay Python tren may.
  echo  - Tai Python tai https://www.python.org/downloads/
  echo  - Luc cai NHO tick o "Add Python to PATH", roi chay lai run.bat.
  echo.
  pause
  exit /b 1
)
echo Dung Python: & %PY% --version

REM 2. Tao moi truong rieng .venv (hong thi tao lai)
if exist .venv if not exist .venv\Scripts\python.exe rmdir /s /q .venv
if not exist .venv\Scripts\python.exe (
  echo Lan dau chay: dang tao moi truong .venv ...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo.
    echo [LOI] Khong tao duoc .venv. Chup man hinh cua so nay gui vao FEEDBACK.md nha.
    pause
    exit /b 1
  )
)
set "VPY=.venv\Scripts\python.exe"

REM 3. Cai / kiem tra thu vien (nhanh neu da du)
echo Dang kiem tra thu vien (lan dau mat vai phut) ...
"%VPY%" -m pip install -q --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo.
  echo [LOI] Cai thu vien that bai. Kiem tra mang Internet roi chay lai.
  echo Van loi thi xoa thu muc .venv va chay lai run.bat.
  pause
  exit /b 1
)
if not exist .env copy .env.example .env >nul

REM 4. Cong 8000 dang bi chiem (thuong la cua so run.bat cu con mo)
netstat -ano | findstr /r /c:":8000 .*LISTENING" >nul
if not errorlevel 1 (
  echo.
  echo [CHU Y] Cong 8000 dang duoc dung - co the Bo da chay o cua so khac.
  echo Mo trinh duyet vao http://localhost:8000 . Neu khong vao duoc, tat cua so cu roi chay lai.
  start "" http://localhost:8000
  pause
  exit /b 0
)

echo.
echo ============================================================
echo  Bo dang chay. Trinh duyet se tu mo: http://localhost:8000
echo  Tren iPhone (cung wifi): http://[IP may tinh]:8000  (xem IP bang lenh ipconfig)
echo  DE NGUYEN cua so nay khi dung Bo. Tat cua so = tat Bo.
echo ============================================================
echo.
REM Mo trinh duyet sau 4 giay (cho may chu khoi dong xong)
start "" /b cmd /c "ping -n 5 127.0.0.1 >nul & start "" http://localhost:8000"
"%VPY%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000

echo.
echo [Bo da dung] Neu co dong bao loi o tren, chup man hinh gui vao FEEDBACK.md nha.
pause
