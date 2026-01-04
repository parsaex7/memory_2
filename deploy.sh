#!/bin/bash

# Deployment script for Memory Slideshow
# This script helps set up the application on a server

set -e  # Exit on error

echo "========================================="
echo "Memory Slideshow - Deployment Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip3 found${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo -e "${YELLOW}Creating .env file from env.example...${NC}"
        cp env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo -e "${YELLOW}⚠ Please edit .env file and set your SECRET_KEY and other variables${NC}"
    else
        echo -e "${YELLOW}⚠ .env.example not found, creating basic .env file...${NC}"
        echo "SECRET_KEY=$(python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
        echo "DEBUG=False" >> .env
        echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
        echo -e "${GREEN}✓ Basic .env file created${NC}"
    fi
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations completed${NC}"

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

# Create media directory if it doesn't exist
if [ ! -d "memories/media" ]; then
    echo -e "${YELLOW}Creating media directory...${NC}"
    mkdir -p memories/media
    echo -e "${GREEN}✓ Media directory created${NC}"
fi

# Set permissions for media directory
echo -e "${YELLOW}Setting permissions...${NC}"
chmod -R 755 memories/media/
echo -e "${GREEN}✓ Permissions set${NC}"

echo ""
echo "========================================="
echo -e "${GREEN}Deployment setup completed!${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and configure your settings"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the server: python manage.py runserver"
echo ""
echo "For production deployment, see README.md"
echo ""

