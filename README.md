# 🌐 Social Media Django Project

Welcome to the **Social Media Django Project**! This feature-rich social media application is built with Django and empowers users to connect, share posts, and engage with each other seamlessly.

![Social Media](https://github.com/user-attachments/assets/8d83e566-be63-43fe-87b9-764976b79818)

---

## ✨ Features

- 🔐 **User Authentication**: Secure signup, login, and logout functionality.
- 👤 **Profile Management**: Create, update, and personalize user profiles.
- 📝 **Post Management**: Effortlessly create, edit, and delete posts.
- 💬 **Commenting**: Engage with posts through a robust commenting system.
- 🔄 **Follow/Unfollow**: Connect with other users by following or unfollowing them.
- 🖼️ **Media Handling**: Upload and showcase images and videos.
- 🛠️ **Admin Panel**: Manage users, posts, and other content using Django's admin interface.

---

## 🚀 Installation

Follow these steps to set up the project locally:

### 1⃣️ Clone the Repository

```bash
git clone https://github.com/CodeWithRanjHa/Social-Media-Django.git
cd Social-Media-Django
```

### 2⃣️ Create and Activate a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3⃣️ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4⃣️ Configure the Database

This project uses MySQL as the database. Ensure you have MySQL installed and configured on your system. Update the `settings.py` file with the following configuration:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": "path/to/file/my.cnf",
        },
    }
}
```

### 5⃣️ Apply Migrations

```bash
python manage.py migrate
```

### 6⃣️ Run the Development Server

```bash
python manage.py runserver
```

---

## 🛠️ Usage

1. Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
2. To access the admin panel, go to: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

---

## 🤝 Contributing

We welcome contributions to enhance this project! Here's how you can help:

- Submit pull requests with new features or bug fixes.
- Raise issues to report bugs or suggest improvements.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear and concise messages.
4. Push to your branch and create a pull request.

---

## 📞 Connect with Me

Stay connected and follow me on:

- [🎥 YouTube](https://www.youtube.com/channel/UCnf5YYtH3mgjex2hx1UWGAg)  
- [💼 LinkedIn](https://www.linkedin.com/in/wasim-ranjhaa/)  
- [💻 GitHub](https://github.com/CodeWithRanjHa)  
- [👥 Facebook](https://web.facebook.com/wasimranjhaa)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

### Made with ❤️ by [CodeWithRanjHa](https://github.com/CodeWithRanjHa) ✨
