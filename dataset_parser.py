import json
import os.path
import math

#allows object to be printed in json file
def jdefault(o):
    return o.__dict__

#sorts array by userid or businessid
def mergeSort(alist, ids):
    if len(alist) > 1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        
        mergeSort(lefthalf, ids)
        mergeSort(righthalf, ids)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if (ids == 'business_id'): #by business_id
              if (lefthalf[i].business_id < righthalf[j].business_id):
                  alist[k]=lefthalf[i]
                  i=i+1
              else:
                  alist[k]=righthalf[j]
                  j=j+1
            else: #by user_id
                if (lefthalf[i].user_id < righthalf[j].user_id):
                  alist[k]=lefthalf[i]
                  i=i+1
                else:
                  alist[k]=righthalf[j]
                  j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
  

#binary search by userid (must be sorted by userid)
def binary_search(value, alist, ids):
    last = len(alist) - 1
    first = 0
    found = None
    

    if (ids == 'user_id'): #by user_id
        while first <= last and not found:
           midpoint = (first + last) // 2
           if (alist[midpoint].user_id == value):
               found = True
           else:
                if (value < alist[midpoint].user_id):
                    last = midpoint - 1
                else:
                    first = midpoint + 1
        return found

    else: #by business_id
        while first <= last and not found:
            midpoint = (first + last) // 2
            if alist[midpoint].business_id == value:
               found = True
            else:
                if value < alist[midpoint].business_id:
                    last = midpoint - 1
                else:
                    first = midpoint+1
        return found
       
      
class User(object):
  def __init__(user, user_id, name, review_count, average_stars, reviews):
    #User attributes
    user.user_id = user_id
    user.name = name
    user.review_count = review_count
    user.average_stars = average_stars
    user.reviews = reviews

class Businesses(object):
   def __init__(business, business_id, categories, city, review_count, name, neighborhoods, stars, attributes):
    #Business attributes
    business.business_id = business_id
    business.categories = categories
    business.city = city
    business.review_count = review_count
    business.name = name
    business.neighborhoods = neighborhoods
    business.stars = stars
    business.attributes = attributes
    
class Reviews(object):
  def __init__(review, user_id, stars, business_id):
    #Review attributes
    review.user_id = user_id
    review.stars = stars
    review.business_id = business_id

#get array of users from filename with at least the minReviewCount
def getUsers(minReviewCount, filename):
    users = []
    usrFile = open(filename)
    for line in usrFile:
       jsonLn = json.loads(line)
       if minReviewCount <= jsonLn["review_count"]:
           users.append(User(jsonLn["user_id"],jsonLn["name"],jsonLn["review_count"], jsonLn["average_stars"], []))
    return users

#get array of businesses from filename
def getBusinesses(filename):
    businesses = []
    bizFile = open(filename)
    for line in bizFile:
        jsonLn = json.loads(line)
        for category in jsonLn["categories"]:
            if category == "Restaurants":
                businesses.append(Businesses(jsonLn["business_id"], jsonLn["categories"], jsonLn["city"], jsonLn["review_count"], jsonLn["name"], jsonLn["neighborhoods"], jsonLn["stars"], jsonLn["attributes"]))
    return businesses

#get array of reviews that are provided for the specified users and businesses
def getReviews(filename, users, businesses):
    revFile = open(filename)
    reviews = []
    for line in revFile:
        jsonLn = json.loads(line)
        business = binary_search(jsonLn["business_id"], businesses, 'business_id')
        user = binary_search(jsonLn["user_id"], users, 'user_id')
        if business != None and user != None:
            reviews.append(Reviews(jsonLn["user_id"], jsonLn["stars"], jsonLn["business_id"]))
    return reviews

#write data to json file 
def data_toJson(alist, filename, length):
    with open(filename, 'w') as outfile:
        for i in range(0, length - 1):
            jsonData = (json.dumps(alist[i], default=jdefault))
            outfile.write(jsonData + '\n')

#connect reviews to each user
def connectReviews(reviews, users):
    j = 0
    for i in range (0, len(reviews) - 1):
        while (users[j].user_id != reviews[i].user_id):
            j = j + 1
        if (j < len(users)):
            users[j].reviews.append(reviews[i])
    return users

#reduces users to only those with minReviewLength or more provided
def reduceUsers(users):
    users2 = []
    for i in range(0, len(users) - 1):
        if (len(users[i].reviews) >= minReviewCount):
            users2.append(users[i])
    return users2

#get array of users with at least the minReviewCount
minReviewCount = 27
users = getUsers(minReviewCount, 'yelp_academic_dataset_user.json')
     
#get array of restaurants and write to file
businesses = getBusinesses('yelp_academic_dataset_business.json')
data_toJson(businesses, 'Restaurants.json', len(businesses))
    
#Sorting business data by business_id
print("Restaurants identified: ", len(businesses))
mergeSort(businesses, 'business_id')
print("Sorted restauraunt list")

# Sorting user data by user_id
print("Users selected: ", len(users))
mergeSort(users, 'user_id')
print("Sorted user list")

#get array of reviews and sort by user
reviews = getReviews('yelp_academic_dataset_review.json', users, businesses)
print("Reviews selected: ", len(reviews))
mergeSort(reviews, 'user_id')
print("Sorted reviews")

#connect reviews to each user and discard users with less than minReviewCount
#associated to it 
users = connectReviews(reviews, users)
selected_users = reduceUsers(users)
print("New users selected: ", len(selected_users))

#writes selected users to file
data_toJson(selected_users, 'Recommend_Users.json', len(selected_users))
