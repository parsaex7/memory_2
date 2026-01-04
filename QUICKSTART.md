# Quick Start Guide

Get your Memory Slideshow application running in minutes!

## Option 1: Using the Deployment Script (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Memory/myMemory

# Run the deployment script
bash deploy.sh

# Edit environment variables
nano .env  # Set SECRET_KEY, DEBUG, ALLOWED_HOSTS

# Create superuser (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

That's it! Your application will be running at `http://127.0.0.1:8000/`

## Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp env.example .env
nano .env  # Edit and set your values

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## Environment Variables (.env file)

Minimum required settings:

```env
SECRET_KEY=your-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

Generate a SECRET_KEY:
```bash
python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## First Steps After Setup

1. **Access Admin Panel**: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. **Create a Memorial Slideshow**:
   - Go to Admin Panel
   - Add a Memory Slideshow
   - Upload images, videos, and media
   - View at: `/slideshows/<slug>/en/` or `/slideshows/<slug>/fa/`

## Production Deployment

For production, see README.md for detailed instructions on:
- Using Gunicorn
- Setting up Nginx
- Creating systemd service
- SSL/HTTPS configuration
- Security settings

## Troubleshooting

**Static files not loading?**
```bash
python manage.py collectstatic
```

**Database errors?**
```bash
python manage.py migrate
```

**Permission errors?**
```bash
chmod -R 755 memories/media/
```

**Check for issues:**
```bash
python manage.py check --deploy
```

## Need Help?

- Check README.md for detailed documentation
- See SETUP.md for step-by-step setup guide
- Review environment variables in env.example

