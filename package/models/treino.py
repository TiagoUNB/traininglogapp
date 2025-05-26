class Treino:
    def __init__(self, name: str, exercises=None): 
        self.name = name
        if exercises is None:
            self.exercises = []
        else:
            self.exercises = exercises
       
