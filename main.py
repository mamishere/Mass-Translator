# Importing Relevant Libraries

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Defining Urls

cam_url = "https://dictionary.cambridge.org/dictionary/english/"
fd_url = "https://fastdic.com/word/"
trs_url = "https://www.thesaurus.com/browse/"

# Opening File of Words

file = open("words_list.txt", "r")

# Words List Preprocessing

words = []

for word in file:
    word = word[:-1]
    words.append(word.lower())
    
# Defining a Pattern to Find Synonyms in Thesaurus

exp = re.compile("^e1ccqdb60.*")

# Creating a List of All Items

def_lst = []
ex_lst = []
ws_lst = []

# Scraping Websites

for word in words:
    
    """""
    In this loop we use each word as an input and extract all data of it.
    
        First Step:
            * Adding word to the words list.
            * Creating 3 urls of 3 websites for word.
        
        Second Step:
            * Getting and parsing data from thesaurus website.
            * Creating an empty string for storing word's synonyms.
            * Finding a list of the most important synonyms of the word.
            * Adding synonms to the empty string we've created before.
            * Adding the synonyms string to the defenitions list.
            
        Third Step:
            * Getting and parsing data from fastdic website.
            * Creating an empty list for storing word's synonyms.
            * Adding synonms to the empty list we've created before.
            * Changing the list of synonims to a string variable.

        Forth Step:
            * Getting and parsing data from cambridge dictionary website.
            * Creating an integer varibale with the initial value of 0 for storing numbers of examples founded for the word.
            * Storing each block's data (one defenition and one or more examples) in two variables named defenition and examples.
            * Adding defenition and examples variables defined before to the main defenition and example list.
            
    """
    
    # First Step
    
    ws_lst += [word]
        
    url1 = trs_url + word
    url2 = fd_url + word
    url3 = cam_url + word
    
    # Second Step
    
    results1 = requests.get(url1, headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    doc1 = BeautifulSoup(results1.text, "html.parser")
    
    syns_str = ""
    
    grid = doc1.find_all(class_ = exp)
    
    syns = grid[0].find_all(class_ = "css-1kg1yv8 eh475bn0")

    for syn in syns:
        
        if syns.index(syn) != len(syns) - 1:
            syns_str += syn.text + "| "
        else:
            syns_str += syn.text
    
    def_lst += [syns_str]    
    
    # Third Step
    
    results2 = requests.get(url2, headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    doc2 = BeautifulSoup(results2.text, "html.parser")
    
    farsi_meanings_lst = []
    farsi_meanings_str = ""

    farsi_meanings = doc2.find("ul", attrs = {"class" : "result"})
    farsi_meanings = farsi_meanings.find_all("span", class_ = "")

    for farsi_meaning in farsi_meanings:
        
        farsi_meaning = farsi_meaning.text
            
        farsi_meaning = farsi_meaning.replace("\n", "")
        farsi_meaning = farsi_meaning.replace("\t", "")
        farsi_meaning = farsi_meaning.replace("\u200c", " ")
        
        farsi_meanings_lst.append(farsi_meaning)
    
    for farsi_meaning in farsi_meanings_lst:
        
        if farsi_meanings_lst.index(farsi_meaning) != (len(farsi_meanings_lst) - 1):
            farsi_meaning += " | "
            
        farsi_meanings_str = farsi_meanings_str + farsi_meaning
        
    ex_lst += [farsi_meanings_str]
        
    # Forth Step
    
    results3 = requests.get(url3, headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    doc3 = BeautifulSoup(results3.text, "html.parser")
    
    ex_num = 0
        
    blocks = doc3.find_all(class_ = "def-block ddef_block")
    
    for block in blocks:
        
        defenition = ""
        examples = []
        
        defenition = ((block.find(class_ = "def ddef_d db")).text)[:-2]
        examples = [example.text for example in block.find_all(class_ = "eg deg")]
        
        if len(examples) == 0:
            examples = [""]
                    
        def_lst = def_lst + [defenition] + (len(examples) - 1) * [""]
        ex_lst += examples
        ex_num += len(examples)
    
    ws_lst += (ex_num + 1) * [""]
    def_lst += [""]
    ex_lst += [""]
    
# Creating a Pandas Dataframe
    
index = []
index_counter = 1

for i in ws_lst:
    if len(i) > 0:
        index += [index_counter]
        index_counter += 1
    else:
        index += [""]

df = pd.DataFrame(list(zip(ws_lst, def_lst, ex_lst)), columns =["Word", "Def.", "Exp."])
df.index = index

# Saving The Dataframe File as an Excel File

df.to_excel("Dictionary.xlsx")