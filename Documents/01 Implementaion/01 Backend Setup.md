## 1. create backend Environment  
```bash
python -m venv venv
```  
2. Activate Environment  
for bash/WSL:
```bash
source venv/Scripts/activate
```  
for CDM:
```cmd
venv\Scripts\activate.bat
```  
for powershell:
```powershell
venv\Scripts\Activate.ps1
```  
3. create requirements.txt file  
```bash
touch requirements.txt
```  
```txt
Flask
Flask-CORS
SQLAlchemy
PyMySQL
python-dotenv
pandas
pyds
```  
4. Install requirements  
```bash
pip install -r requirements.txt
```  
5. Entry point creation  
```python
# backend-flask-app/app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is your Flask Backend.'

if __name__ == '__main__':
    app.run(debug=True)
```  
## 6. backend environment variables  
```env
# backend-flask-app/.env
FLASK_APP=app.py
FLASK_ENV=development
# Add a placeholder for your database URI, we'll configure this properly later
DATABASE_URI="mysql+pymysql://user:password@localhost:3306/flood_data"
# For production, you'd add a secret key too:
# SECRET_KEY="your_super_secret_key_here"
```  
## 7. Run application  
```bash
flask run
```  
#### Output:  
```console
$ flask run
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [30/Jul/2025 19:09:58] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jul/2025 19:09:58] "GET /favicon.ico HTTP/1.1" 404 -
```  


```bash
alias python="./venv/Scripts/python.exe"
python --version
source venv/Scripts/activate
```  