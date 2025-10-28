@echo off
echo ================================================
echo GIT SETUP - Thiet lap Git repository
echo ================================================
echo.

REM Kiem tra Git da cai chua
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Git chua duoc cai dat!
    echo Download tai: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git da duoc cai dat:
git --version
echo.

REM Kiem tra da khoi tao chua
if exist ".git" (
    echo [!] Git da duoc khoi tao roi!
    echo.
    git status
    pause
    exit /b 0
)

echo [1] Khoi tao Git repository...
git init
echo.

echo [2] Cau hinh thong tin cua ban:
set /p name="Nhap ten cua ban: "
set /p email="Nhap email cua ban: "

git config user.name "%name%"
git config user.email "%email%"

echo.
echo [OK] Da cau hinh:
git config user.name
git config user.email
echo.

echo [3] Them remote repository:
echo Vi du: https://github.com/username/my-ai-chatbot.git
set /p remote="Nhap URL GitHub repository: "

git remote add origin %remote%
echo.

echo [4] Doi ten branch thanh main:
git branch -M main
echo.

echo ================================================
echo [HOAN THANH] Git da san sang!
echo ================================================
echo.
echo Buoc tiep theo:
echo   1. Chay: git_push.bat de push code
echo   2. Hoac tu chay: git add . && git commit -m "message" && git push -u origin main
echo.
pause
