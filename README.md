# Investment App 📈

A robust Django-based application for tracking investments, performing financial calculations, and managing investment portfolios.

## 🌟 Features

- **User Authentication System**: Secure login, registration, and password reset functionality
- **Investment Management**: Add, edit, and delete investments
- **Product Management**: Track various investment products
- **Financial Calculators**: 
  - Monthly SIP (Systematic Investment Plan) calculator
  - One-time investment calculator with return projections
- **Dashboard**: Visual overview of investments and financial position
- **Responsive Design**: Works seamlessly across desktop and mobile devices


![](Investment\InvestmentApp\static\i1.png)
![](Investment\InvestmentApp\static\i2.png)
![](Investment\InvestmentApp\static\i3.png)
![](Investment\InvestmentApp\static\i4.png)
![](Investment\InvestmentApp\static\i5.png)

## 📋 Requirements

- Python 3.11+
- Django 5.1+
- Modern web browser

## 🚀 Installation

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd InvestmentApp
   ```

2. **Set up a virtual environment**
   ```
   python -m venv env
   ```

3. **Activate the environment**
   - Windows:
   ```
   env\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source env/bin/activate
   ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
   
   If requirements.txt is not available, install Django:
   ```
   pip install django
   ```

5. **Set up the database**
   ```
   cd Investment
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```
   python manage.py runserver
   ```

8. **Access the application** at http://127.0.0.1:8000/

## 🧪 Using the App

1. **Register** a new account or login with your credentials
2. **Add products** through the admin interface
3. **Make investments** using the dashboard interface
4. **Calculate returns** using the SIP or one-time investment calculators
5. **Track performance** of your investments over time

## 👩‍💻 Admin Access

Access the admin interface at http://127.0.0.1:8000/admin/ using your superuser credentials to:
- Manage users
- Add investment products
- Manage investments
- View system data

## 🛠️ Project Structure

```
Investment/
├── Investment/               # Project settings
├── InvestmentApp/            # Main application
│   ├── migrations/           # Database migrations
│   ├── static/               # Static files (CSS, JS, images)
│   ├── templates/            # HTML templates
│   │   └── Investment/       # App-specific templates
│   ├── admin.py              # Admin interface configuration
│   ├── models.py             # Database models
│   ├── views.py              # View controllers
│   └── urls.py               # URL routing
└── manage.py                 # Django management script
```

## 📝 Notes

- This project uses SQLite by default for development
- For production, consider using PostgreSQL or MySQL
- Email settings are configured to output to console - configure your SMTP settings for real email delivery

---

Made with ❤️ using Django