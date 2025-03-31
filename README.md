# **Planit - Backend**  
 
This repository is the backend of the Planit application built with **Flask** that handles event creation, user availability tracking, and authentication. It provides a **RESTful API** to interact with the frontend and stores data in a **MySQL database**.  

## **Tech Stack**  
- **Backend Framework:** Flask  
- **Database:** MySQL  

## **Installation**  

### **1. Clone the repository**  
```bash
git clone ...
```

### **2. Set up a virtual environment**  
```bash
python -m venv .venv
```

#### **Activate the environment:**  
- **Windows:**  
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**  
  ```bash
  source venv/bin/activate
  ```

### **3. Install dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Set up the MySQL database**  
To set up the MySQL database take a look to this repository [MySQL Template](https://github.com/MarinCervinschi/flask-mysql-template)


### **6. Run Flask locally**  
```bash
py ./run.py
```
By default, the API will be available at: `http://localhost:5000`


## **Project Structure**  
```
planit-backend/
├── README.md                  # Documentation for the repository
├── LICENSE                    # License information
├── app/                       # Core application logic
│   ├── __init__.py            # App initialization
│   ├── config.py              # Configuration settings
│   ├── db.py                  # Database connection logic
│   └── routes/                # Application routes
│       ├── __init__.py        # Routes initialization
│       ├── routes...          # API routes
│       └── main.py            # Main application routes
├── docker-compose.yml         # Docker configuration for MySQL
├── requirements.txt           # Python dependencies
├── run.py                     # Entry point to run the Flask application
├── schema.sql                 # MySQL database schema
└── tests/                     # Testing suite
    ├── conftest.py            # Pytest fixtures and configurations
    ├── data.sql               # Sample data for tests
    ├── test_db.py             # Unit tests for `db.py`
    ├── test_db_route.py       # Unit tests for `db_route.py`
    ├── test_factory.py        # Unit tests for `factory.py`
    └── test_main.py           # Unit tests for `main.py`
```

## **Frontend Integration**  
This backend is designed to work with the [Planit Frontend](https://github.com/isabella-capp/Planit-FE).


## **Contributing**  
If you’d like to contribute:  
1. Fork the repository.  
2. Create a new branch (`feature-branch`).  
3. Commit your changes.  
4. Submit a pull request.  
