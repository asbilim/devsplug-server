# Devsplug Server

A Django-based platform for coding challenges with social features and gamification.

## 🌟 Features

- **Coding Challenges**

  - Multiple difficulty levels
  - Point-based rewards
  - Solution submissions
  - Code documentation

- **Social Features**

  - Follow other developers
  - Like/dislike solutions
  - Comment on submissions
  - Private/public solutions

- **User Progress**
  - Experience points
  - Achievement titles
  - Progress tracking
  - Leaderboards

## 🛠️ Tech Stack

- Django 3.2+
- Django REST Framework
- JWT Authentication
- SQLite/PostgreSQL
- Custom Test Runner

## 🚀 Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/devsplug-server.git
cd devsplug-server
```

2. Set up virtual environment:

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Example test output:

```
================================================================================
📊 Test Execution Report
================================================================================

📁 authentication.tests
--------------------------------------------------------------------------------
✅ test_user_login
   📝 Test user login with valid credentials
   📥 Response:
      • Status: Success
      • Data: {'access_token': 'Received'}

✅ test_follow_user
   📝 Test that a user can successfully follow another user
   📥 Response:
      • Status: Created Successfully
...
```

## 📚 Documentation

For detailed documentation about:

- API Endpoints
- Models & Database Schema
- Testing Infrastructure
- Development Guidelines

See [Documentation.md](Documentation.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Write tests for your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **asbilim** - _Initial work_ - [GitHub](https://github.com/asbilim)

## 🙏 Acknowledgments

- Django community
- All contributors
- Open source community
