
class DinoTree:
    def __init__(self, question,list):
        self.question = question
        self.list = list
        self.next_question = []
    
    def add_next_question(self,question):
        self.next_question.append(question)