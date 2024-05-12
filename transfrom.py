import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download NLTK stopwords corpus
# nltk.download('stopwords')

def preprocess_text(text):
    # Remove HTML tags
    clean_text = re.sub('<.*?>', '', text)
    
    # Remove special characters and punctuation
    clean_text = re.sub(r'[^a-zA-Z\s]', '', clean_text)
    
    # Convert to lowercase
    clean_text = clean_text.lower()
    
    # Tokenization
    tokens = word_tokenize(clean_text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming (Optional)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    
    return ' '.join(stemmed_tokens)  # Join tokens back into a single string

# Read data from CSV file
try:
    data = pd.read_csv('data.csv', sep='|')
except FileNotFoundError:
    print("Error: 'data.csv' file not found.")
    exit()

# Check if 'description' column exists
if 'description' not in data.columns:
    print("Error: 'description' column not found in the CSV file.")
    exit()

# Preprocess text data in the 'description' column
data['cleaned_description'] = data['description'].apply(lambda x: preprocess_text(x) if isinstance(x, str) else "")

# Save cleaned data to a new CSV file
data[['headline', 'link', 'cleaned_description']].to_csv('cleaned_data.csv', index=False)

print("Preprocessing complete. Cleaned data saved to 'cleaned_data.csv'.")
