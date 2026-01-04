# Memory Slideshow - Memorial Platform

A modern, minimal Django application for creating and sharing memorial slideshows.

## Features

- Beautiful, minimal design suitable for memorial purposes
- Bilingual support (English/Farsi)
- Modern slideshow interface with smooth animations
- Admin panel for easy content management
- Responsive design for all devices

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Memory/myMemory
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file and set your SECRET_KEY and other variables
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
TIME_ZONE=UTC
```

**Important**: Change the `SECRET_KEY` to a random string in production. You can generate one using:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Production Deployment

### Using Gunicorn

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn myMemory.wsgi:application --bind 0.0.0.0:8000
   ```

### Using Nginx + Gunicorn (Recommended)

1. **Install Nginx**
   ```bash
   sudo apt-get update
   sudo apt-get install nginx
   ```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/mymemory`)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /path/to/myMemory/staticfiles/;
       }

       location /media/ {
           alias /path/to/myMemory/memories/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/mymemory /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **Run Gunicorn as a service** (Create `/etc/systemd/system/mymemory.service`)
   ```ini
   [Unit]
   Description=Gunicorn daemon for Memory Slideshow
   After=network.target

   [Service]
   User=your-user
   Group=www-data
   WorkingDirectory=/path/to/myMemory
   ExecStart=/path/to/venv/bin/gunicorn myMemory.wsgi:application --bind 127.0.0.1:8000

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start the service**
   ```bash
   sudo systemctl start mymemory
   sudo systemctl enable mymemory
   ```

### Using systemd (Alternative)

Create a service file at `/etc/systemd/system/mymemory.service`:

```ini
[Unit]
Description=Memory Slideshow Django Application
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/myMemory
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn myMemory.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start mymemory
sudo systemctl enable mymemory
```

## Project Structure

```
myMemory/
├── accounts/          # User accounts app
├── core/              # Core templates and static files
├── memories/          # Main slideshow app
├── myMemory/          # Project settings
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── env.example        # Environment variables template
└── README.md          # This file
```

## Admin Panel

Access the admin panel at `/admin/` after creating a superuser.

Default admin site customization:
- Site Header: "Memory Slideshow Administration"
- Site Title: "Memory Admin"

## Static Files

Static files are collected to the `staticfiles/` directory. Run `collectstatic` before deployment:

```bash
python manage.py collectstatic --noinput
```

## Media Files

Media files (uploaded images, videos, audio) are stored in `memories/media/`.

Make sure this directory is writable by the web server:
```bash
chmod -R 755 memories/media/
```

## Database

The default database is SQLite (`db.sqlite3`). For production, consider using PostgreSQL:

1. Install PostgreSQL and psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update settings.py to use PostgreSQL
3. Update DATABASES configuration in settings.py

## Troubleshooting

### Static files not loading
- Run `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL in settings.py
- Verify Nginx/Apache configuration for static files

### Media files not loading
- Check MEDIA_ROOT and MEDIA_URL in settings.py
- Verify file permissions on media directory
- Check web server configuration

### 500 Internal Server Error
- Check DEBUG=False in production
- Review error logs: `python manage.py check --deploy`
- Check ALLOWED_HOSTS setting

## Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Generate a new SECRET_KEY
- [ ] Set ALLOWED_HOSTS to your domain
- [ ] Use HTTPS (SSL/TLS)
- [ ] Keep dependencies updated
- [ ] Use strong database passwords
- [ ] Restrict file permissions
- [ ] Regularly backup database and media files

## License

[Your License Here]

## Support

For issues and questions, please contact [Your Contact Information]

