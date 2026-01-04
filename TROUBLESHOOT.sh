#!/bin/bash
# Troubleshooting script for Django app not running
# Run this to diagnose issues

echo "=== Memory Slideshow Troubleshooting ==="
echo ""

# Check Gunicorn service status
echo "[1] Checking Gunicorn service status..."
systemctl status memory-slideshow --no-pager -l || echo "Service not running!"
echo ""

# Check if socket file exists
echo "[2] Checking socket file..."
if [ -S /run/memory-slideshow.sock ]; then
    echo "✓ Socket file exists"
    ls -la /run/memory-slideshow.sock
else
    echo "✗ Socket file NOT found!"
fi
echo ""

# Check Gunicorn logs
echo "[3] Recent Gunicorn logs (last 30 lines):"
journalctl -u memory-slideshow -n 30 --no-pager
echo ""

# Check Nginx status
echo "[4] Checking Nginx status..."
systemctl status nginx --no-pager -l | head -20
echo ""

# Check Nginx error logs
echo "[5] Recent Nginx error logs:"
tail -20 /var/log/nginx/error.log 2>/dev/null || echo "No error log found"
echo ""

# Test Django settings
echo "[6] Testing Django configuration..."
cd /root/memory_2/myMemory
source ../venv/bin/activate
python manage.py check --deploy 2>&1 | head -30
echo ""

# Test if we can import Django
echo "[7] Testing Django import..."
python -c "import django; print(f'Django version: {django.get_version()}')" 2>&1
echo ""

# Check if manage.py works
echo "[8] Testing manage.py..."
python manage.py check 2>&1 | head -20
echo ""

# Test Gunicorn manually
echo "[9] Testing Gunicorn manually (will timeout in 5 seconds)..."
timeout 5 /root/memory_2/venv/bin/gunicorn --bind 127.0.0.1:8001 --check-config myMemory.wsgi:application 2>&1 || echo "Gunicorn test completed"
echo ""

echo "=== Troubleshooting Complete ==="
echo ""
echo "Common issues and fixes:"
echo "1. If socket file doesn't exist: sudo systemctl restart memory-slideshow"
echo "2. If service failed: Check logs above for errors"
echo "3. If Django errors: Check database migrations and settings"
echo "4. If 502 Bad Gateway: Check socket permissions (should be root:www-data)"
echo "5. If static files not found: Run 'python manage.py collectstatic --noinput'"

