import json
import os.path
import math
import businessobject
import ideal_set
import comparesets

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

class Business(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
class Reviews(object):
  def __init__(review, user_id, stars, business_id):
    #Review attributes
    review.user_id = user_id
    review.stars = stars
    review.business_id = business_id


minReviewCount = 10
#get array of users with at least the minReviewCount
users = []
usrFile = open('yelp_academic_dataset_user.json')
for line in usrFile:
   jsonLn = json.loads(line)
   if minReviewCount <= jsonLn["review_count"]:
       users.append(User(jsonLn["user_id"],jsonLn["name"],jsonLn["review_count"],jsonLn["average_stars"], []))

      
#get array of businesses
data = []
bizFile = open('yelp_academic_dataset_business.json')
for line in bizFile:
   jsonLn = json.loads(line)
   for category in jsonLn["categories"]:
      if category == "Restaurants":
        data.append(jsonLn)
        
businesses = []
for number in data:
    businesses.append(Business(**number))
    

# Sorting business data by business_id
print("Restaurants identified: ", len(businesses))
mergeSort(businesses, 'business_id')
print("Sorted restauraunt list")


# Sorting user data by user_id
print("Users selected: ", len(users))
mergeSort(users, 'user_id')
print("Sorted user list")


#get array of reviews
revFile = open('yelp_academic_dataset_review.json')
reviews = []
for line in revFile:
   jsonLn = json.loads(line)
   business = binary_search(jsonLn["business_id"], businesses, 'business_id')
   user = binary_search(jsonLn["user_id"], users, 'user_id')
   if business != None and user != None:
      reviews.append(Reviews(jsonLn["user_id"], jsonLn["stars"], jsonLn["business_id"]))

      
#sort reviews by user
print("Reviews selected: ", len(reviews))
mergeSort(reviews, 'user_id')
print("Sorted reviews")

j = 0

for i in range (0, len(reviews) - 1):
    while (users[j].user_id != reviews[i].user_id):
        j = j + 1
    if (j < len(users)):
        users[j].reviews.append(reviews[i])


#create list of business sets
businessobject.createbusinessset(businesses)
print("Created business sets")

#create user set
ideal_set.idealset(users[1])
print("Create user set for user 1")

#compare user set to business sets and create list
comparisons = []
for business in businesses:
    comparisons.append(comparesets.matchsets(ideaset, business.attributeset, business.business_id))
    
#sort list
def getKey(item):
    return item[1]
sorted(comparisons, key=getKey, reverse=True)

#print suggestions
print "Suggested Businesses: ", comparisons[0:9]








    
