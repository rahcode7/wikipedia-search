# mkdir $2
touch $2/index.json
# touch $3
python indexer.py $1 $2 $3