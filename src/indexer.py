import xml.sax
import time
import sys
from textprocessing import textprocessor
from content_extraction import getWikiInfoboxBody
import more_itertools
from spimi import sort_terms,write_block_todisk,merge_blocks
import os
import pandas as pd
import pickle
from collections import Counter

doc_count = 0
doc_file = {}

#term_count = 0 
inv_index = {}
#inv_index_text = {}
doc_text = []
all_text = []
token_cnt = 0
#token_main_cnt =0
block_id = 0
BLOCK_SIZE = 3000000 # 1000000
index = 0
doc_title = ""
import json
wordfreq = {}


doc_file_df = pd.DataFrame(columns=['docid','doc_length','doctitle'])


class XmlWikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentdata = ""
        self.title = ""
        self.id = ""
        #self.redirect=""
        self.text=""
    
    def UpdateWikiIndex(self,token_stream: str,texttype:str,wordfreq :dict):
        global inv_index,block_id,token_cnt,BLOCK_SIZE,doc_count
        
        for term in token_stream:
            token_cnt +=1
            #token_main_cnt +=1
            # Write individual blocks of texts
            if token_cnt == BLOCK_SIZE:
                print(token_cnt)
                inv_index = sort_terms(inv_index)
                write_block_todisk(inv_index,block_id)
                inv_index = {}
                block_id +=1
                token_cnt = 0
                break

            if term in inv_index:
                #print(inv_index)
                if texttype not in inv_index[term].keys():
                    inv_index[term][texttype]=[tuple((doc_count,wordfreq[term]))]
                    #inv_index[term][texttype].append(1)
                    #inv_index[term][texttype].append({})
                    # update frequencey to term
                    #inv_index[term][texttype].append(doc_count)
                else:
                    if doc_count not in inv_index[term][texttype]:
                        inv_index[term][texttype].append(tuple((doc_count,wordfreq[term])))
                    

                # update posting list with position of the term
                # If term exists in docid, 
                # if doc_count in inv_index[term][1]:
                #     inv_index[term][1][doc_count].append(termpos)
                # else:
                #     inv_index[term][1][doc_count] = [termpos]
                # if doc_count not in inv_index[term][1]:
                #     inv_index[term][1].append(doc_count)   
            else:
                inv_index[str(term)] = {}
                inv_index[term][texttype]=[] 
                # add Frequency to term
                #inv_index[term][texttype].append(1)
                # Posting list
                #inv_index[term][texttype].append({})
                inv_index[term][texttype].append(tuple((doc_count,wordfreq[term])))
            
            #inv_index[term][texttype] = [tuple((i)) for i in inv_index[term][texttype]]

        #doc_count+=1
        #doc_file[doc_count] = len(doc_text)
        return(None)
        
    def startElement(self,name, attrs):
        self.currentdata=name
        self.text =""
        self.title=""

    def endElement(self, name):
        global term_count,all_text,doc_count,doc_file,doc_text,doc_file_df,doc_title,wordfreq
        if self.currentdata=='title':
            doc_title = self.title  # Get raw title
            self.title,cnt = textprocessor(self.title)
            doc_count+=1
            wordfreq = Counter(self.title)
            doc_text = []
            all_text.extend(cnt)
            doc_text.extend(cnt)
            self.UpdateWikiIndex(self.title,'t',wordfreq)
        if self.currentdata=='text':
            i,b,c,r,e = getWikiInfoboxBody(self.text)
            if i is not None:
                i,cnt = textprocessor(' '.join(i))
                wordfreq = Counter(i)
                all_text.extend(cnt)
                doc_text.extend(cnt)
                self.UpdateWikiIndex(i,'i',wordfreq)
            if b is not None:
                b,cnt = textprocessor(b)
                wordfreq = Counter(b)
                all_text.extend(cnt)
                doc_text.extend(cnt)
                self.UpdateWikiIndex(b,'b',wordfreq)

            if c is not None:
                c,cnt = textprocessor(' '.join(c))
                wordfreq = Counter(c)
                all_text.extend(cnt)
                doc_text.extend(cnt)
                self.UpdateWikiIndex(c,'c',wordfreq)

            if r is not None:
                r,cnt = textprocessor(" ".join([' '.join(x) for x in r]))
                wordfreq = Counter(r)
                all_text.extend(cnt)
                doc_text.extend(cnt)
                self.UpdateWikiIndex(r,'r',wordfreq)
            
            if e is not None:
                e,cnt = textprocessor(" ".join([' '.join(x) for x in e]))
                wordfreq = Counter(e)
                all_text.extend(cnt)
                doc_text.extend(cnt)
                self.UpdateWikiIndex(e,'e',wordfreq)
            #print(doc_text) 

            doc_file_df.loc[doc_count]= [doc_count,len(doc_text),doc_title]
            #doc_file[doc_count] = len(doc_text)

    def characters(self, content):
        if self.currentdata=='id':
            self.id = content
        if self.currentdata=='title':
            self.title = content
        if self.currentdata=='text':
            self.text += content
        
if __name__=='__main__':

    parser = xml.sax.make_parser()
    handler = XmlWikiHandler()
    print(handler)
    parser.setContentHandler(handler)

    start_time = time.time()
    #parser.parse("../enwiki-latest-pages-articles17.xml-p23570393p23716197")
    # For testing
    #parser.parse("../enwiki-latest-pages-articles17.xml-p23570393p23716197-s")
    # Preprocess documents 
    parser.parse(sys.argv[1])
    
    
    #print(more_itertools.take(100, inv_index.items()))

    #inv_index = {k:v for k,v in sorted (inv_index.items())}

    # create list of strings
    #list_of_strings = [ f'{key} : {inv_index[key]}' for key in inv_index ]

    # write string one by one adding newline
    # with open(f'{sys.argv[2]}/indexfile.txt', 'w') as my_file:
    #     [my_file.write(f'{st}\n') for st in list_of_strings ]
    # with open(f'{sys.argv[2]}/index.json', "w") as outfile:
    #     #json.dump(inv_index , outfile,indent=2)
    #     json.dump(inv_index , outfile)
    end_time = time.time()
    

    index_size = len(inv_index)
    #print("Num of words at start {}".format(term_count))
    # print("Num of words at start {}".format(str(len(all_text)))) 
    # print("Num of words found {}".format(index_size))
    # print("Num of documents found {}".format(doc_count))

    print("Total time: {}".format(end_time-start_time))

    path, dirs, files = next(os.walk(os.getcwd()+"/inverted_indexes/2020900039"))
    file_count = len(files)
    print("No of index files {}".format(file_count))

    size = 0
    for ele in os.scandir((os.getcwd() +"/inverted_indexes/2020900039")):
        size+=os.path.getsize(ele)
    size = round(size/(1024*1024*1024),2)


    with open(sys.argv[3], 'w') as my_file:
        #my_file.write(str(term_count))
        my_file.write("Index size : " +str(size) + " GB")
        my_file.write('\n')
        my_file.write("No of index files : " + str(file_count))
        my_file.write('\n')
        my_file.write("No of tokens in inverted index : " + str(index_size))
           

    #print(doc_file_df.head(10))

    filename = os.getcwd() + '/inverted_indexes/2020900039/' + 'doc_file.csv'

    #doc_file_df.to_pickle(filename)
    doc_file_df.to_csv(filename,index=False)

    merge_blocks()

    
    