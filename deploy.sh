#!/bin/sh

# Pulls any updates from the remote repository.
git pull

# Uses a virtual environment if it exists.
if [ -f ".venv/bin/activate" ]; then
	source ".venv/bin/activate"
fi

# Updates Python dependencies.
yes | pip install -r "requirements.txt"

# Checks for a .env file.
if [ ! -f ".env" ]; then
	echo "Please create a .env file with a TOKEN variable."
	exit 1
fi

# Creates the database if it doesn't already exist.
if [ ! -f "automoji.db" ]; then
	touch "automoji.db"
fi

# Creates the log directory if they don't already exist.
if [ ! -d "logs" ]; then
	mkdir "logs"
fi

# Runs the program.
python3.10 "src/main.py" > "logs/nohup.log" 2>&1 &
echo $! > "logs/pid.log"
