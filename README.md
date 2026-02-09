# 🚀 Smart Job Recommendation Portal (MVP)

## 📌 Project Overview

The **Smart Job Recommendation Portal** is a simple web application built using **Streamlit** and **Python**. It helps users find internships and jobs based on their skills, interests, location, and experience.

This project is designed as a **Minimum Viable Product (MVP)** to demonstrate job matching logic, user authentication, and database integration.

---

## ✨ Features

✅ User registration and login
✅ Admin authentication
✅ Job recommendation based on skills
✅ Location-based filtering
✅ Experience-based suggestions
✅ Lightweight SQLite database
✅ Easy-to-use Streamlit interface

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** SQLite
* **Data Handling:** Pandas

---

## 📂 Project Structure

```
job_portal_mvp/
│
├── app.py              # Main Streamlit application
├── auth.py             # User authentication logic
├── admin_auth.py       # Admin login functionality
├── database.py         # Database connection and operations
├── jobs.csv            # Job dataset
├── users.db            # SQLite database file
├── requirements.txt    # Project dependencies
```

---

## ⚙️ Installation Guide

Follow these steps to run the project locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/job-portal-mvp.git
cd job-portal-mvp
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

After running the command, open your browser and go to:

```
http://localhost:8501
```

---

## 🧠 How It Works

1. Users enter their skills, preferred location, interest, and experience.
2. The system compares user data with available jobs in **jobs.csv**.
3. A scoring algorithm ranks the jobs.
4. The best matches are displayed to the user.

---

## 🔐 Authentication

* Users must register before logging in.
* Admin login is handled separately for secure access.
* Credentials are stored in an SQLite database.

---

## 📊 Future Improvements

🚀 Add AI-based job matching
🚀 Resume upload and parsing
🚀 Email notifications
🚀 Advanced filters
🚀 Deploy on AWS / Streamlit Cloud
🚀 Improve UI design

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 👨‍💻 Author

**Puneeth Reddy**
If you like this project, consider giving it a ⭐ on GitHub!
