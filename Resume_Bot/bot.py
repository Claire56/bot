from flask import Flask, render_template, request
from newspaper import Article
import random, string, warnings, nltk, numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
warnings.filterwarnings('ignore')

app = Flask(__name__)




# nltk.download('punkt', quiet = True)
nltk.download('punkt')

article = Article('https://abcnews.go.com/International/wireStory/ugandas-bobi-wine-arrested-protesting-capital-76461367')
article.download()
article.parse()
article.nlp()
corpus= article.text

#TOKENIZATION
text = corpus
sentence_list = nltk.sent_tokenize(text)# get  list of sentences 
#print(sentence_list)
#print(len(sentence_list))

def index_sort(list_var):
    n = len(list_var)
    list_index = list(range(0,n))
    x = list_var
    for i in range(n):
        for j in range(n):
            if x[list_index[i]]> x [list_index[j]]:
                #swap
                [list_index[j]],[list_index[i]] = [list_index[i]],[list_index[j]]


    return list_index

# greeting function 
def  greet_response(text):
    text = text.lower()
    #bot greeting response
    bot_greet =  ['hi', 'Ensula','wassup', 'otyanno','hello', 'Holla', 'hey', 'Warrup', 'merhaba']
    #user greeting response
    user_greet =  ['hi', 'wassup', 'hello', 'Holla', 'hey', 'merhaba'] 

    for word in text.split():
        if word in user_greet:
            return random.choice(bot_greet)

#bot response 
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_resp = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores= cosine_similarity(cm[-1],cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)

    index = index[1:]# only from 1
    response_flag =0
    #bring only top two sentences
    j =0 
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
          bot_resp = bot_resp + ' '+ sentence_list[index[i]]
          response_flag =1
          j+=1
        if j>2:
            break
    if response_flag ==0:
        bot_resp = bot_resp+ " "+ "Apologies , I dont have an answer for that."
    sentence_list.remove(user_input)

    return bot_resp


# with open('file.txt','r') as file:
#     conversation = file.read()

# bot = ChatBot(" ChatBot")
# trainer = ListTrainer(bot)
# trainer.train(conversation)

exit_list =['bye', 'exit', 'welaba', 'later', 'end']


# while(True):
  
#     user_input = input()
#     if user_input.lower() in exit_list:
#         print(" ChatBot: See you later ")
#         break
#     else:
#         if greet_response(user_input) != None:
#             print("ChatBot:"+ greet_response(user_input))
#         else:
#             print("ChatBot :"+ bot_response(user_input))

@app.route("/")
def home():
	return render_template("bot.html")

@app.route("/get")
def get_bot_response():
    exit_list =['bye', 'exit', 'welaba', 'later', 'end']

    user_input = request.args.get('msg')
    if user_input.lower() in exit_list:
        return " ChatBot: See you later "
        
    else:
        if greet_response(user_input) != None:
            return "ChatBot:"+ greet_response(user_input)
        else:
            return "ChatBot :"+ bot_response(user_input)


if __name__ == "__main__":
	app.run()
