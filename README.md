 Basement Freezer Inventory Web App

This is a simple web application for managing your basement freezer inventory using a SQLite database. The app provides a user-friendly web interface for viewing, adding, editing, and deleting items.

## Features
- View all inventory items in a table
- Add new items with date picker and amount spinner
- Edit and delete existing items
- Responsive web interface (Bootstrap)
- Accessible from any device on your local network

## Requirements
- Python 3.7+
- Flask
- SQLite3 (included with Python)

## Setup

1. **Clone or copy the files to your computer.**
2. **Install dependencies:**
   ```sh
   pip install flask
   ```
3. **Ensure you have a `food.db` SQLite database in the same directory.**
   - You can use the provided scripts (e.g., `000-create-db.py`, `001-create-table.py`) to create the database and table if needed.

## Running the App

### For Local Use (on your computer only)
```sh
python food_webapp.py
```
- Open your browser and go to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### For Network Use (access from other devices)
1. **Find your computer's local IP address:**
   - Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux) and look for your IPv4 address (e.g., `192.168.86.65`).
2. **Run Flask on all interfaces:**
   ```sh
   python food_webapp.py
   ```
   Or edit the last line of `food_webapp.py` to:
   ```python
   app.run(debug=True, host='0.0.0.0')
   ```
3. **On another device (phone, tablet, etc.) on the same WiFi/network, open a browser and go to:**
   ```
   http://<your-ip>:5000/
   ```
   Example: [http://192.168.86.65:5000/](http://192.168.86.65:5000/)

## Notes
- This app is for personal/local use. Do not expose it to the public internet without proper security.
- Make sure your firewall allows connections to port 5000 if using on a network.
