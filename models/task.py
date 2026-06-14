class Task:
    def __init__(self, title, due_date, contributors=None):
        self.title = title
        self.due_date = due_date
        self.completed = False
        self.contributors = contributors if contributors else []

    def mark_complete(self):
        self.completed = True

    def __repr__(self):
        return f"Task({self.title}, Completed={self.completed})"
