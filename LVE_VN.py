import csv
import spacy

nlp = spacy.load("en_core_web_lg")

def find_verb_dobj_concordances(csv_file, columns_indices, output_file):
    concordances = []

    with open(csv_file, 'r', encoding='utf-8') as file, open(output_file, 'w', newline='', encoding='UTF-8') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Lemma', 'Noun', 'Context', 'Writing ID', 'L1', 'CEFR', 'Topic'])
        reader = csv.reader(file)
        for row in reader:
            if len(row) > max(columns_indices):
                text = row[23]
                print("Text from CSV row:", text)
                doc = nlp(text)
                for i, token in enumerate(doc[:-1]):
                    if token.pos_ == 'VERB' and i+1 < len(doc) and (doc[i+1].pos_ == 'NOUN' or doc[i+1].pos_ == 'PRON' or doc[i+1].pos_ == 'PROPN') and doc[i+1].dep_ == 'dobj':
                        start = max(0, i - 5)
                        end = min(len(doc), i + 6)
                        context = ' '.join([token.text for token in doc[start:end]])
                        concordances.append((context, [row[i] for i in columns_indices]))
                        lemma = token.lemma_
                        noun_lemma = doc[i+1].lemma_
                        writer.writerow([lemma, noun_lemma, context] + [row[i] for i in columns_indices])
                        print("Concordance: ", context)
                        print("token: ", token)
                        print("lemma: ", lemma)
                        print("noun", noun_lemma)
                        print("Row data:", [row[i] for i in columns_indices])

    return concordances

def write_to_csv(concordances, output_file):
    with open(output_file, 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Lemma', 'Noun', 'Context', 'Writing ID', 'L1', 'CEFR', 'Topic'])
        for context, rows in concordances:
            writer.writerow([context] + rows)
   # file_out.write(file + tab + token.text + tab + token.lemma_ + tab + token.pos_ + tab + spacy.explain(token.pos_) +
   #                tab + token.tag_ + tab + spacy.explain(token.tag_) + '\n')

csv_file = 'efcamdat.csv'
columns_indices = [0, 4, 5, 14]  # Indices of columns to extract: writing_id, L1, cefr, topic
output_file = '2verb_dobj_concordances_output.csv'
result = find_verb_dobj_concordances(csv_file, columns_indices, output_file)


# write_to_csv(result, output_file)

print("Verb-Direct Object Concordances written to:", output_file)
