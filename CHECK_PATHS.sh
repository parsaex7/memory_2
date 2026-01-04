#!/bin/bash
# Check file paths and structure

echo "=== Checking File Paths ==="
echo ""

echo "Current directory: $(pwd)"
echo ""

echo "Checking if manage.py exists..."
if [ -f "/root/memory_2/myMemory/manage.py" ]; then
    echo "✓ manage.py found at /root/memory_2/myMemory/manage.py"
else
    echo "✗ manage.py NOT found at /root/memory_2/myMemory/manage.py"
    echo ""
    echo "Searching for manage.py..."
    find /root/memory_2 -name "manage.py" 2>/dev/null
fi

echo ""
echo "Checking directory structure..."
ls -la /root/memory_2/ 2>/dev/null | head -20

echo ""
echo "Checking myMemory directory..."
if [ -d "/root/memory_2/myMemory" ]; then
    ls -la /root/memory_2/myMemory/ 2>/dev/null | head -20
else
    echo "✗ /root/memory_2/myMemory directory not found!"
fi

echo ""
echo "Checking service file paths..."
cat /etc/systemd/system/memory-slideshow.service | grep -E "WorkingDirectory|ExecStart|Environment"

