from py2neo import authenticate, ServiceRoot, Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

if os.environ.get("N4J_HOST") and os.environ.get("N4J_USER") and os.environ.get("N4J_PASS"):
    authenticate(os.environ.get("N4J_HOST"), os.environ.get("N4J_USER"), os.environ.get("N4J_PASS"))
else:
    print "Credentials not declared"

graphenedb_url = os.environ.get("GRAPHENEDB_URL")
graph = ServiceRoot(graphenedb_url).graph

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')

def get_todays_recent_posts():
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())

class User:
    def __init__(self, username):
        self.username = username
    
    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user
    
    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False
    
    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        user = self.find()
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in set(tags):
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)
    
    def get_recent_posts(self):
        query = """
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        """

        return graph.cypher.execute(query, username=self.username)