@echo off
echo ================================================
echo GIT PUSH - Push code len GitHub
echo ================================================
echo.

REM Kiem tra git da duoc khoi tao chua
if not exist ".git" (
    echo [!] Chua khoi tao Git repository!
    echo.
    echo Chay lenh nay truoc:
    echo   git init
    echo   git config user.name "Your Name"
    echo   git config user.email "your@email.com"
    echo   git remote add origin https://github.com/USERNAME/REPO.git
    echo.
    pause
    exit /b 1
)

echo [1] Kiem tra trang thai Git...
git status
echo.

echo [2] Them tat ca files (tru .gitignore)...
git add .
echo.

echo [3] Xem lai files se duoc commit:
echo ================================================
git status
echo ================================================
echo.

echo [!] QUAN TRONG: Kiem tra .env KHONG co trong list!
echo.
set /p confirm="Ban da kiem tra chua? (y/n): "
if /i not "%confirm%"=="y" (
    echo Huy bo!
    pause
    exit /b 1
)

echo.
set /p message="Nhap commit message: "

echo.
echo [4] Commit voi message: %message%
git commit -m "%message%"

echo.
echo [5] Push len GitHub...
git push

echo.
echo ================================================
echo [HOAN THANH] Code da duoc push len GitHub!
echo ================================================
pause
