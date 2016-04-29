from operator import itemgetter
from collections import namedtuple
from sets import Set
import json
import csv

## returns the number of matches in a list with the business id
def matchsets(userset, businessset, business_id):
    nummatch = []
    nummatch.append(business_id)
    matchset = []
    
    matchset = userset.intersection(businessset)
    nummatch.append(len(matchset))
    return nummatch


    
