
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. Now run: python3 bot.py"
