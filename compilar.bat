@echo off
cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
  call "venv\Scripts\activate.bat"
) else (
  echo Aviso: "venv\Scripts\activate.bat" nao encontrado. Continuando sem ativar venv.
)

python -m PyInstaller -F -w ".\main.py" --name "bot_Whatsapp" ^
  --hidden-import=comtypes ^
  --hidden-import=comtypes.client ^
  --hidden-import=comtypes.automation ^
  --hidden-import=comtypes.stream ^
  --hidden-import=comtypes.gen ^
  --hidden-import=pywinauto.uia_defines

exit /b %errorlevel%