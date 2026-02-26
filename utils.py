from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path): 
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
def clean_text(text):
    # convert to lowercase
    text = text.lower()

    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # split into words
    words = text.split()

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    cleaned_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(cleaned_words)
from sklearn.feature_extraction.text import TfidfVectorizer
def vectorize_text(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    return vectors
from sklearn.metrics.pairwise import cosine_similarity
def calculate_match_score(vectors):
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0] * 100
def interpret_score(score):
    if score >= 70:
        return "Strong Match ✅"
    elif score >= 50:
        return "Moderate Match ⚠️"
    else:
        return "Weak Match ❌"
