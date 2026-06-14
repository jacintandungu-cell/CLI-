class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def __repr__(self):
        return f"User({self.username}, {self.email})"
