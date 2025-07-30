## **Frontend:**

* **Framework:** **Next.js** (React Framework)
* **Chart Library:** **Chart.js** (for ease of use, with options to integrate D3.js, Plotly.js, Apache ECharts for more complex needs)
* **CSS Framework:** **Bootstrap 5+**
* **Icons:** **Font Awesome**

## ***Backend:**

* **Language:** **Python**
* **Web Framework:** **Flask**
* **Database:** **MySQL**

```bash
C:\Users\RaSkull>C:\Users\RaSkull\AppData\Local\Programs\Python\Python39\python.exe --version
Python 3.9.12
```  
```bash
pydss
pandas
Flask-SQLAlchemy
PyMySQL
python-dotenv
waitress
APScheduler 
```  
```txt
# Core Flask application
Flask==2.3.3 # A stable release from the 2.x series

# DSS File Processing
pydsstools==1.5.0 # Latest stable release as of late 2024 / early 2025 - check PyPI for the absolute newest if needed
pandas==2.1.4 # A recent, stable version for data manipulation

# Database Interaction
Flask-SQLAlchemy==3.1.1 # Latest stable release for SQLAlchemy integration
PyMySQL==1.1.0 # Compatible MySQL driver

# Utility & Deployment
python-dotenv==1.0.0 # For environment variable management
waitress==2.1.2 # Production-ready WSGI server for Windows/cross-platform
APScheduler==3.10.4 # For future automated alert scheduling (if implemented)
```  
## ***Data Conversion (DSS Parsing):**

* **Primary Tool:** **`pydss` Python library** (as a community open-source effort for reading DSS files)
* **Fallback/Alternative:** **Jython** to interface with the (non-open-source but callable) HEC-DSS Java libraries, executed from your Python backend. This would be a server-side dependency.