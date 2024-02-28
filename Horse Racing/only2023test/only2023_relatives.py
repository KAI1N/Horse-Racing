import pandas as pd
import fasttext
import gensim
import re

def remove_english_parentheses(s):
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'[A-Za-z\s]', '', s)
    s = re.sub(r"'", '', s)
    return s

df=pd.read_csv('horse_relative_data_2023_to_2023.csv')
df_filtered = df[['name', 'father', 'mother', 'grand_father_1', 'grand_father_2', 'grand_mother_1', 'grand_mother_2']]
for column in df_filtered.columns.tolist():
  df_filtered[column] = df_filtered[column].apply(remove_english_parentheses)
  
df_filtered['combined_text'] = df_filtered.apply(lambda x: ' '.join(x.dropna()), axis=1)

df_filtered['combined_text'].to_csv('fasttext_input.txt', index=False, header=False)
model = fasttext.train_unsupervised('fasttext_input.txt', model='skipgram')
model.save_model('model.bin')
model.save_model('model.vec')

model=gensim.models.KeyedVectors.load_word2vec_format('model.vec',binary=False)

# Example: Get the vector for a word
vector = model.get_word_vector("スピードパンサー")
print(vector)