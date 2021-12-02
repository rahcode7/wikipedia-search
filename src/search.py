# Example query - t:World Cup i:2018 c:Football
import sys 
import json 
import os
import pickle
import pandas as pd

def tf_idf_scores(qterm,qfield,inv_index,doc_file):
    #print(qterm)
    #print(qfield)
    NUM_CORPUS_DOCS = len(doc_file.index)
    #print(NUM_CORPUS_DOCS)
    # Get TF scores - field specific
    field_ids_dict = inv_index[qterm]
    #print(field_ids_dict)
    docfreq = []
    if qfield !='':
        for fields in field_ids_dict.keys():
            #print(fields)
            if qfield == fields:
                #print(True)
                docfreq.extend(field_ids_dict[qfield])
            #else:
                #docfreq = []
    else: # if no field
        for fields in field_ids_dict.keys():
            docfreq.extend(field_ids_dict[fields])

    docfreq = [tuple((i)) for i in docfreq]
    #print(docfreq)
    docfreq = list(set(docfreq))
    #print(docfreq)
    tf_dict = {}
    for doc in docfreq:
        # of time words occur in doc/# of terms in the doc
        tf_dict[doc[0]]=round(doc[1]/doc_file[doc_file['docid']==doc[0]]['doc_length'].values[0],4)
    # # Get IDF scores - 
    idf_dict = {}
    for doc in docfreq:
        idf_dict[doc[0]]= round(NUM_CORPUS_DOCS /len(docfreq) ,4)  # total # of docs/# of documents which contains terms t 

    # Get tf-idf scores 
    tfidf_dict = {}
    for k in idf_dict:
        try:
            tfidf_dict[k] = tf_dict[k]*idf_dict[k]
        except:
            continue
    return(tfidf_dict)


if __name__ == "__main__":
    
    #f = open('indexes/indexfile.json')
    filename = os.getcwd() + '/inverted_indexes/2020900039/' + 'master_index.json'
    with open(filename, 'r') as json_file: 
       inv_index = json.load(json_file)
    
    filename = os.getcwd() + '/inverted_indexes/2020900039/' + 'doc_file.csv'
    #doc_file_df = pd.read_pickle(filename)
    doc_file_df = pd.read_csv(filename)

    #print(doc_file_df.head(3))

    # Search for query
    # q = sys.argv[2]
    # with open(f'{sys.argv[2]}', 'r') as file:
    #    q = file.read()
    # #f = open(q)

    # myfile = open(f'{sys.argv[2]}', "r")
    # q = myfile.readline()
    # while q:
    #     print(q)
    #     q = myfile.readline()
    #q = "b:world i:cup"
    #q = "cricket world cup"

    l = sys.argv[2:]
    print(' '.join(l))
    #l = q.split(' ')
    key = ''
    word = ''
    
    #l = ['t:World', 'Cup'] #, 'i:2018', 'c:Football']
    tf_idf = pd.DataFrame(columns=['docid','tfidfscore','word'])


    for i in l:
        #print(i)
        i = i.lower()
        if ':' in i:
            key,word=i.split(':')
            word_dict = tf_idf_scores(word,key,inv_index,doc_file_df)
            #print(word_dict)
            word_df = pd.DataFrame(list(word_dict.items()),columns = ['docid','tfidfscore'])
            word_df['word']=word
            #print(word_df)
            #tf_idf.append(word_df,ignore_index=True)
            tf_idf = pd.concat([tf_idf,word_df])
        elif i in inv_index.keys() and key=='':
            word_dict = tf_idf_scores(i,key,inv_index,doc_file_df)   
            word_df = pd.DataFrame(list(word_dict.items()),columns = ['docid','tfidfscore'])
            word_df['word']=i
            #print(word_df)
            #tf_idf.append(word_df, ignore_index=True)
            tf_idf = pd.concat([tf_idf,word_df])
        else:
            #print("Word doesn't exist")
            continue
   #print(tfidf_dict.keys())
    #print(tf_idf)


    # Get list of top 10 doc ids with highest tf-idf
    #print(tf_idf.groupby(['docid'])['tfidfscore'].sum().reset_index())
    df = tf_idf.groupby(['docid'])['tfidfscore'].sum().reset_index()
    topdf = df.sort_values(by=['tfidfscore'],ascending=False).head(10)
    #print(topdf)

    topids = [x-1 for x in topdf['docid']]
    if len(topids)==0:
        print("Word doesn't exist")
    else:
        print(doc_file_df.iloc[topids][['docid','doctitle']].to_string(index=False))
    print("\n")
    