# Quick Setup Guide

## For First-Time Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Memory/myMemory
   ```

2. **Run the deployment script**
   ```bash
   bash deploy.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env file with your settings
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

3. **Edit .env file**
   ```bash
   nano .env  # or use your preferred editor
   ```
   
   Set at minimum:
   - `SECRET_KEY` - Generate a new one for production
   - `DEBUG=False` for production
   - `ALLOWED_HOSTS=your-domain.com,www.your-domain.com`

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Generate SECRET_KEY

```bash
python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py collectstatic`
- [ ] Configure web server (Nginx/Apache)
- [ ] Set up SSL/HTTPS
- [ ] Configure firewall
- [ ] Set up backups
- [ ] Test the application

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Check for issues
python manage.py check --deploy
```

## Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3 python3-venv python3-pip nginx -y

# Clone and setup (follow steps above)

# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn myMemory.wsgi:application --bind 0.0.0.0:8000

# Or create systemd service (see README.md)
```

