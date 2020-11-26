from joblib import dump, load
import joblib
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer


def predictOutput(textData):
    classifier = load('sentimentClassifier.joblib')
    corpus = joblib.load('Corpus.joblib')
    cv = CountVectorizer(max_features = 1500)
    cv.fit_transform(corpus).toarray()


    try:
        to_predict = textData
        
        new_review = to_predict
        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        
        
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_corpus = [new_review]
        new_X_test = cv.transform(new_corpus).toarray()
        new_y_pred = classifier.predict(new_X_test)
        #my_logger.error(data)
        #return {"prediction": 1}
        if(new_y_pred == 1):
            result = 'Positive'
        else:
            result = 'Negative'
            
        return result
    except:
        my_logger.error("Something went wrong!")
        return "error"