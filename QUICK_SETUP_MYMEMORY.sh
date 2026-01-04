#!/bin/bash
# Quick setup script for Nginx and Gunicorn
# Run this on your server: bash QUICK_SETUP_MYMEMORY.sh

set -e

echo "=== Memory Slideshow - Nginx & Gunicorn Setup (mymemory site) ==="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="/etc/systemd/system/memory-slideshow.service"
NGINX_FILE="/etc/nginx/sites-available/mymemory"
SOCKET_FILE="/run/memory-slideshow.sock"

echo "Script directory: $SCRIPT_DIR"
echo "Project directory: $PROJECT_DIR"
echo "Nginx site: mymemory"
echo ""

# Step 1: Copy Gunicorn service file
echo "[1/6] Setting up Gunicorn service..."
if [ -f "$SCRIPT_DIR/memory-slideshow.service" ]; then
    cp "$SCRIPT_DIR/memory-slideshow.service" $SERVICE_FILE
    echo "✓ Service file copied"
else
    echo "✗ Error: memory-slideshow.service not found in $SCRIPT_DIR"
    exit 1
fi

# Step 2: Create socket file
echo "[2/6] Creating socket file..."
mkdir -p /run
touch $SOCKET_FILE
chown root:www-data $SOCKET_FILE
chmod 660 $SOCKET_FILE
echo "✓ Socket file created"

# Step 3: Enable and start Gunicorn
echo "[3/6] Starting Gunicorn service..."
systemctl daemon-reload
systemctl start memory-slideshow
systemctl enable memory-slideshow
sleep 2
systemctl status memory-slideshow --no-pager -l || echo "⚠ Check service status manually"
echo "✓ Gunicorn service started"

# Step 4: Setup Nginx (update existing mymemory site)
echo "[4/6] Updating Nginx configuration..."
cp /etc/nginx/sites-available/mymemory /etc/nginx/sites-available/mymemory.backup 2>/dev/null || true
if [ -f "$SCRIPT_DIR/nginx_mymemory.conf" ]; then
    cp "$SCRIPT_DIR/nginx_mymemory.conf" $NGINX_FILE
else
    echo "✗ Error: nginx_mymemory.conf not found in $SCRIPT_DIR"
    exit 1
fi
# Site should already be enabled, but check
if [ ! -L /etc/nginx/sites-enabled/mymemory ]; then
    ln -s $NGINX_FILE /etc/nginx/sites-enabled/mymemory
fi
echo "✓ Nginx configuration updated"

# Step 5: Test and restart Nginx
echo "[5/6] Testing Nginx configuration..."
nginx -t
if [ $? -eq 0 ]; then
    systemctl restart nginx
    echo "✓ Nginx restarted successfully"
else
    echo "✗ Nginx configuration test failed!"
    echo "Restoring backup..."
    cp /etc/nginx/sites-available/mymemory.backup $NGINX_FILE 2>/dev/null || true
    exit 1
fi

# Step 6: Setup firewall
echo "[6/6] Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 22/tcp
    echo "✓ Firewall configured"
else
    echo "⚠ UFW not found, configure firewall manually"
fi

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Your server IP: $SERVER_IP"
echo "Nginx site name: mymemory"
echo ""
echo "Next steps:"
echo "1. Collect static files (if not done):"
echo "   cd $PROJECT_DIR/myMemory"
echo "   source ../venv/bin/activate"
echo "   python manage.py collectstatic --noinput"
echo ""
echo "2. Set permissions:"
echo "   chown -R root:www-data $PROJECT_DIR/myMemory"
echo "   chmod -R 755 $PROJECT_DIR/myMemory"
echo "   chmod -R 775 $PROJECT_DIR/myMemory/memories/media"
echo ""
echo "4. Test your application:"
echo "   Visit: http://$SERVER_IP"
echo ""
echo "5. Check services:"
echo "   systemctl status memory-slideshow"
echo "   systemctl status nginx"
echo ""
echo "For troubleshooting, see: SETUP_NGINX_GUNICORN.md"

