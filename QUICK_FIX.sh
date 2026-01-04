#!/bin/bash
# Quick fix script - tries common fixes

set -e

echo "=== Quick Fix for Django App ==="
echo ""

# Fix 1: Restart Gunicorn
echo "[1/5] Restarting Gunicorn service..."
systemctl restart memory-slideshow
sleep 2
systemctl status memory-slideshow --no-pager -l | head -15
echo ""

# Fix 2: Fix socket permissions
echo "[2/5] Fixing socket permissions..."
touch /run/memory-slideshow.sock 2>/dev/null || true
chown root:www-data /run/memory-slideshow.sock
chmod 660 /run/memory-slideshow.sock
ls -la /run/memory-slideshow.sock
echo ""

# Fix 3: Collect static files
echo "[3/5] Collecting static files..."
cd /root/memory_2/myMemory
source ../venv/bin/activate
python manage.py collectstatic --noinput 2>&1 | tail -5
echo ""

# Fix 4: Run migrations
echo "[4/5] Running migrations..."
python manage.py migrate --noinput 2>&1 | tail -5
echo ""

# Fix 5: Fix file permissions
echo "[5/5] Fixing file permissions..."
chown -R root:www-data /root/memory_2/myMemory
chmod -R 755 /root/memory_2/myMemory
chmod -R 775 /root/memory_2/myMemory/memories/media 2>/dev/null || true
echo "✓ Permissions fixed"
echo ""

# Restart services
echo "Restarting services..."
systemctl restart memory-slideshow
systemctl restart nginx
echo ""

echo "=== Fix Complete ==="
echo ""
echo "Check service status:"
echo "  systemctl status memory-slideshow"
echo "  systemctl status nginx"
echo ""
echo "View logs:"
echo "  journalctl -u memory-slideshow -f"
echo "  tail -f /var/log/nginx/error.log"

