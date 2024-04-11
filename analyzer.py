from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

class Analyzer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def tokenize_text(self, text):
        words = word_tokenize(text)
        return words
    
    def remove_stop_words(self, tokens):
        filtered_tokens = [token for token in tokens if token.lower() not  in self.stop_words]
        return filtered_tokens
    
    def stem_words(self, tokens):
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens
    
    def lemmatize_words(self, tokens):
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens
    
