# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:12:49 2022

@author: joneszc
"""

import win32com.client
import os, re, codecs
from datetime import datetime
import numpy as np

# MS Word Spelling Error types:
SpellingErrorTypeDict = {
    2: 'wdSpellingCapitalization: Capitalization error.',
    1: 'wdSpellingNotInDictionary: The word is not in the specified dictionary.',
    0: 'wdSpellingCorrect: Spelling is correct.'
}

# MS Word Language Names and Enumerations:
msWord_lng_codes = {
    'African': ['wdAfrikaans', 1078], 'Albanian': ['wdAlbanian', 1052], 'Amharic': ['wdAmharic', 1118], 
    'Arabic': ['wdArabic', 1025], 'Arabic Algerian': ['wdArabicAlgeria', 5121], 'Arabic Bahraini': ['wdArabicBahrain', 15361],
    'Arabic Egyptian': ['wdArabicEgypt', 3073], 'Arabic Iraqi': ['wdArabicIraq', 2049], 'Arabic Jordanian': ['wdArabicJordan', 11265],
    'Arabic Kuwaiti': ['wdArabicKuwait', 13313], 'Arabic Lebanese': ['wdArabicLebanon', 12289], 'Arabic Libyan': ['wdArabicLibya', 4097],
    'Arabic Moroccan': ['wdArabicMorocco', 6145], 'Arabic Omani': ['wdArabicOman', 8193], 'Arabic Qatari': ['wdArabicQatar', 16385],
    'Arabic Syrian': ['wdArabicSyria', 10241], 'Arabic Tunisian': ['wdArabicTunisia', 7169], 'Arabic United Arab Emirates': ['wdArabicUAE', 14337],
    'Arabic Yemeni': ['wdArabicYemen', 9217], 'Armenian': ['wdArmenian', 1067], 'Assamese': ['wdAssamese', 1101], 'Azeri Cyrillic': ['wdAzeriCyrillic', 2092],
    'Azeri Latin': ['wdAzeriLatin', 1068], 'Basque (Basque)': ['wdBasque', 1069], 'Belgian Dutch': ['wdBelgianDutch', 2067], 'Belgian French': ['wdBelgianFrench', 2060],
    'Bengali': ['wdBengali', 1093], 'Bulgarian': ['wdBulgarian', 1026], 'Burmese': ['wdBurmese', 1109], 'Belarusian': ['wdByelorussian', 1059],
    'Catalan': ['wdCatalan', 1027], 'Cherokee': ['wdCherokee', 1116], 'Chinese Hong Kong SAR': ['wdChineseHongKongSAR', 3076],
    'Chinese Macao SAR': ['wdChineseMacaoSAR', 5124], 'Chinese Singapore': ['wdChineseSingapore', 4100], 'Croatian': ['wdCroatian', 1050], 'Czech': ['wdCzech', 1029],
    'Danish': ['wdDanish', 1030], 'Divehi': ['wdDivehi', 1125], 'Dutch': ['wdDutch', 1043], 'Edo': ['wdEdo', 1126], 'Australian English': ['wdEnglishAUS', 3081],
    'Belize English': ['wdEnglishBelize', 10249], 'Canadian English': ['wdEnglishCanadian', 4105], 'Caribbean English': ['wdEnglishCaribbean', 9225],
    'Indonesian English': ['wdEnglishIndonesia', 14345], 'Irish English': ['wdEnglishIreland', 6153], 'Jamaican English': ['wdEnglishJamaica', 8201],
    'New Zealand English': ['wdEnglishNewZealand', 5129], 'Filipino English': ['wdEnglishPhilippines', 13321], 'South African English': ['wdEnglishSouthAfrica', 7177],
    'Tobago Trinidad English': ['wdEnglishTrinidadTobago', 11273], 'United Kingdom English': ['wdEnglishUK', 2057], 'United States English': ['wdEnglishUS', 1033],
    'Zimbabwe English': ['wdEnglishZimbabwe', 12297], 'Estonian': ['wdEstonian', 1061], 'Faeroese': ['wdFaeroese', 1080], 'Filipino': ['wdFilipino', 1124],
    'Finnish': ['wdFinnish', 1035], 'French': ['wdFrench', 1036], 'French Cameroon': ['wdFrenchCameroon', 11276], 'French Canadian': ['wdFrenchCanadian', 3084],
    'French (Congo (DRC))': ['wdFrenchCongoDRC', 9228], "French Cote d'Ivoire": ['wdFrenchCotedIvoire', 12300], 'French Haiti': ['wdFrenchHaiti', 15372],
    'French Luxembourg': ['wdFrenchLuxembourg', 5132], 'French Mali': ['wdFrenchMali', 13324], 'French Monaco': ['wdFrenchMonaco', 6156],
    'French Morocco': ['wdFrenchMorocco', 14348], 'French Reunion': ['wdFrenchReunion', 8204], 'French Senegal': ['wdFrenchSenegal', 10252],
    'French West Indies': ['wdFrenchWestIndies', 7180], 'Frisian Netherlands': ['wdFrisianNetherlands', 1122], 'Fulfulde': ['wdFulfulde', 1127],
    'Irish (Irish)': ['wdGaelicIreland', 2108], 'Scottish Gaelic': ['wdGaelicScotland', 1084], 'Galician': ['wdGalician', 1110], 'Georgian': ['wdGeorgian', 1079],
    'German': ['wdGerman', 1031], 'German Austrian': ['wdGermanAustria', 3079], 'German Liechtenstein': ['wdGermanLiechtenstein', 5127],
    'German Luxembourg': ['wdGermanLuxembourg', 4103], 'Greek': ['wdGreek', 1032], 'Guarani': ['wdGuarani', 1140], 'Gujarati': ['wdGujarati', 1095],
    'Hausa': ['wdHausa', 1128], 'Hawaiian': ['wdHawaiian', 1141], 'Hebrew': ['wdHebrew', 1037], 'Hindi': ['wdHindi', 1081], 'Hungarian': ['wdHungarian', 1038],
    'Ibibio': ['wdIbibio', 1129], 'Icelandic': ['wdIcelandic', 1039], 'Igbo': ['wdIgbo', 1136], 'Indonesian': ['wdIndonesian', 1057], 'Inuktitut': ['wdInuktitut', 1117],
    'Italian': ['wdItalian', 1040], 'Japanese': ['wdJapanese', 1041], 'Kannada': ['wdKannada', 1099], 'Kanuri': ['wdKanuri', 1137], 'Kashmiri': ['wdKashmiri', 1120],
    'Kazakh': ['wdKazakh', 1087], 'Khmer': ['wdKhmer', 1107], 'Kirghiz': ['wdKirghiz', 1088], 'Konkani': ['wdKonkani', 1111], 'Korean': ['wdKorean', 1042], 'Kyrgyz': ['wdKyrgyz', 1088],
    'No specified': ['wdLanguageNone', 0], 'Lao': ['wdLao', 1108], 'Latin': ['wdLatin', 1142], 'Latvian': ['wdLatvian', 1062], 'Lithuanian': ['wdLithuanian', 1063], 
    'Macedonian (FYROM)': ['wdMacedonianFYROM', 1071], 'Malayalam': ['wdMalayalam', 1100], 'Malay Brunei Darussalam': ['wdMalayBruneiDarussalam', 2110],
    'Malaysian': ['wdMalaysian', 1086], 'Maltese': ['wdMaltese', 1082], 'Manipuri': ['wdManipuri', 1112], 'Marathi': ['wdMarathi', 1102], 'Mexican Spanish': ['wdMexicanSpanish', 2058],
    'Mongolian': ['wdMongolian', 1104], 'Nepali': ['wdNepali', 1121], 'Disables proofing if the ID identifies a in which an object is grammatically validated using the Microsoft Word proofing tools': ['wdNoProofing', 1024],
    'Norwegian Bokmol': ['wdNorwegianBokmol', 1044], 'Norwegian Nynorsk': ['wdNorwegianNynorsk', 2068], 'Oriya': ['wdOriya', 1096], 'Oromo': ['wdOromo', 1138], 'Pashto': ['wdPashto', 1123], 'Persian': ['wdPersian', 1065],
    'Polish': ['wdPolish', 1045], 'Portuguese': ['wdPortuguese', 2070], 'Portuguese (Brazil)': ['wdPortugueseBrazil', 1046], 'Punjabi': ['wdPunjabi', 1094], 'Rhaeto Romanic': ['wdRhaetoRomanic', 1047],
    'Romanian': ['wdRomanian', 1048], 'Romanian Moldova': ['wdRomanianMoldova', 2072], 'Russian': ['wdRussian', 1049], 'Russian Moldova': ['wdRussianMoldova', 2073], 'Sami Lappish': ['wdSamiLappish', 1083],
    'Sanskrit': ['wdSanskrit', 1103], 'Serbian Cyrillic': ['wdSerbianCyrillic', 3098], 'Serbian Latin': ['wdSerbianLatin', 2074], 'Sesotho': ['wdSesotho', 1072], 'Simplified Chinese': ['wdSimplifiedChinese', 2052],
    'Sindhi': ['wdSindhi', 1113], 'Sindhi (Pakistan)': ['wdSindhiPakistan', 2137], 'Sinhalese': ['wdSinhalese', 1115], 'Slovakian': ['wdSlovak', 1051], 'Slovenian': ['wdSlovenian', 1060], 'Somali': ['wdSomali', 1143],
    'Sorbian': ['wdSorbian', 1070], 'Spanish': ['wdSpanish', 1034], 'Spanish Argentina': ['wdSpanishArgentina', 11274], 'Spanish Bolivian': ['wdSpanishBolivia', 16394], 'Spanish Chilean': ['wdSpanishChile', 13322],
    'Spanish Colombian': ['wdSpanishColombia', 9226], 'Spanish Costa Rican': ['wdSpanishCostaRica', 5130], 'Spanish Dominican Republic': ['wdSpanishDominicanRepublic', 7178], 'Spanish Ecuadorian': ['wdSpanishEcuador', 12298],
    'Spanish El Salvadorian': ['wdSpanishElSalvador', 17418], 'Spanish Guatemala': ['wdSpanishGuatemala', 4106], 'Spanish Honduran': ['wdSpanishHonduras', 18442], 'Spanish Modern Sort': ['wdSpanishModernSort', 3082],
    'Spanish Nicaraguan': ['wdSpanishNicaragua', 19466], 'Spanish Panamanian': ['wdSpanishPanama', 6154], 'Spanish Paraguayan': ['wdSpanishParaguay', 15370], 'Spanish Peruvian': ['wdSpanishPeru', 10250],
    'Spanish Puerto Rican': ['wdSpanishPuertoRico', 20490], 'Spanish Uruguayan': ['wdSpanishUruguay', 14346], 'Spanish Venezuelan': ['wdSpanishVenezuela', 8202], 'Sutu': ['wdSutu', 1072], 'Swahili': ['wdSwahili', 1089],
    'Swedish': ['wdSwedish', 1053], 'Swedish Finnish': ['wdSwedishFinland', 2077], 'Swiss French': ['wdSwissFrench', 4108], 'Swiss German': ['wdSwissGerman', 2055], 'Swiss Italian': ['wdSwissItalian', 2064],
    'Syriac': ['wdSyriac', 1114], 'Tajik': ['wdTajik', 1064], 'Tamazight': ['wdTamazight', 1119], 'Tamazight Latin': ['wdTamazightLatin', 2143], 'Tamil': ['wdTamil', 1097], 'Tatar': ['wdTatar', 1092],
    'Telugu': ['wdTelugu', 1098], 'Thai': ['wdThai', 1054], 'Tibetan': ['wdTibetan', 1105], 'Tigrigna Eritrea': ['wdTigrignaEritrea', 2163], 'Tigrigna Ethiopic': ['wdTigrignaEthiopic', 1139],
    'Traditional Chinese': ['wdTraditionalChinese', 1028], 'Tsonga': ['wdTsonga', 1073], 'Tswana': ['wdTswana', 1074], 'Turkish': ['wdTurkish', 1055], 'Turkmen': ['wdTurkmen', 1090], 'Ukrainian': ['wdUkrainian', 1058],
    'Urdu': ['wdUrdu', 1056], 'Uzbek Cyrillic': ['wdUzbekCyrillic', 2115], 'Uzbek Latin': ['wdUzbekLatin', 1091], 'Venda': ['wdVenda', 1075], 'Vietnamese': ['wdVietnamese', 1066], 'Welsh': ['wdWelsh', 1106],
    'Xhosa': ['wdXhosa', 1076], 'Yi': ['wdYi', 1144], 'Yiddish': ['wdYiddish', 1085], 'Yoruba': ['wdYoruba', 1130], 'Zulu': ['wdZulu', 1077]
}



def msWordProofreader(
    texts_list, language = "United States English",
    printOutput=False, get_proofread_txt=False, checkGrammaticalErrors=False,
    inplace=False, rmv_repeat_word=True, repeats_in_quotes=False
):
    '''
    -- Employs MS COM Object Model to programmatically spellcheck with MS Word --
    input:
        - texts_list: list() of strings that need to be proofread
        - language: str() of proper MS Word title of language as provided in the msWord_lng_codes dict
          (User must ensure that current installation of MS Word has Proofreading/Spellcheck enabled for input language)
        - printOutput: bool(), False; True performs a printout of all the spelling errors per segment
        - get_proofread_txt: bool(), False; True performs and returns a spelling correction inplace rather than a null value
        - checkGrammaticalErrors: bool(), False; True returns null (np.nan) inplace of the text if 
          grammar error detected & get_proofread_txt=False. If get_proofread_txt=True then grammar errors are ignored.
        - inplace: bool(), False; True performs all spelling corrections inplace on the input list
        - rmv_repeat_word: bool(), True; True performs removal of repeated words
        - repeats_in_quotes: bool(), False; True indicates a removal of repeated words even if in quotes
    output:
        Default setting: (get_proofread_txt=False) returns list of original texts
        with np.nan (null) values inplace of texts containing Spelling errors.
        --This feature is most beneficial for using the function to instantiate a
        pandas DataFrame column, which can be quickly filtered to eliminate NaN values.
        Alternative setting: (get_proofread_txt=True) returns list of original texts
        with Spelling Corrections substituted inplace for texts containing Spelling errors.
        --The first suggested spelling correction that MS Word recommends is chosen as best candidate. 
    '''
    if not inplace:
        texts_list = texts_list.copy()
    wdDoNotSaveChanges = 0
    timeget = str(datetime.now())
    timeget = timeget.split()
    timeget = timeget[0] + '_' + timeget[1][:8].replace(':','')
    path = os.path.abspath(timeget + '.txt')
    with codecs.open(path, 'w', encoding='utf-8') as file:
        for text in texts_list:
            file.write(text)
            file.write('\n')
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(path)
    paras_count = int(doc.Paragraphs.Count)
    for i in range(paras_count):
        doc.Paragraphs(i+1).Range.LanguageID=msWord_lng_codes[language][1] # for example, 1034 is code for Spanish & 1049 is Russian
    print("Proofreading Language:", word.Languages(doc.Content.LanguageID).Name)
    print("Total Grammar Errors: %d" % (doc.GrammaticalErrors.Count,))
    print("Total Spelling Errors: %d" % (doc.SpellingErrors.Count,))
    
    # Let's set a step for printing status updates, so we don't print excessively with large data sets:
    step = len(str(paras_count))-2 
    if step<0:
        step=0
    for i,p in enumerate(doc.Paragraphs):
        if 10%(10**step)==0:
            print('- Now proofreading segment #', str(i+1))
        #p.Range.LanguageID = 1049 # wdRussian
        spellErrors = p.Range.SpellingErrors
        spellErrorsCnt = int(spellErrors.Count)
        if checkGrammaticalErrors and not get_proofread_txt:
            grammarErrors = p.Range.GrammaticalErrors
            if grammarErrors.Count:
                #grammarErrorIdx.append(i)
                texts_list[i] = np.nan
                if printOutput:
                    print(
                        "Grammatical Error Count:",
                        grammarErrors.Count,
                        "\n",
                        [err.Text for err in grammarErrors] # print the erred text
                    )
                continue
        if  spellErrorsCnt>0:
            if printOutput:
                print(
                    "Spelling Error Count:",
                    spellErrorsCnt,
                    "\n",
                    [
                        (
                            SpellingErrorTypeDict[err.GetSpellingSuggestions().SpellingErrorType], # print the spelling error type
                            err.Text, # print the typo
                            [str(s) for s in err.GetSpellingSuggestions()] # print the spelling suggestions
                        )
                        for err in spellErrors
                    ]
                )
            for err in spellErrors:
                spSuggestions = err.GetSpellingSuggestions()
                if spSuggestions.SpellingErrorType in [1,2]:
                    if get_proofread_txt:
                        if spSuggestions.Count:
                            correction = [str(s) for s in spSuggestions][0] # Grab the 1st spelling suggestions
                            texts_list[i] = texts_list[i].replace(err.Text, correction, 1) # Make a text replacement at 1st instance
                    else:
                        texts_list[i] = np.nan
                elif rmv_repeat_word and spSuggestions.SpellingErrorType == 0: # 0 indicates a correct spelling but possible duplicate
                    if repeats_in_quotes:
                        dups = re.compile(r'\b(\w+)( \1\b)+') # removes duplicates in consecutive order
                    else:
                        dups = re.compile(r'(?<!")\b(\w+)( \1\b)+(?!")') # removes duplicates in consecutive order, if not in quotes
                    
                    if len(set(tt.strip() for t in re.findall(dups, texts_list[i]) for tt in t if tt.strip()==err.Text.strip())) == 1:
                        if get_proofread_txt:
                            texts_list[i] = re.sub(dups, r'\1', texts_list[i]) # remove duplicate text at 1st instance
                        else:
                            texts_list[i] = np.nan
                            
    doc.Close(wdDoNotSaveChanges)
    word.Quit(wdDoNotSaveChanges)
    word = None
    os.remove(path)

    return texts_list


test_list =[
    'Im that guy who joined the discussion too late on the last day during the first week',
    ' But I have a concern here with a a Convenience Sample, possibly incurring some bias, which probably occurs in Question 7',
    'I having a terrible days today but cannot not do not do well, i can also do that.'
    '29 of Homeowkr Section 1',
    'The currect.. aNswer to this question declares the census as the best study for determining average credi card debt',
    'I am interested to see what sampling tecqniques others would propose here to account for certain members who are unable to present credit card debt metrics',
    'Are there any few-shot sampling methods out there for small populations that might not serve as census candidates?']

proofread_list = msWordProofreader(
    test_list,
    language ='United States English',
    printOutput=True,
    get_proofread_txt = False,
    checkGrammaticalErrors=False,
    rmv_repeat_word=True,
    repeats_in_quotes = False
    )

print(proofread_list)
