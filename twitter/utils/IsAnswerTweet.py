from core.models import Quiz
from twitter.TextSanitize import TextSanitize

def is_answer_tweet(text):
    if text == None:
        return -1
    line = text.split('\n')[0]
    if "問題" in line:
        try:
            pk =int(line.replace("問題",""))
            return pk
        except ValueError:
            return -1
    else:
        return -1

def is_correct_answer(pk,text):
    text = TextSanitize(text)
    quiz = Quiz.objects.get(pk=pk)
    if(text in quiz.answers.split(",")):
        return True
    else:
        return False
