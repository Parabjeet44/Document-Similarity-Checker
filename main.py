import string
import os

class DocumentSimilarityChecker:
    def __init__(self):
        self.documents = []
        self.word_frequencies = []
        self.sorted_words = []
        self.file_names = []

    def load_document(self, file_path):
        try:
            if os.path.isdir(file_path):
                print(f"Error: '{file_path}' is a directory, not a file.")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.documents.append(content)
            self.file_names.append(os.path.basename(file_path))
            words = self.preprocess(content)
            freq = self.get_word_frequency(words)
            self.word_frequencies.append(freq)
            self.sorted_words.append(sorted(words))
            return True
        except PermissionError:
            print(f"Error: Permission denied. Unable to read '{file_path}'.")
        except IOError as e:
            print(f"Error reading file '{file_path}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def preprocess(self, content):
        content = content.translate(str.maketrans('', '', string.punctuation))
        return content.lower().split()

    def get_word_frequency(self, words):
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        return freq

    def binary_search(self, arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return True
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def calculate_similarity(self, freq1, freq2, sorted_words1, sorted_words2):
        common_words = 0
        for word in freq1:
            if self.binary_search(sorted_words2, word):
                common_words += min(freq1[word], freq2.get(word, 0))
        
        max_words = max(sum(freq1.values()), sum(freq2.values()))
        return common_words / max_words if max_words > 0 else 0

    def compare_all_documents(self):
        n = len(self.documents)
        for i in range(n):
            for j in range(i+1, n):
                if self.documents[i] == self.documents[j]:
                    print(f"'{self.file_names[i]}' and '{self.file_names[j]}' are exactly identical (100% match).")
                else:
                    similarity = self.calculate_similarity(
                        self.word_frequencies[i], 
                        self.word_frequencies[j],
                        self.sorted_words[i],
                        self.sorted_words[j]
                    )
                    percentage = similarity * 100
                    print(f"Similarity between '{self.file_names[i]}' and '{self.file_names[j]}': {percentage:.2f}%")

def main():
    checker = DocumentSimilarityChecker()

    while True:
        file_path = input("Enter the path to a text file (or 'done' to finish adding files): ").strip()
        if file_path.lower() == 'done':
            break
        
        if os.path.exists(file_path):
            if checker.load_document(file_path):
                print(f"File '{os.path.basename(file_path)}' loaded successfully.")
        else:
            print("File not found. Please enter a valid file path.")

    if len(checker.documents) < 2:
        print("At least two documents are required for comparison.")
    else:
        print("\nComparing documents:")
        checker.compare_all_documents()

if __name__ == "__main__":
    main()