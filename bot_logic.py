import json
import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class SituationalBot:
    def __init__(self, data_path):
        with open(data_path, 'r') as f:
            self.data = json.load(f)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        if 'not' in self.stop_words:
            self.stop_words.remove('not')

    def nlp_clean(self, text):
        text = re.sub(r'[^\w\s]', '', text.lower().strip())
        tokens = word_tokenize(text)
        
        clean_tokens = []
        for w in tokens:
            if w not in self.stop_words:
                lemma = self.lemmatizer.lemmatize(w, pos='n') 
                lemma = self.lemmatizer.lemmatize(lemma, pos='v')
                clean_tokens.append(lemma)
        return clean_tokens

    def get_response(self, user_input):
        user_tokens = self.nlp_clean(user_input)

        for intent in self.data['intents']:
            if any(p in user_input.lower() for p in intent['patterns']):
                if intent['tag'] == 'exit': 
                    return random.choice(intent['responses']), True
                return random.choice(intent['responses']), False

        for item in self.data['knowledge_base']:
            q_tokens = self.nlp_clean(item['question'])
            
            if ('not' in user_tokens) != ('not' in q_tokens):
                continue

            matches = [w for w in q_tokens if w in user_tokens]
            
            if len(q_tokens) > 0:
                score = len(matches) / len(q_tokens)
                if score >= 0.8: 
                    return item['response'], False

        return self.data['bot_config']['fallback_message'], False