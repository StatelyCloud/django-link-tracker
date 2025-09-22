# 🔗 LinkTracker - Django + StatelyDB Tutorial

A modern link tree application built with Django and StatelyDB - learn how to integrate StatelyDB with Django for real-time data management!

## ✨ Features

- **Scalable**: Powered by StatelyDB for your first billion users
- **Beautiful Profiles**: Create stunning profile pages with customizable names and emojis
- **Unlimited Links**: Add as many links as you want with custom emojis and descriptions
- **Analytics**: Track views and clicks on your profile and links
- **Mobile First**: Fully responsive design that looks great on all devices
- **Modern UI**: Hip, gradient-filled design with smooth animations

## Prerequisites

* **Stately CLI**
   ```bash
   curl -sL https://stately.cloud/install | sh
   stately login
   ```
* **Python 3**
  
  >Setup is system dependent

## 🚀 Quick Start

Click this button and follow the steps to get your app running!

[![Build with Stately](https://gist.githubusercontent.com/ryan-stately/51a07a4b3123f5cb89c8b9a1f3edf214/raw/158cb441aa65d05dd1a75b85dffad2feeb473f6b/build-icon.svg)](https://console.stately.cloud/new?repo=https%3A%2F%2Fgithub.com%2FStatelyCloud%2Fdjango-link-tracker)

### Local Development

These steps are provided as reference but you should have preformed the same steps when you bootstrapped your project above.

**Clone and Install Dependencies**
```bash Clone the Repository
git clone https://github.com/StatelyCloud/django-link-tracker
cd django-link-tracker
```
**Install Dependencies**
```bash Install Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**Login and Generate the SDK**
```bash Login and Generate the SDK
stately login
stately schema generate --language python --schema-id $SCHEMA_ID ./generated
```

### **Run the Application**
Finally, run the link tracker application!

```bash
uvicorn linktracker.asgi:application --reload --port 8000
```

### **Visit the App**

- Home page: http://127.0.0.1:8000/
- Create your first profile and start adding links!

## 📁 Project Structure

```
django-link-tracker/
├── linktracker/          # Django project settings
│   ├── settings.py      # Configuration with StatelyDB setup
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application (for uvicorn)
├── app/                 # Main Django app
│   ├── models.py        # StatelyDB model imports
│   ├── views.py         # Async views using StatelyDB
│   ├── urls.py          # App URL patterns
│   ├── stately_client.py # StatelyDB integration layer
│   ├── tests.py         # Test suite
│   └── utils.py         # Helper functions
├── templates/app/       # HTML templates
├── static/              # CSS, JS, images
├── generated/           # StatelyDB generated code
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## 🔗 StatelyDB Integration

This tutorial demonstrates key StatelyDB concepts:

### **Models** (`app/stately_client.py`)

- **Profile**: User profiles with view tracking
- **Link**: Individual links with click analytics

### **Async Views** (`app/views.py`)

- Async/await pattern for StatelyDB operations
- Integrated analytics tracking

### **Key Functions**

- `get_profile_and_links()` - Efficiently fetch profile and all links in single call
- `create_profile()` - Create new profiles
- `increment_profile_views()` - Real-time analytics
- `create_link()` - Add links to profiles

## 🎨 Customization

### **Adding Link Types**

Edit the select options in `templates/app/profile_edit.html` to add new link categories.

### **Styling**

All styles are in `static/css/styles.css` with CSS custom properties for easy theming.

### **StatelyDB Schema**

Check `generated/stately_item_types.py` to see the auto-generated StatelyDB models.

## 🛠️ StatelyDB Models

### **Profile**

- `id`: Unique identifier
- `slug`: URL-friendly name
- `full_name`: Display name
- `bio`: Profile description
- `profile_image`: Emoji or image
- `view_count`: Analytics tracking
- `is_active`: Visibility control

### **Link**

- `id`: Unique identifier
- `profile_id`: Associated profile
- `title`: Link display text
- `url`: Target URL
- `emoji`: Display icon
- `link_type`: Category (social, portfolio, etc.)
- `click_count`: Analytics tracking
- `order`: Display ordering
- `is_active`: Visibility control

## 🔧 Technical Details

- **Django 4.2+**: Modern async Django with StatelyDB
- **StatelyDB**: Real-time cloud database
- **ASGI**: Async server interface with uvicorn
- **UUID Primary Keys**: Secure, distributed IDs
- **Responsive Design**: Mobile-first CSS Grid and Flexbox
- **Modern JavaScript**: ES6+ with smooth animations

## 🚀 Deployment

1. Set `DEBUG = False` in production
2. Configure `ALLOWED_HOSTS`
3. Set up static file serving
4. Use environment variables for StatelyDB credentials
5. Deploy with uvicorn or gunicorn with async workers

## 📚 Learning Resources

- [StatelyDB Documentation](https://docs.stately.cloud)
- [Django Async Views](https://docs.djangoproject.com/en/stable/topics/async/)
- [ASGI Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/asgi/)

## 🤝 Contributing

This is a tutorial project - feel free to fork and extend it for your learning!
