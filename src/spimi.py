import sys
import json
import os
from tqdm import tqdm
import itertools
# global inv_index,doc_count

# BLOCK_SIZE = 100 # 1000000

# inv_index = {}
# doc_ids = 0
# token_cnt = 0
# block_id = 0
from collections import OrderedDict

def sort_terms(inv_index):
    """
    Sort terms alphabetically 
    """
    odict = OrderedDict(sorted(inv_index.items(),reverse=False))
    return(odict)

def create_index_block(token_stream: str,texttype:str):
    global inv_index,block_id,token_cnt

    for term in token_stream:
        token_cnt +=1
        # If term is not in dictionary, add dict(term,dict(textype,docId))
        if term not in inv_index:
            inv_index[term] = {}
            inv_index[term][texttype]=[] 
            # add Frequency to term
            #inv_index[term][texttype].append(1)
            # Posting list
            #inv_index[term][texttype].append({})
            inv_index[term][texttype].append(doc_count)
        # Else if term in dictionary, update posting list 
        else:
            if texttype not in inv_index[term].keys():
                inv_index[term][texttype]=[doc_count]
            else:
                if doc_count not in inv_index[term][texttype]:
                    inv_index[term][texttype].append(doc_count)
                    #

    if token_cnt >= BLOCK_SIZE:
        inv_index = sort_terms(inv_index)
        write_block_todisk(inv_index,block_id)
        print(token_cnt)

    return(None)

def write_block_todisk(inv_index: dict,blockid: int):
    """
    Writes sorted index to disk
    """
    with open(f'{sys.argv[2]}/{blockid}_index.json', "w") as outfile:
        #for k in inv_index:
        json.dump(inv_index ,outfile)
        #outfile.write('\n')

    # with open(f'{sys.argv[2]}/{blockid}_index.json', "w") as f:
    #     f.write("{")
    #     f.write("\n")
    #     for k in inv_index.keys():
    #         f.write("{}:{}".format(k, inv_index[k]))
    #         f.write(",")
    #         f.write("\n")
    #     f.write("}")

    # f = open(f'{sys.argv[2]}/{blockid}_index.json', "w")
    # f.write("{\n")
    # for k in inv_index.keys():
    #     f.write("'{}':'{}'".format(k, inv_index[k]))
    # f.write("}")
    # f.write("\n")
    # f.close()

    return(None)

def read_block_fromdisk(filename: str):
    """
    Reads sorted index from disk
    """
    with open(filename, 'r') as json_file: 
        dictionary = json.load(json_file)

def merge_blocks():
    master_inv_index = {}

    # open files simulatneously
    #file_pointer = [f.open_handle() for f in os.listdir(f'{sys.argv[2]}']):
    #file_pointer = [open(f) for f in os.listdir('inverted_indexes')]
    #print(file_pointer)
    #single_lines = [f.readline() for f in file_pointer]
    #print(single_lines)
    #temp_d = {}
    inverted_index = OrderedDict()
    doc_count = 0
    
    for blockfile in os.listdir(os.getcwd() + '/inverted_indexes/2020900039'):
        filename = os.getcwd() + '/inverted_indexes/2020900039/' + blockfile
        #print(filename)
        #block = read_block_fromdisk(filename)
        with open(filename, 'r') as json_file: 
            #print(filename)
            try:
                block = json.load(json_file)
                print(len(block))
                #print(postings)
                #doc_occurences = block[key]
                #postings.update(doc_occurences)
                #inverted_index[key] = postings
            except:
                continue
            for term in block:
                if term not in inverted_index:
                    inverted_index[term] = block[term]
                else: # If key in inverted_index
                    #None
                    # Check for texttype and update postings
                    for texttype in block[term].keys():
                        if texttype not in inverted_index[term].keys():
                            inverted_index[term][texttype]=block[term][texttype]
                            #inverted_index[term][texttype] = list(itertools.chain(*inverted_index[term][texttype]))
                            #print()
                        else:  # If field exist append 
                            if block[term][texttype] not in inverted_index[term][texttype]:
                                inverted_index[term][texttype].extend(block[term][texttype])
                            #else:
                                #inverted_index[term][texttype].extend(block[term][texttype])
                                #inverted_index[term][texttype] = list(itertools.chain(*inverted_index[term][texttype]))
                                #print(inverted_index[term][texttype])

    print(len(inverted_index))


    master_file = os.getcwd() + '/inverted_indexes/2020900039/' + 'master_index.json'
    with open(master_file, "w") as outfile:
        #for k in inv_index:
        json.dump(inverted_index,outfile)
    return(None)  

# if __name__ == "__main__":
#     merge_blocks()


     