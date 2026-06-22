#!/bin/bash

# GalaksiAksaraBot Setup & Testing Script
# Usage: bash setup.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌙 GalaksiAksaraBot Setup & Testing${NC}\n"

# Function: Print colored messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function: Check Python installation
check_python() {
    print_info "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        VERSION=$(python3 --version)
        print_status "Python found: $VERSION"
        return 0
    else
        print_error "Python3 not found. Please install Python 3.9+"
        return 1
    fi
}

# Function: Setup virtual environment
setup_venv() {
    print_info "Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        return 0
    fi
    
    python3 -m venv venv
    source venv/bin/activate
    print_status "Virtual environment created and activated"
}

# Function: Install dependencies
install_deps() {
    print_info "Installing dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        return 1
    fi
    
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    print_status "Dependencies installed"
}

# Function: Setup environment variables
setup_env() {
    print_info "Setting up environment variables..."
    
    if [ -f ".env" ]; then
        print_warning ".env already exists"
        return 0
    fi
    
    if [ ! -f ".env.example" ]; then
        print_error ".env.example not found"
        return 1
    fi
    
    cp .env.example .env
    print_status ".env created from .env.example"
    
    print_info "Please edit .env with your configuration:"
    print_warning "  - TELEGRAM_BOT_TOKEN"
    print_warning "  - TELEGRAM_CHANNEL_ID"
    print_warning "  - GEMINI_API_KEY"
    print_warning "  - GEMINI_MODEL (optional)"
}

# Function: Check Gemini configuration
check_gemini() {
    print_info "Checking Gemini configuration..."

    if [ -n "$GEMINI_API_KEY" ]; then
        print_status "GEMINI_API_KEY found"
        print_info "Model: ${GEMINI_MODEL:-gemini-2.0-flash}"
        return 0
    else
        print_warning "GEMINI_API_KEY not set"
        print_info "Add it to .env to enable Gemini responses"
        return 1
    fi
}

# Function: Setup database
setup_database() {
    print_info "Initializing database..."
    
    python3 -c "
from db import Database
db = Database()
print('✓ Database initialized')
"
    print_status "Database ready"
}

# Function: Test components
test_components() {
    print_info "Testing components..."
    
    # Test imports
    python3 -c "
import bot
import db
import personality
import ai_engine
import styles
print('✓ All modules imported successfully')
" && print_status "Module imports OK" || (print_error "Module import failed"; return 1)
    
    # Test database
    python3 -c "
from db import Database
db = Database()
db.init_user(999, 'TestUser')
profile = db.get_user_profile(999)
if profile:
    print('✓ Database operations OK')
else:
    print('✗ Database operations failed')
" && print_status "Database operations OK" || (print_error "Database operations failed"; return 1)
    
    # Test AI Engine
    python3 -c "
from ai_engine import AIEngine
ai = AIEngine()
print('✓ AI Engine initialized')
" && print_status "AI Engine OK" || (print_error "AI Engine initialization failed"; return 1)
}

# Function: Run bot
run_bot() {
    print_info "Starting GalaksiAksaraBot..."
    
    if [ ! -f ".env" ]; then
        print_error ".env not found. Run 'bash setup.sh init' first"
        return 1
    fi
    
    source venv/bin/activate 2>/dev/null || true
    python3 bot.py
}

# Function: Docker setup
docker_setup() {
    print_info "Setting up Docker deployment..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not installed"
        return 1
    fi
    
    print_status "Docker and Docker Compose found"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_warning "Creating .env from .env.example"
        cp .env.example .env
    fi
    
    print_info "To start with Docker Compose:"
    echo "    docker-compose up -d"
    print_info "To check logs:"
    echo "    docker-compose logs -f"
    print_info "To stop:"
    echo "    docker-compose down"
}

# Function: Full setup
full_setup() {
    print_info "Running full setup...\n"
    
    check_python || return 1
    setup_venv
    install_deps
    setup_env
    setup_database
    
    print_info "\nTesting Gemini configuration..."
    check_gemini || print_warning "Gemini key not available (will use fallback poems)"
    
    print_info "\nTesting components..."
    test_components
    
    echo ""
    print_status "Setup complete! 🎉"
    echo ""
    print_info "Next steps:"
    echo "  1. Edit .env with your credentials"
    echo "  2. Add GEMINI_API_KEY to enable AI responses"
    echo "  3. Run the bot: bash setup.sh run"
    echo ""
}

# Main command handling
case "${1:-help}" in
    init)
        check_python && setup_venv && install_deps && setup_env && setup_database
        ;;
    check-gemini)
        check_gemini
        ;;
    test)
        test_components
        ;;
    docker)
        docker_setup
        ;;
    run)
        run_bot
        ;;
    full)
        full_setup
        ;;
    help|*)
        echo "Usage: bash setup.sh [command]"
        echo ""
        echo "Commands:"
        echo "  init           - Initialize project (venv, deps, db)"
        echo "  check-gemini   - Check Gemini configuration"
        echo "  test           - Test all components"
        echo "  docker         - Setup Docker deployment"
        echo "  run            - Run the bot"
        echo "  full           - Full setup (init + tests)"
        echo "  help           - Show this help message"
        echo ""
        echo "Quick start:"
        echo "  bash setup.sh full"
        echo "  bash setup.sh run"
        ;;
esac
