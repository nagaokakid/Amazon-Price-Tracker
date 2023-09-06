@ECHO OFF

rmdir /s .\venv

echo Creating virtual environment...
python3 -m venv venv
echo Success!

echo Copying program files into virtual environment...
md .\venv\app\
md .\venv\app\data
md .\venv\app\logic
md .\venv\app\presentation
xcopy /i /s ".\data" ".\venv\app\data"
xcopy /i /s ".\logic" ".\venv\app\logic"
xcopy /i /s ".\presentation" ".\venv\app\presentation"
xcopy /i ".\requirements.txt" ".\venv\app"
xcopy /i ".\main.py" ".\venv\app"
echo Success!

echo Installing requirements...
pip install -r .\venv\app\requirements.txt
echo Success!

echo Running app...
.\venv\Scripts\activate
python3 .\venv\app\main.py
pause