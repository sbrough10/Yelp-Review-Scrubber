from operator import itemgetter
from collections import namedtuple
import collections
from sets import Set
import json
import csv

## Create "ideal set" for user    
def idealset(user, businessarray):
    
    idealset = set()
    latenight = 0;
    creditcard = 0;
    takeout = 0;
    delivery = 0;
    alcohol = 0;
    revcount = 0;
    
    city = ['1']
    star = ['1']
    price = ['1']
    ambience = ['1']
    typefood = ['1']
    for review in user.reviews:
        
        #find business_id from review
        b_id = review.business_id
        
        business = [item for item in businessarray if item.business_id == b_id]
        if hasattr(business, 'attributeset'):
            print b_id
            # Late night
            if 'latenight-true' in business.attributeset:
                latenight+=1
            if 'latenight-false' in business.attributeset:
                latenight-=1
            # Credit Card
            if 'creditcards-true' in business.attributeset:
                creditcard+=1
            if 'creditcards-false' in business.attributeset:
                creditcard-=1
            # Take Out
            if 'takeout-true' in business.attributeset:
                takeout+=1
            if 'takeout-false' in business.attributeset:
                takeout-=1
            # Delivery
            if 'delivery-true' in business.attributeset:
                delivery+=1
            if 'devliery-false' in business.attributeset:
                delivery-=1
            # Alcohol
            if 'alcohol-true' in business.attributeset:
                alcohol+=1
            if 'alcohol-false' in business.attributeset:
                alcohol-=1
            # Review Count
            if 'trendy' in business.attributeset:
                revcount+=1
            if 'nottrendy' in business.attributeset:
                revcount-=1
            # Neighborhood/City
            city.append(business.city)
            city.append('none')
            # Star Rating
            star.append(business.stars)
            star.append('none')
            # Price Range
            price.append('none')
            if 'Price Range' in business.attributes:          
                price.append(business.attributes['Price Range'])   
            # Ambience
            ambience.append('none')
            if 'romantic' in business.attributeset:
                ambience.append('romantic')
            if 'intimate' in business.attributeset:
                ambience.append('intimate')
            if 'classy' in business.attributeset:
                ambience.append('classy')
            if 'hipster' in business.attributeset:
                ambience.append('hipster')
            if 'divey' in business.attributeset:
                ambience.append('divey')
            if 'tourtisty' in business.attributeset:
                ambience.append('touristy')
            if 'trendy' in business.attributeset:
                ambience.append('trendy')
            if 'upscale' in business.attributeset:
                ambience.append('upscale')
            if 'casual' in business.attributeset:
                ambience.append('casual')
            # Type of Food
            typefood.append('none')
            for category in business.categories:
                typefood.append(category)
            
    if latenight > 0:
        idealset.add('latenight-true')
    if latenight < 0:
        idealset.add('latenight-false')
    if creditcard > 0:
        idealset.add('creditscard-true')
    if creditcard < 0:
        idealset.add('creditcards-false')
    if takeout > 0:
        idealset.add('takeout-true')
    if takeout < 0:
        idealset.add('takeout-false')
    if delivery > 0:
        idealset.add('delivery-true')
    if delivery < 0:
        idealset.add('delivery-false')
    if alcohol > 0:
        idealset.add('alcohol-true')
    if alcohol < 0:
        idealset.add('alcohol-false')
    if revcount > 0:
        idealset.add('trendy')
    if revcount < 0:
        idealset.add('nottrendy')
    c = collections.Counter(city)

    idealset.add(collections.Counter(city).most_common(1)[0][0])
    idstar = collections.Counter(star).most_common(1)[0][0]
    if idstar <= 2:
        idealset.add('star-low')
    if idstar == 3:
        idealset.add('star-med')
    if idstar >= 4:
        idealset.add('star-high')

    idprice = collections.Counter(price).most_common(1)[0][0]
    if idprice == 1:
        idealset.add('price-low')
    if idprice == 3 or idprice == 2:
        idealset.add('price-med')
    if idprice == 4:
        idealset.add('price-high')

    if len(ambience) >= 3:
        idealset.add(collections.Counter(ambience).most_common(3)[0][0])
        idealset.add(collections.Counter(ambience).most_common(3)[1][0])
        idealset.add(collections.Counter(ambience).most_common(3)[2][0])
    if len(ambience) == 2:
        idealset.add(collections.Counter(ambience).most_common(2)[0][0])
        idealset.add(collections.Counter(ambience).most_common(2)[1][0])
 
    if len(ambience) == 1:
        idealset.add(collections.Counter(ambience).most_common(1)[0][0])


    if len(typefood) >=3 :
        mosttypefood = collections.Counter(typefood).most_common(3)
        
        idealset.add(mosttypefood[0][0])
        idealset.add(mosttypefood[1][0])
        idealset.add(mosttypefood[2][0])

    if len(typefood) == 2:
        mosttypefood = collections.Counter(typefood).most_common(2)
        
        idealset.add(mosttypefood[0][0])
        idealset.add(mosttypefood[1][0])
    if len(typefood) == 1:
        mosttypefood = collections.Counter(typefood).most_common(1)
        
        idealset.add(mosttypefood[0][0])

    return idealset
