
# Prerequisites

Step 2
    - Contains code for searching - search.py and Indexing - indexer.py  

    - inverted_indexes/src - Download all files from Google drive - https://drive.google.com/drive/folders/1uLxJn3szxzOSW-_GMTFDfl4K9F19ZaLT?usp=sharing  

    - queries.txt - Sample query file, one can upload new quries in this text file  

    - Download file from https://dumps.wikimedia.org/enwiki/20210720/enwiki- 20210720- pages- articles- multistream.xml.bz2  

    - results - Gets created after re-run all code from this repo   
        - src_eval_results.txt 
        - src_stats.txt  




# To rerun all codes and perform indexing and search
rm src.zip 
rm -r inverted_indexes results 
zip -r src.zip src 
rm -r src 
bash eval.sh 


# To create indexes only
cd src
python indexer.py ../enwiki-20210720-pages-articles-multistream.xml ../inverted_indexes invertedindex_stat.txt 

bash index.sh enwiki-latest-pages-articles17.xml-p23570393p23716197 inverted_indexes/src/ invertedindex_stat.txt


