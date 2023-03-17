import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = re.sub(r"[\n\r]+", "\n", text)  # Remove duplicate line breaks
    text = re.sub(r"[^a-zA-Z0-9\s_.,!?:;@#$%^&*()+\-=[\]{}|\\<>`~'\"/]+", "", text)  # Remove unwanted characters
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = text.lower()  # Convert text to lowercase

    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = " ".join(words)

    return text.strip()

def process_input_file(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()

    cleaned_text = preprocess_text(input_text)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(cleaned_text)

if __name__ == "__main__":
    input_file_path = input("Enter input file path: ")
    output_file_path = input("Enter output file path: ")

    process_input_file(input_file_path, output_file_path)
