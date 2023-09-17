from transformers import pipeline
import os

# Set the cache path
os.environ['TRANSFORMERS_CACHE'] = 'D:\\Programs'



# ANSWER QUESTIONS FROM CONTEXT
classifier = pipeline("question-answering")



output = classifier(
    question= "What is my occupation?",
    context = "My name is Affan and I am a software developer."
)



print( output )


# {'score': 0.9253730773925781, 'start': 28, 'end': 46, 'answer': 'software developer'}
