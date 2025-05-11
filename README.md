# 🏋️ Gym Management System

A web-based Gym Management System built with **Django**, **Python**, **HTML**, and **CSS**. This system is designed to help gym owners manage their members, trainers, subscriptions, and payments efficiently.

---

## 📌 Features

- ✅ User authentication (Admin login)
- ✅ Member registration and management
- ✅ Trainer profiles and assignments
- ✅ Subscription plans and **Stripe payment integration** 
- ✅ Dashboard overview with key metrics
- ✅ Responsive design using HTML and CSS

---

## 🛠️ Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS
- **Database:** Postgresql
- **Payment Integration:** Stripe
- **Others:** Django Admin Panel for data management

---

## 🚀 Getting Started

### 1. Clone the repository
(bash)
git clone https://github.com/faith-nye/gym-management-system.git
cd gym-management-system

2. Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
(bash)
pip install -r requirements.txt

4. Run migrations
python manage.py makemigrations
python manage.py migrate

5. Run the development server
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

6.🔐 Admin Access
python manage.py createsuperuser
Then log in at http://127.0.0.1:8000/admin

📂 Project Structure
gym-management-system/
│
├── gymManageSys/                # Main Django app
├── main-templates         # HTML templates
├── main-static            # CSS files
├── .env                # Environment variables (Stripe keys)
├── db.sqlite3          # SQLite database
├── manage.py
└── requirements.txt
