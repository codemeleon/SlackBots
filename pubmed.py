from Bio import Entrez
import datetime as dt

Entrez.email = "" # You email id

period = 1 # Period in days
max_search = 100 # Change according to your need


def search():
    now = dt.datetime.now()
    week = dt.datetime.now() - dt.timedelta(days=period) # Time gap
    your_query = "Microbiome" #  Alter your qyery here
    # query
    query = "(\"%s\"[All Fields]) AND \"%d/%d/%d %d.%d\"[MHDA]:\"%d/%d/%d %d.%d\"[MHDA])" % (your_query, week.year, week.month, week.day, week.hour, week.minute,
                                                                                                       now.year, now.month, now.day, now.hour, now.minute)
    # print(query)
    handle = Entrez.esearch(db = "pubmed",
                            sort="relevance",
                            retmax=max_search,
                            retmode="xml",
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    # print(ids)
    handle = Entrez.efetch(db = "pubmed",
                           retmode="xml",
                           id=str(ids))
    # print(handle)
    results = Entrez.read(handle)
    return results["PubmedArticle"]

if __name__ == '__main__':
    results = search()
    id_list = results["IdList"]
    # print(id,list)
    papers = fetch_details(id_list)
    # print(papers)
    for pid, paper in zip(id_list, papers):
        print(pid, paper['MedlineCitation']['Article']['ArticleTitle'])
