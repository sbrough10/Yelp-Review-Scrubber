from operator import itemgetter
from collections import namedtuple
from sets import Set
import json
import csv

## Create a list of sets of relevant attributes for each business
def createbusinessset(businesses):
    relattr = []
    for business in businesses:
        attrset = set()
        attrset.add(business.business_id)

        # Late night
        if 'Good For' in business.attributes:
            if 'latenight' in business.attributes['Good For']:
                if business.attributes['Good For']['latenight']:
                    attrset.add('latenight-true')
                else:
                    attrset.add('latenight-false')
        # Credit Card
        if 'Accepts Credit Cards' in business.attributes:
            if business.attributes['Accepts Credit Cards']:
                attrset.add('creditcards-true')
            else:
                attrset.add('creditcards-false')
        # Take Out
        if 'Take-out' in business.attributes:
            if business.attributes['Take-out']:
                attrset.add('takeout-true')
            else:
                attrset.add('takeout-false')
        # Delivery
        if 'Delivery' in business.attributes:
            if business.attributes['Delivery']:
                attrset.add('delivery-true')
            else:
                attrset.add('delivery-false')
        # Alcohol
        if 'Alcohol' in business.attributes:
            if business.attributes['Alcohol'] == 'none':
                attrset.add('alcohol-false')
            else:
                attrset.add('alcohol-true')
        # Review Count
        if business.review_count > 31:
            attrset.add('trendy')
        else:
            attrset.add('nottrendy')
        # Neighborhood/City
        attrset.add(business.city)
        # Star Rating
        if business.stars <= 2:
            attrset.add('star-low')
        if business.stars == 3:
            attrset.add('star-med')
        if business.stars >= 4:
            attrset.add('star-high')
        # Price Range
        if 'Price Range' in business.attributes:
            if business.attributes['Price Range'] == 1:
                attrset.add('price-low')
            if business.attributes['Price Range'] == 2 or business.attributes['Price Range'] == 3:
                attrset.add('price-med')
            if business.attributes['Price Range'] == 4:
                attrset.add('price-high')
        # Ambience
         #ambience = []
        if 'Ambience' in business.attributes:
            if 'romantic' in business.attributes['Ambience']:
                if business.attributes['Ambience']['romantic']:
                    attrset.add('romantic')
            if 'intimate' in business.attributes['Ambience'] and business.attributes['Ambience']['intimate']:
                attrset.add('intimate')
            if 'classy' in business.attributes['Ambience'] and business.attributes['Ambience']['classy']:
                attrset.add('classy')
            if 'hipster' in business.attributes['Ambience'] and business.attributes['Ambience']['hipster']:
                attrset.add('hipster')
            if 'divey' in business.attributes['Ambience'] and business.attributes['Ambience']['divey']:
                attrset.add('divey')
            if 'touristy' in business.attributes['Ambience'] and business.attributes['Ambience']['touristy']:
                attrset.add('touristy')
            if 'trendy' in business.attributes['Ambience'] and business.attributes['Ambience']['trendy']:
                attrset.add('trendy')
            if 'upscale' in business.attributes['Ambience'] and business.attributes['Ambience']['upscale']:
                attrset.add('upscale')
            if 'casual' in business.attributes['Ambience'] and business.attributes['Ambience']['casual']:
                attrset.add('casual')
                
                # if ambience is not empty, add the set to attrset
           # s = frozenset(ambience)
           # if len(s) != 0:
           #     attrset.add(s)
            
        # Type of Food
        for category in business.categories:
            attrset.add(category)
        # Add set to list
        relattr.append(attrset)

        # Add set to object
        business.attributeset = attrset;
    
