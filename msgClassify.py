import json
import re



def contains(a_list, a_sentence):
    for item in a_list:
        
        if item[0] == '*':
            if re.search(item.replace('*', '').replace('d', '\d'), a_sentence):
                return (item)
        else:
            if item.lower() in a_sentence.lower():
                return (item)


#  split text into one or more sentences
def split(text, rows_split_delim=['.', '!', '?']):
    # sentences after the split
    rows_split = []
    # pointer to position within text
    pointer = 0

    
    if 'http' in text.lower():
        return [text]

    # loop through each character in the message text
    for char in text:
        # if character is a sentence delimeter
        if char in rows_split_delim:
            # split out the text from the previous pointer to this delimeter
            sentence = text[pointer:text.index(char, pointer) + 1]
            # remove extra spaces
            sentence = sentence.lstrip().strip()
            rows_split.append(sentence)
            # update the pointer
            pointer = text.index(char, pointer) + 1

    
    sentence = text[pointer:].lstrip().strip()
    rows_split.append(sentence)

    return rows_split



class Classifier(object):
    

    def __init__(self, topics_file):
        
        # load topics and their words
        try:
            self.topics = json.load(open(topics_file))
        except:
            print ('error opening file', topics_file)

    def classify(self, text):
       

        topics_data = {}
        # split out sentences from the text
        sentences = split(text)

        for sentence in sentences:
            # loop through the topics
            for key in self.topics.keys():
                # if the sentence contains any of the words for this topic, add to results
                if contains(self.topics[key], sentence):
                    if key not in topics_data:
                        topics_data[key] = [sentence]
                    else:
                        topics_data[key].append(sentence)

        return topics_data
