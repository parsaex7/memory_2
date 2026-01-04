# Setup Nginx and Gunicorn for Memory Slideshow

This guide will help you set up Nginx and Gunicorn on your server without a domain name (IP access only).

## Your Configuration

- **Project Path**: `/root/memory_2`
- **Django Project**: `/root/memory_2/myMemory`
- **Virtual Environment**: `/root/memory_2/venv`
- **Access**: Server IP address (no domain)

## Step 1: Configure Gunicorn Service

### 1.1 Copy service file
```bash
sudo cp /root/memory_2/myMemory/memory-slideshow.service /etc/systemd/system/
```

### 1.2 Create socket directory and file
```bash
sudo mkdir -p /run
sudo touch /run/memory-slideshow.sock
sudo chown root:www-data /run/memory-slideshow.sock
sudo chmod 660 /run/memory-slideshow.sock
```

### 1.3 Enable and start Gunicorn service
```bash
sudo systemctl daemon-reload
sudo systemctl start memory-slideshow
sudo systemctl enable memory-slideshow
sudo systemctl status memory-slideshow
```

### 1.4 Check Gunicorn logs (if errors)
```bash
sudo journalctl -u memory-slideshow -f
```

## Step 2: Configure Nginx

### 2.1 Copy Nginx configuration
```bash
sudo cp /root/memory_2/myMemory/nginx.conf /etc/nginx/sites-available/memory-slideshow
```

### 2.2 Enable the site
```bash
sudo ln -s /etc/nginx/sites-available/memory-slideshow /etc/nginx/sites-enabled/
```

### 2.3 Remove default Nginx site (optional)
```bash
sudo rm /etc/nginx/sites-enabled/default
```

### 2.4 Test Nginx configuration
```bash
sudo nginx -t
```

If test passes, restart Nginx:
```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

## Step 3: Configure Firewall

```bash
# Allow HTTP (port 80)
sudo ufw allow 80/tcp

# Allow SSH (if not already allowed)
sudo ufw allow 22/tcp

# Check firewall status
sudo ufw status
```

## Step 4: Check Your Server IP

```bash
# Find your server's IP address
ip addr show
# or
hostname -I
```

## Step 5: Update Django Settings

Make sure your `.env` file includes the server IP:

```bash
cd /root/memory_2/myMemory
nano .env
```

Add your server IP to `ALLOWED_HOSTS`:
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,YOUR_SERVER_IP
```

Replace `YOUR_SERVER_IP` with your actual server IP address.

## Step 6: Collect Static Files (if not done)

```bash
cd /root/memory_2/myMemory
source ../venv/bin/activate
python manage.py collectstatic --noinput
```

## Step 7: Set Proper Permissions

```bash
# Set ownership
sudo chown -R root:www-data /root/memory_2/myMemory
sudo chown -R root:www-data /root/memory_2/staticfiles
sudo chown -R root:www-data /root/memory_2/myMemory/memories/media

# Set permissions
sudo chmod -R 755 /root/memory_2/myMemory
sudo chmod -R 775 /root/memory_2/myMemory/memories/media
sudo chmod -R 755 /root/memory_2/staticfiles
```

## Step 8: Test Your Application

1. **Check Gunicorn is running**:
   ```bash
   sudo systemctl status memory-slideshow
   ```

2. **Check Nginx is running**:
   ```bash
   sudo systemctl status nginx
   ```

3. **Check socket exists**:
   ```bash
   ls -la /run/memory-slideshow.sock
   ```

4. **Test in browser**: 
   - Open `http://YOUR_SERVER_IP` in your browser
   - Replace `YOUR_SERVER_IP` with your actual server IP

## Troubleshooting

### Gunicorn won't start
```bash
# Check logs
sudo journalctl -u memory-slideshow -n 50

# Check if socket file exists
ls -la /run/memory-slideshow.sock

# Verify paths in service file
sudo systemctl cat memory-slideshow
```

### 502 Bad Gateway
```bash
# Check Gunicorn is running
sudo systemctl status memory-slideshow

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify socket permissions
ls -la /run/memory-slideshow.sock
sudo chown root:www-data /run/memory-slideshow.sock
sudo chmod 660 /run/memory-slideshow.sock
```

### Static files not loading
```bash
# Verify static files directory
ls -la /root/memory_2/staticfiles/

# Check Nginx can access the directory
sudo nginx -t

# Verify STATIC_ROOT in settings.py matches Nginx alias
# It should be: /root/memory_2/staticfiles
```

### Permission denied errors
```bash
# Make sure www-data can read the files
sudo chown -R root:www-data /root/memory_2/staticfiles
sudo chmod -R 755 /root/memory_2/staticfiles
sudo chmod -R 775 /root/memory_2/myMemory/memories/media
```

## Useful Commands

```bash
# Restart services
sudo systemctl restart memory-slideshow
sudo systemctl restart nginx

# View logs
sudo journalctl -u memory-slideshow -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check service status
sudo systemctl status memory-slideshow
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# Reload Nginx (without downtime)
sudo nginx -s reload
```

## Notes

- **No Domain Name**: This configuration uses `server_name _;` to accept any hostname/IP
- **IP Address Access**: Access your site via `http://YOUR_SERVER_IP`
- **SSL Not Configured**: For SSL/HTTPS, you'll need a domain name (or use self-signed certificate)
- **Root User**: The service runs as root user. For production, consider creating a dedicated user

## Next Steps (Optional)

1. **Create dedicated user** (more secure):
   ```bash
   sudo adduser --disabled-password --gecos "" memoryapp
   sudo usermod -aG www-data memoryapp
   # Update service file to use memoryapp user
   # Move project to /home/memoryapp/memory_2
   ```

2. **Set up SSL** (requires domain name):
   - Get a free domain name (e.g., from Freenom, NoIP, etc.)
   - Use Let's Encrypt with Certbot

3. **Configure backups** for database and media files

4. **Set up monitoring** to track server performance

