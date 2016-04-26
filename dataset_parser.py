import json
import os.path
import math
import sorting
       
      
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


minReviewCount = 10
#get array of users with at least the minReviewCount
users = []
usrFile = open('yelp_academic_dataset_user.json')
for line in usrFile:
   jsonLn = json.loads(line)
   if minReviewCount <= jsonLn["review_count"]:
       users.append(User(jsonLn["user_id"],jsonLn["name"],jsonLn["review_count"],jsonLn["average_stars"], []))

      
#get array of businesses
businesses = []
bizFile = open('yelp_academic_dataset_business.json')
for line in bizFile:
   jsonLn = json.loads(line)
   for category in jsonLn["categories"]:
      if category == "Restaurants":
        businesses.append(Businesses(jsonLn["business_id"], jsonLn["categories"], jsonLn["city"], jsonLn["review_count"], jsonLn["name"], jsonLn["neighborhoods"], jsonLn["stars"], jsonLn["attributes"])) 

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