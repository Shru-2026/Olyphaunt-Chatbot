# chatbot_backend.py
import fitz  # PyMuPDF
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk

# Ensure required NLTK packages are downloaded
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Function to extract Q&A pairs from a PDF
def extract_pdf_text(pdf_path):
    with fitz.open(pdf_path) as reader:
        text = "".join([reader[page_num].get_text("text") for page_num in range(len(reader))])
    qa_pairs = []
    lines = text.split('\n')
    question, answer = None, None
    for line in lines:
        if line.strip().startswith("Q:"):
            if question and answer:
                qa_pairs.append((question, answer.strip()))
            question = line[2:].strip()
            answer = ""
        elif line.strip().startswith("A:"):
            answer = line[2:].strip()
        elif question:
            answer += f" {line.strip()}"
    if question and answer:
        qa_pairs.append((question, answer.strip()))
    return qa_pairs

# Chatbot class
class XYZConsultingChatbot:
    def __init__(self, qa_pairs):
        self.qa_pairs = qa_pairs
        self.questions = [qa[0].lower() for qa in qa_pairs]
        self.answers = [qa[1] for qa in qa_pairs]
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def respond(self, user_query):
        query_vector = self.vectorizer.transform([user_query.lower()])
        similarities = cosine_similarity(query_vector, self.question_vectors)
        max_similarity_idx = np.argmax(similarities)
        if similarities[0, max_similarity_idx] > 0.4:
            return self.answers[max_similarity_idx]
        return "I'm sorry, I couldn't find an answer. Please contact us for more details."

# Function to initialize the chatbot with PDF input
def initialize_chatbot(pdf_path):
    qa_pairs = extract_pdf_text(pdf_path)
    return XYZConsultingChatbot(qa_pairs)
