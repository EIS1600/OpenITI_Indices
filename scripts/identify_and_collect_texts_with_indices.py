import re, math, os.path, sys, os, csv, shutil

"""
1. load metadata (start with EIS1600 texts, move to others)
2. algorithm:
    - focus on the last 20% of a text (20% of lines, not the entire text)
    - compare the ratio of words to numbers (as a measuting stick, use the ration from 0637IbnDubaythi.DhaylTarikhBaghdad.Masaha004452Vols-ara1)
    - if the ratio of numbers is higher, copy the text into the "texts" folder
3. collected texts should be tagged in the following manner:
    - # |INDICES|
    - # |TOPONYMS|
    - # |PERSONS|
    - # ...
    - # |ETC.|
4. another script to process tagged texts in indices:
    - automatically extract and aggregate by types
5. do some manual filtering and arranging;
"""

fahrasRE = r"\b(beg|فهرس|end)\b"

def indexTest(text):
    fahras = len(re.findall(fahrasRE, text))

    text = text.split("\n")
    indexPart = int((len(text)/5))
    #print(indexPart)

    textToTest = "\n".join(text[-indexPart:])

    numbers = len(re.findall(r"\b\d+\b", textToTest))
    words   = len(re.findall(r"\b\w+\b", textToTest))

    #print("fihrist: ", fahras)
    #print("numbers: ", numbers)
    #print("words:   ", words)

    result = numbers/words
    #print("numbers/words = ", result)
    
    return(result)

"""
0637IbnDubaythi.DhaylTarikhBaghdad
87106
numbers:  36877
words:    178959
numbers/words =  0.20606395878385553
"""


########################################################################################################################
# PATHS and VARIABLES ##################################################################################################
########################################################################################################################

targetPath   = "../texts/"
OpenITIpath  = "/Users/romanov/_OpenITI/_main_corpus/"

path_to_metadata_file1 = "/Users/romanov/Dropbox/Mac (2)/Downloads/_EIS1600 - Text Selection - Serial Source Test - EIS1600_AutomaticSelectionForReview.tsv"
path_to_metadata_file2 = "/Users/romanov/Dropbox/Mac (2)/Downloads/kitab-corpusmetadata.csv"

########################################################################################################################
# CODE #################################################################################################################
########################################################################################################################

def cleanText(textToClean):
    text = textToClean
    text = re.sub("\n~~", " ", text)
    text = re.sub("\n# ", "\n\n", text)

    text = re.sub(r"Page\w+", "\n\n", text)
    text = re.sub(r"ms\d+", "", text)

    text = re.sub(" +", " ", text)
    text = re.sub("\n{3,}", "\n\n", text)

    return(text)

"""
with open(path_to_metadata_file1, "r", encoding="utf8") as f1:
    for line in csv.DictReader(f1, delimiter="\t"):
        #print(line)

        bookURI = line["Book Title"]
        pathSource = line["sourcePath"]
        pathTarget = targetPath + pathSource.split("/data/")[1]

        print(pathSource)
        print(pathTarget)
        folderTarget = os.path.dirname(pathTarget)

        #print("="*80)

        with open(pathSource, "r", encoding="utf8") as f1:
            #print(bookURI)
            textForTesting = f1.read()
            result = indexTest(textForTesting)

            if result > 0.095:
                print(bookURI, ":: ", result)
                target = targetPath + pathSource.split("/")[-1] + ".INDICES"
                with open(pathSource, "r", encoding="utf8") as f1:
                    text = f1.read()
                    text = cleanText(text)
                with open(target, "w", encoding="utf8") as f9:
                    f9.write(text)
                #shutil.copyfile(pathSource, target)
"""

files = os.listdir(targetPath)
indices = os.listdir("../indices/")

files = files + indices

with open(path_to_metadata_file2, "r", encoding="utf8") as f1:
    for line in csv.DictReader(f1, delimiter=","):
        #input(line)

        bookURI = line["Book Title"]
        pathSource = line["PATH"].replace("https://raw.githubusercontent.com/OpenITI/", OpenITIpath).replace("/master/", "/")
        pathTarget = targetPath + pathSource.split("/")[-1] + ".INDICES"

        #print(pathSource)
        #print(pathTarget)
        folderTarget = os.path.dirname(pathTarget)

        fileName = pathSource.split("/")[-1] + ".INDICES"
        print("\t=", fileName)

        if fileName not in files:
            if not os.path.isfile(pathTarget) and os.path.isfile(pathSource):
                with open(pathSource, "r", encoding="utf8") as f1:
                    textForTesting = f1.read()
                    result = indexTest(textForTesting)
                    tLen = len(re.findall(r"\w+", textForTesting))

                    if result > 0.095:
                        if tLen > 10000:
                            print(bookURI, ":: ", result)
                            target = targetPath + pathSource.split("/")[-1] + ".INDICES"
                            with open(pathSource, "r", encoding="utf8") as f1:
                                text = f1.read()
                                text = cleanText(text)
                            with open(pathTarget, "w", encoding="utf8") as f9:
                                f9.write(text)
                            print("\t", bookURI, ": ", result)
                            #input("waiting...")
                            #shutil.copyfile(pathSource, target)
                        else:
                            print("\t", bookURI, " is too short.")

        else:
            print("PROCESSED: ", fileName)
            #input()