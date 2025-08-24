#!/bin/bash
# MLX Fine-Tuning Toolkit - Installation Script

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_warning "MLX is optimized for macOS"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found. Please install Python 3.9+"
        return 1
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"; then
        log_error "Python 3.9+ required. Found: $python_version"
        return 1
    fi
    
    log_success "System requirements check passed"
    return 0
}

# Install MLX Fine-Tuning Toolkit
install_toolkit() {
    log_info "Installing MLX Fine-Tuning Toolkit..."
    
    # Install in development mode
    pip3 install -e .
    
    log_success "Installation completed"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    if python3 cli/main.py --version > /dev/null 2>&1; then
        log_success "Installation verified successfully"
        
        # Run system check
        log_info "Running system diagnostics..."
        python3 cli/main.py doctor
    else
        log_error "Installation verification failed"
        return 1
    fi
}

# Main installation process
main() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║            MLX Fine-Tuning Toolkit - Installer              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo
    
    # Check requirements
    if ! check_requirements; then
        log_error "System requirements not met"
        exit 1
    fi
    
    # Install toolkit
    if ! install_toolkit; then
        log_error "Installation failed"
        exit 1
    fi
    
    # Verify installation
    if ! verify_installation; then
        log_error "Installation verification failed"
        exit 1
    fi
    
    echo
    log_success "🎉 MLX Fine-Tuning Toolkit installed successfully!"
    echo
    echo "Next steps:"
    echo "1. Download a model: python3 cli/main.py download qwen2.5-7b-instruct"
    echo "2. Prepare your training data (JSONL format)"
    echo "3. Start training: python3 cli/main.py train --data your_data.jsonl"
    echo
    echo "For more help: python3 cli/main.py --help"
}

# Run main function
main "$@"