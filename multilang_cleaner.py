# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 11:51:18 2021

@author: joneszc
"""

import re
import codecs
from bs4 import BeautifulSoup

rusStopWords_path = r'C:\Users\joneszc\Documents\Python_Scripts\NLP\stopwords\ru_stopwords.txt'
with codecs.open(rusStopWords_path,'r', encoding='utf-8') as stpwds:
    rusStopWords = [w.lower().strip() for w in stpwds if w.strip()!='']
    
engStopWords_path = r'C:\Users\joneszc\Documents\Python_Scripts\NLP\stopwords\en_stopwords.txt'
with open(engStopWords_path,'r') as stpwds:
    engStopWords = [w.lower().strip() for w in stpwds if w.strip()!='']

class cleanRussText:
    '''Process Russian text with various cleaning tools that focus on lowercasing Russian characters, normalizing whitespace
        and filtering out non-Russian segments'''
    def __init__(self, text):
        text = str(text).strip()
        self.cleanText(text)
        
    def filterLat2Russ(self, string):
        '''Separate English and Russian terms and process both accordingly before re-joining text as cleaned output'''
        latin2Russn = {'A':'А', 'a': 'а', 'B': 'В', 'E': 'Е', 'e': 'е', 'u': 'и', 'K': 'К', 'k': 'к', 'M':'М','m': 'м', 'H': 'Н', 'O': 'О', 'o': 'о', 'n': 'п', 'P': 'Р', 'p': 'р', 'C': 'С', 'c': 'с', 'T': 'Т', 'Y': 'У', 'y': 'у', 'X': 'Х', 'x': 'х'}# 'm': 'т',
        segms = string.split()
        for i,v in enumerate(segms):
            russString=''
            if cleanEngText.is_english(v):
                russString = str(cleanEngText.en_clean_text(v))
                #print("English Converted",v,"to",russString)
            else:
                for letter in v:
                    if letter in latin2Russn.keys():
                        russString+=latin2Russn[letter]
                        #print("Russian Converted",v,"to",russString)
                    else:
                        russString+=letter
                russString = self.ru_clean_text(russString)
            segms[i] = russString
        outstring = ' '.join(segms)
        return outstring
    
    def RU_lower(self, string):
        #ru_lower_dict = {'А': 'а', 'Б': 'б', 'В': 'в', 'Г': 'г', 'Д': 'д', 'Е': 'е', 'Ё': 'ё', 'Ж': 'ж', 'З': 'з', 'И': 'и', 'Й': 'й', 'К': 'к', 'Л': 'л', 'М': 'м', 'Н': 'н', 'О': 'о', 'П': 'п', 'Р': 'р', 'С': 'с', 'Т': 'т', 'У': 'у', 'Ф': 'ф', 'Х': 'х', 'Ц': 'ц', 'Ч': 'ч', 'Ш': 'ш', 'Щ': 'щ', 'Ъ': 'ъ', 'Ы': 'ы', 'Ь': 'ь', 'Э': 'э', 'Ю': 'ю', 'Я': 'я'}
        ru_lower_dict = {'А': 'а', 'Б': 'б', 'В': 'в', 'Г': 'г', 'Д': 'д', 'Е': 'е', 'Ё': 'ё', 'Ж': 'ж', 'З': 'з', 'И': 'и', 'Й': 'й', 'К': 'к', 'Л': 'л', 'М': 'м', 'Н': 'н', 'О': 'о', 'П': 'п', 'Р': 'р', 'С': 'с', 'Т': 'т', 'У': 'у', 'Ф': 'ф', 'Х': 'х', 'Ц': 'ц', 'Ч': 'ч', 'Ш': 'ш', 'Щ': 'щ', 'Ъ': 'ъ', 'Ы': 'ы', 'Ь': 'ь', 'Э': 'э', 'Ю': 'ю', 'Я': 'я', 'Ë': 'ë', 'Ž': 'ž', 'Č': 'č', 'Š': 'š', 'Ŝ': 'ŝ', 'È': 'è', 'Û': 'û', 'Â': 'â'}
        lowerString=''
        for letter in string:
            if letter in ru_lower_dict.keys():
                lowerString+=ru_lower_dict[letter]
            else:
                lowerString+=letter
        return lowerString

    #def normalzLinebreaks(self, string):
        #string = re.sub('[\t\n\r\x0b\x0c]+','\n', string)
        #return string
    def normalzWhitespace(self, string):
        string = re.sub('[#$%&()*\+®,-\./:;<=>?@[\\]—^_`{|}~ʺʹ«„“»]+',' ', string)
        string = re.sub('[ \t\n\r\x0b\x0c]+',' ', string)
        string=re.sub(' +',' ',string)
        return string
    #def ru_isalpha(self, string):
        #if set(string.replace(' ','')).issubset('́́ААаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'):
        #if set(string.replace(' ','')).issubset('́́ААаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсCcТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяËŽČŠŜÈÛÂëžčšŝèûâ'):
            #return True
        #else:
            #return False
    #def normalzNumbs(text):  ## replace all numbers with a common label
        ##text=re.sub('\w*\d\w*','', text) # remove words with digits
        #text=re.sub('\d+','digits_entity', text) # remove words with digits
        #return text
    def is_russian(self, string):    
        if set(self.normalzWhitespace(string).replace(' ','')).issubset('́́ААаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсCcТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяËŽČŠŜÈÛÂëžčšŝèûâ\t\n\r\x0b\x0c!"#$%&\'()*+®,-./:\';<=>?@[\\]—^_`{|}~ʺʹ«„“»0123456789'):
            return True
        else:
            return False
    
    def ru_clean_text(self, text):
        text = str(text).strip()
        text=re.sub(r"http\S+", " ", text) # remove urls
        text = self.RU_lower(text)
        #text = self.normalzWhitespace(text)
        #text=re.sub('\w*\d\w*','', text) # remove words with digits
        #text=re.sub('\n',' ',text) # remove line breaks
        #text = re.sub("[0-9]","", text)
        text = ' '.join([w for w in text.split() if w not in rusStopWords])
        text=re.sub('[^́́ААаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяËŽČŠŜÈÛÂëžčšŝèûâ ]',' ',text) # remove all non-english text 
        text=re.sub(' +',' ',text) # remove extra whitespace
        return text.strip()    
    
    def cleanText(self,text):
        text = self.normalzWhitespace(text)
        text = self.filterLat2Russ(text)
        text=re.sub(' +',' ',text) # remove extra whitespace
        self.outtext = text.strip()

    def __str__(self):
        return self.outtext

class cleanEngText:
    '''Process English text with various cleaning tools that focus on IDing, lowercasing, removing stopwords, characters, normalizing whitespace
        and filtering out non-English segments'''
    def is_english(string):    
        if set(cleanEngText.normalzWhitespace(string).replace(' ','')).issubset('abcdeéfghijklmnopqrstuüvwxyzABCDEÉFGHIJKLMNOPQRSTUÜVWXYZ\t\n\r\x0b\x0c!"#$%&\'()*+®,-./:\';<=>?@[\\]—^_`{|}~ʺʹ«„“»0123456789'):
            return True
        else:
            return False
    def expand_contractions(text):
        '''Function for expanding contractions in English text'''

        contractions_dict = { "ain't": "are not","'s":" is","aren't": "are not","can't": "can not","can't've": "cannot have",
        "'cause": "because","could've": "could have","couldn't": "could not","couldn't've": "could not have",
        "didn't": "did not","doesn't": "does not","don't": "do not","hadn't": "had not","hadn't've": "had not have",
        "hasn't": "has not","haven't": "have not","he'd": "he would","he'd've": "he would have","he'll": "he will",
        "he'll've": "he will have","how'd": "how did","how'd'y": "how do you","how'll": "how will","i'd": "i would",
        "i'd've": "i would have","i'll": "i will","i'll've": "i will have","i'm": "i am","i've": "i have",
        "isn't": "is not","it'd": "it would","it'd've": "it would have","it'll": "it will","it'll've": "it will have",
        "let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have","mightn't": "might not",
        "mightn't've": "might not have","must've": "must have","mustn't": "must not","mustn't've": "must not have",
        "needn't": "need not","needn't've": "need not have","o'clock": "of the clock","oughtn't": "ought not",
        "oughtn't've": "ought not have","shan't": "shall not","sha'n't": "shall not",
        "shan't've": "shall not have","she'd": "she would","she'd've": "she would have","she'll": "she will",
        "she'll've": "she will have","should've": "should have","shouldn't": "should not",
        "shouldn't've": "should not have","so've": "so have","that'd": "that would","that'd've": "that would have",
        "there'd": "there would","there'd've": "there would have",
        "they'd": "they would","they'd've": "they would have","they'll": "they will","they'll've": "they will have",
        "they're": "they are","they've": "they have","to've": "to have","wasn't": "was not","we'd": "we would",
        "we'd've": "we would have","we'll": "we will","we'll've": "we will have","we're": "we are","we've": "we have",
        "weren't": "were not","what'll": "what will","what'll've": "what will have","what're": "what are",
        "what've": "what have","when've": "when have","where'd": "where did",
        "where've": "where have","who'll": "who will","who'll've": "who will have","who've": "who have",
        "why've": "why have","will've": "will have","won't": "will not","won't've": "will not have",
        "would've": "would have","wouldn't": "would not","wouldn't've": "would not have","y'all": "you all",
        "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
        "you'd": "you would","you'd've": "you would have","you'll": "you will","you'll've": "you will have",
        "you're": "you are","you've": "you have"}
        contractions_re=re.compile('(%s)' % '|'.join(contractions_dict.keys())) # Regular expression for finding contractions
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, text)
    
    def normalzWhitespace(string):
        string = re.sub('[ \t\n\r\x0b\x0c]+',' ', string)
        #string=re.sub(' +',' ',string)
        return string

    def en_clean_text(text):
        del_symbols = re.compile('[^0-9a-z #+]')
        del_symbols2 = re.compile('[/(){}\[\]\|@,;]')
        #text=re.sub('\w*\d\w*','', text) # remove words with digits
        #text=re.sub('\n',' ',text) # remove line breaks
        text=BeautifulSoup(text,'lxml', text)
        text = cleanEngText.normalzWhitespace(text)
        text = del_symbols.sub('', text) # delete symbols which are in del_symbols from text
        text = del_symbols2.sub('', text) # delete symbols which are in del_symbols2 from text
        text = str(text).lower().strip()
        text=re.sub(r"http\S+", "", text) # remove urls
        text = cleanEngText.expand_contractions(text).strip()
        text = ' '.join([w for w in text.split() if w not in engStopWords])
        #text = re.sub("[0-9]","", text)
        text=re.sub('[^abcdeéfghijklmnopqrstuüvwxyz]',' ',text) # remove all non-english text 
        text=re.sub(' +',' ',text) # remove extra whitespace
        return text.strip()