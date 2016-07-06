from passlib.hash import bcrypt
from datetime import datetime
import uuid

class User:
    def verify_password(self, passw):
        return True