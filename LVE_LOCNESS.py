import os
import spacy
import csv
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:  # Open the file in binary mode
        raw_data = file.read(10000)  # Read the first 10,000 bytes to guess the encoding
        return chardet.detect(raw_data)['encoding']

nlp = spacy.load("en_core_web_lg")



def find_verb_concordances(input_folder, output_file):
    target_verbs = {'add', 'bring', 'build', 'develop', 'find'}  # Set of target verbs
    concordances = []

    with open(output_file, 'w', newline='', encoding='utf-8') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Lemma', 'Context', 'File'])

        # Loop through all files in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                encoding = detect_encoding(file_path)
                with open(file_path, 'r', encoding='iso-8859-1') as file:
                    text = file.read()
                    doc = nlp(text)
                    for token in doc:
                        if token.pos_ == 'VERB' and token.lemma_ in target_verbs:
                            start = max(0, token.i - 5)
                            end = min(len(doc), token.i + 6)
                            context = ' '.join([t.text for t in doc[start:end]])
                            concordances.append((token.lemma_, context, filename))
                            writer.writerow([token.lemma_, context, filename])
                            print(token)
                            print("Concordance: ", context)

    return concordances

# Specify the folder containing the text files and the output CSV file
input_folder = '/Users/soyeonsim/Desktop/Python_wd/LOCNESS'
output_file = 'concordances_LOCNESS.csv'

# Extract and write verb concordances
result = find_verb_concordances(input_folder, output_file)
print("Verb Concordances written to:", output_file)

