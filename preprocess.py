import pandas as pd
import difflib
from konlpy.tag import Mecab

def read_melon_data(file_path):
    # Read the Melon data from a CSV file
    return pd.read_csv(file_path)

def read_music_dict(file_path):
    # Read the music dictionary from a CSV file
    return pd.read_csv(file_path)

def calculate_similarity(answer_string, input_string):
    # Calculate the similarity ratio between two strings
    answer_bytes = bytes(answer_string, 'utf-8')
    input_bytes = bytes(input_string, 'utf-8')
    answer_bytes_list = list(answer_bytes)
    input_bytes_list = list(input_bytes)
    
    sm = difflib.SequenceMatcher(None, answer_bytes_list, input_bytes_list)
    similar = sm.ratio()
    
    return similar

def tokenize_input_string(input_string):
    # Tokenize the input string using Mecab
    mecab = Mecab()
    tokens = mecab.morphs(input_string)
    return ' '.join(tokens)

if __name__ == "__main__":
    melon = read_melon_data('./static/data/melondata_edited.csv')

    musicdict = read_music_dict('./static/data/musicdict.csv')
    
    answer_strings = melon['words'].astype(str)
    titles = melon['title']
    singers = melon['singer']
    
    input_string = "시티팝 노래"
    
    # Remove '음악' or '노래' from the input_string
    input_string = input_string.replace('음악', '').replace('노래', '')
    
    tokenized_input = tokenize_input_string(input_string)
    
    # Identify singers in the input_string with partial matching
    singer_names_in_input = [singer for singer in singers if singer in input_string]
    
    if singer_names_in_input:
        # Filter and print results matching the singer's name
        singer_outputs = [(answer, title, singer, calculate_similarity(answer, tokenized_input)) for answer, title, singer in zip(answer_strings, titles, singers) if singer in singer_names_in_input]
        # Set a similarity threshold (adjust this value as needed)
        similarity_threshold = 0.01
        # Keep track of unique answers
        printed_answers = set()
        for answer, title, singer, similarity in sorted(singer_outputs, key=lambda x: x[3], reverse=True):
            if similarity > similarity_threshold and answer not in printed_answers:
                print(f"Title: {title}, Singer: {singer}, Similarity: {similarity}")
                printed_answers.add(answer)
                if len(printed_answers) >= 3:
                    break
        if not printed_answers:
            print("No similar answers found above the similarity threshold for the identified singer.")
    else:
        # Apply the previous rule when no singer's name is found
        # Set a similarity threshold (adjust this value as needed)
        similarity_threshold = 0.1
        # Keep track of unique answers
        printed_answers = set()
        similarities = [(answer, title, singer, calculate_similarity(answer, tokenized_input)) for answer, title, singer in zip(answer_strings, titles, singers)]
        for answer, title, singer, similarity in sorted(similarities, key=lambda x: x[3], reverse=True):
            if similarity > similarity_threshold and answer not in printed_answers:
                print(f"Title: {title}, Singer: {singer}, Similarity: {similarity}")
                printed_answers.add(answer)
                if len(printed_answers) >= 3:
                    break
        if not printed_answers:
            print("No similar answers found above the similarity threshold.")
