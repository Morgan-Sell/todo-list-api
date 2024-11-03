#!/bin/bash

# Exit on error
set -e

# Ensures the the script always points to the directory in which the script is located
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set Python Path
export PYTHONPATH=$THIS_DIR


# Run application once configuration is setup
function run-app {
    python src/main.py
}


# Load environment variables from .env file
function load-env {
    check-api-key
    echo "Loading environment variables from .env file..."
    export $(grep -v '^\s*#' "$THIS_DIR/.env" | grep -v '^\s*$' | xargs)  # Ignores comment and blank lines
}




# Set up a virtual environment
function setup-venv {
    if [ ! -d "venv" ]; then
        python3.11 -m venv venv
        echo "Virtual environment created."
    fi
    source venv/bin/activate
    echo "Virtual environment activated."
}

# Install dependencies
function install-deps {
    setup-venv
    pip install --upgrade pip
    pip install -r requirements.txt

}

# Run all setup tasks after cloning the repo
function initial-setup {
    echo "Running initial setup..."
    load-env
    setup-venv
    install-deps
    echo "Initial setup completed. You're ready to go!"
}

# Display help/usage information
function help {
    echo "Usage: ./run.sh <task>"
    echo "Tasks:"
    echo "  run-app             Run the application"
    echo "  load-env            Load environment variables from .env"
    echo "  setup-venv          Set up virtual environment"
    echo "  install-deps        Install dependencies"
    echo "  initial-setup       Run the initial setup after cloning"
    echo "  help                Show this help message"
}

# Main script logic for running the desired task
if [ $# -eq 0 ]; then
    help
    exit 0
fi

case "$1" in
    run-app)
        run-app
        ;;
    load-env)
        load-env
        ;;
    setup-venv)
        setup-venv
        ;;
    install-deps)
        install-deps
        ;;
    initial-setup)
        initial-setup
        ;;
    help)
        help
        ;;
    *)
        echo "Invalid task: $1"
        help
        exit 1
        ;;
esac