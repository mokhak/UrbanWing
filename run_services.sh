#!/bin/bash

VENV_ACTIVATE="/Users/kirat.mokha/Documents/School Work/Cloud Computing/Final Project/env/bin/activate"

FLASK_APP_1="/Users/kirat.mokha/Documents/School Work/Cloud Computing/Final Project/app_services/auth.py"
FLASK_APP_2="/Users/kirat.mokha/Documents/School Work/Cloud Computing/Final Project/app_services/camera.py"
FLASK_APP_3="/Users/kirat.mokha/Documents/School Work/Cloud Computing/Final Project/app_services/classification.py"

# Function to open a new terminal window and run a command
run_in_new_terminal() {
  local script_path="$1"
  osascript <<EOF
tell application "Terminal"
    do script "source \"$VENV_ACTIVATE\" && cd \"$(dirname "$script_path")\" && python3 \"$(basename "$script_path")\""
end tell
EOF
}

# Run the Flask apps
run_in_new_terminal "$FLASK_APP_1"
run_in_new_terminal "$FLASK_APP_2"
run_in_new_terminal "$FLASK_APP_3"