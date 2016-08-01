from flask_login import (LoginManager, login_required, login_user, 
                         current_user, logout_user, UserMixin)
class User(UserMixin):
    """
    User Class for flask-Login
    """
    def __init__(self, userid, password):
        self.id = userid
        self.password = password
 
    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)
 
    @staticmethod
    def get(userid):
        """
        Static method to search the database and see if userid exists.  If it 
        does exist then return a User Object.  If not then return None as 
        required by Flask-Login. 
        """
        #For this example the USERS database is a list consisting of 
        #(user,hased_password) of users.
        for user in USERS:
            if user[0] == userid:
                return User(user[0], user[1])
        return None