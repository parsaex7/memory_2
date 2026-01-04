#!/bin/bash
# Fix socket file issue

echo "=== Fixing Socket File Issue ==="
echo ""

# Stop the service
echo "[1/4] Stopping Gunicorn service..."
systemctl stop memory-slideshow

# Remove the socket file if it exists (as regular file)
echo "[2/4] Removing existing socket file..."
rm -f /run/memory-slideshow.sock
echo "✓ Socket file removed"

# Create directory if needed
echo "[3/4] Ensuring /run directory exists..."
mkdir -p /run
echo "✓ Directory ready"

# Start the service (Gunicorn will create the socket)
echo "[4/4] Starting Gunicorn service..."
systemctl start memory-slideshow
sleep 3

# Check status
echo ""
echo "Checking service status..."
systemctl status memory-slideshow --no-pager -l | head -20

echo ""
echo "Checking socket file..."
if [ -S /run/memory-slideshow.sock ]; then
    echo "✓ Socket file created successfully!"
    ls -la /run/memory-slideshow.sock
else
    echo "✗ Socket file still not created. Check logs:"
    echo "  journalctl -u memory-slideshow -n 30"
fi

