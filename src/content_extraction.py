# Separates  Title, Infobox, Body, Category, External Links and References
import re 

# Get References
# List of links containing list of token words 
def getWikiReferences(text,startswith="==References==",end="]]"):
    links = []
    referenceflag=0
    strs = text.split('\n')
    for s in strs:
        if s == startswith:
            referenceflag = 1
            continue
        if referenceflag == 1 and "http" in s:
            links.append(re.split(r"[/|=]",s))# split('/'))
    #print("References {}".format(links))

# Retrieve multiple categories
def getWikiCategory(text,startswith="[[Category:",end="]]"):
    #l = text.split(startswith)
    offset = len(startswith)
    categories = []
    strs = text.split('\n')
    for s in strs:
        if startswith in s and end in s:
            #stringfound = s[s.find(startswith)+offset:s.find(end)]
            #print(stringfound)
            categories.append(s[s.find(startswith)+offset:s.find(end)])
    #print("Categories found {}".format(categories))
    return(categories)

# Get Infobox list of items
# ['Aircraft Type', 'Two seat light aircraft', 'United Kingdom', 'Vickers', 'Rex Pierson R.K. Pierson', '1924', '1']

def getWikiInfobox(text,startswith="{{Infobox",end="}}"):
    info = []
    offset = len(startswith)
    infoflag=0
    endflag=0
    strs = text.split('\n')
    #print(strs)
    for s in strs:
        if startswith in s:
           infoflag = 1
           info.append(s[s.find(startswith)+offset:].strip())
           continue 
        elif infoflag == 1 and end == s:
            if len(end)>1:
               temp = re.sub('[^a-zA-Z0-9 \n\.]', ' ', s[:-2]).strip()
               if temp != '':
                   info.append(temp)
            endflag = 1
            infoflag = 0 
        elif infoflag == 1 and end != s:
            if len(s.split("="))>1:
                temp = re.sub('[^a-zA-Z0-9 \n\.]', ' ', s.split('=')[1]).strip()
                if temp != '':
                    info.append(temp)
        else:
           continue 
    #print("Info found {}".format(info))
    return(info)


def getExternalLinks(text,startswith="==External links==",end="]]"):
    extlinks = []
    extflag=0
    strs = text.split('\n')
    for s in strs:
        if s == startswith:
            extflag = 1
            continue
        if extflag == 1 and "http" in s:
            extlinks.append(re.split(r"[/|=]",s))# split('/'))
    #print("External Links {}".format(extlinks))
    return(extlinks)
        
def getWikiCategory(text,startswith="[[Category:",end="]]"):
    #l = text.split(startswith)
    offset = len(startswith)
    categories = []
    strs = text.split('\n')
    for s in strs:
        if startswith in s and end in s:
            #stringfound = s[s.find(startswith)+offset:s.find(end)]
            #print(stringfound)
            categories.append(s[s.find(startswith)+offset:s.find(end)])
    #print("Categories found {}".format(categories))
    return(categories)


# Return body text as string
def getWikiBody(text):
    strs = text.split('\n')
    #print(strs)
    body = ''
    infoflag=0
    for safter in strs:
        if '{{Infobox' in safter:
            infoflag=1
            #safter = safter[safter.find('{{Infobox}')+1:]
        if '}}' in safter and infoflag==1:
            infoflag=0
            safter = safter[safter.find('}}')+1:]
        if '#REDIRECT' not in safter and '{{Infobox' not in safter and '[[Category:' not in safter and infoflag==0:
            body += ' ' + safter
        body = ' '.join(x for x in body.split() if x.isalpha())
    return(body)


def getWikiInfoboxBody(text,startswith="{{Infobox",end="}}"):
    offset = len(startswith)
    infoflag=0
    info = []
    body=''
    categories = []

    startswithc="[[Category"
    endc="]]"
    offsetc = len(startswithc)

    referenceflag=0
    links = []
    startswithr="==References=="

    startswithe="==External links=="
    extlinks = []
    extflag=0

    strs = text.split('\n')
    #print(strs)
    for s in strs:
        if startswith in s:
           infoflag = 1
           info.append(s[s.find(startswith)+offset:].strip())
        elif infoflag == 1 and end in s:
            if len(s)>1:
                #temp = re.sub('[^a-zA-Z0-9 \n\.]', ' ', s[:-2]).strip()
                #if temp != '':
                info.append(re.sub('[^a-zA-Z0-9 \n\.]', ' ', s[:-2]).strip())
            infoflag = 0 
        #elif infoflag == 1 and end==s:
            #infoflag == 0
        elif infoflag == 1 and end != s:
            if len(s.split("="))>1:
                #temp = re.sub('[^a-zA-Z0-9 \n\.]', ' ', s.split('=')[1]).strip()
                #if temp != '':
                    #info.append(temp)
                info.append(re.sub('[^a-zA-Z0-9 \n\.]', ' ', s.split('=')[1]).strip())
        elif startswithc in s:
            categories.append(s[s.find(startswithc)+offsetc:s.find(endc)])
        elif startswithr==s:
            referenceflag = 1
        elif referenceflag == 1 and "http" in s:
            links.append(re.split(r"[/|=]",s))# split('/'))
        elif s == startswith:
            extflag = 1
        elif extflag == 1 and "http" in s:
            extlinks.append(re.split(r"[/|=]",s))# split('/'))
        #elif '#REDIRECT' not in s and '{{Infobox' not in s and '[[Category:' not in s and infoflag==0:
        elif '#REDIRECT' in s:
            continue
        else:
           body += ' ' + s
    info = list(filter(None, info))
    #print("Info found {}".format(info))
    body = ' '.join(x for x in body.split() if x.isalpha())
    #print(info)
    return(info,body,categories,links,extlinks)


