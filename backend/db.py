# Very small demo DB: file-based JSON store. Replace with SQLModel/SQLite for production.
import json
import os

STORE_FILE = 'user_store.json'


class SimpleUserDB:
    def __init__(self):
        if os.path.exists(STORE_FILE):
            with open(STORE_FILE, 'r') as f:
                try:
                    self.store = json.load(f)
                except Exception:
                    self.store = {}
        else:
            self.store = {}

    def save(self):
        with open(STORE_FILE, 'w') as f:
            json.dump(self.store, f, indent=2)

    def create_user(self, username, password, email, lat=None, lon=None):
        self.store[username] = {
            'password': password,
            'email': email,
            'known_ips': [],
            'known_devices': [],
            'lat': lat,
            'lon': lon,
            'failed_attempts': 0
        }
        self.save()

    def get_user(self, username):
        return self.store.get(username)

    def increment_failed(self, username):
        if username in self.store:
            self.store[username]['failed_attempts'] = self.store[username].get('failed_attempts', 0) + 1
            self.save()

    def reset_failed(self, username):
        if username in self.store:
            self.store[username]['failed_attempts'] = 0
            self.save()
