import json
import os.path

class TreeNode(object):
  def __init__(self, value, left, right, searchValue):
    self.value = value
    self.left = left
    self.right = right
    self.searchValue = searchValue

  def addReview(self, review):
    self.reviews.append(review)

def setChild(self, node, branch):
  if branch == "left":
    self.left = node
  else:
    self.right = node

def mergeSort(alist, orderedLtoG):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf, orderedLtoG)
        mergeSort(righthalf, orderedLtoG)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if orderedLtoG(lefthalf[i], righthalf[j]):
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

# @param num, a list of integers
# @return a tree node
def sortedArrayToBST(num, searchValue):
    return sortedArrayToBSTRec(num, 0, len(num)-1, searchValue)
    
def sortedArrayToBSTRec(num, begin, end, searchValue):
    if begin>end:
        return None
    midPoint = (begin+end)//2
    root = TreeNode(num[midPoint], None, None, searchValue)
    root.left = sortedArrayToBSTRec(num, begin, midPoint-1, searchValue)
    root.right = sortedArrayToBSTRec(num, midPoint+1,end, searchValue)
    return root

def searchTree(value, tree):
   if value == tree.searchValue(tree.value):
      return tree.value
   elif tree.left != None and value < tree.searchValue(tree.value):
      return searchTree(value, tree.left)
   elif tree.right != None and tree.searchValue(tree.value) < value:
      return searchTree(value, tree.right)
   else:
      return None

def iterateTree(tree, iterator):
  iterator(tree.value)
  iterateTree(tree.left, iterator)
  iterateTree(tree.right, iterator)

def height(node):
    if node is None:
        return 0
    else:
        return max(height(node.left), height(node.right)) + 1


BizSets = { "latenight": set([]) }

businesses = []
minReviewCount = 10

bizFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_business.json')
for line in bizFile:
   jsonLn = json.loads(line)
   for category in jsonLn["categories"]:
      if category == "Restaurants":
         businesses.append(jsonLn)
         continue

print("Restaurants identified: ", len(businesses))
mergeSort(businesses, lambda left, right: left["business_id"] < right["business_id"])
print("Sorted restauraunt list")
businessTree = sortedArrayToBST(businesses, lambda value: value["business_id"])
print("Treeified restaurant list: (height) ", height(businessTree))

users = []
usrFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_user.json')
for line in usrFile:
   jsonLn = json.loads(line)
   if minReviewCount <= jsonLn["review_count"]:
      users.append(jsonLn)
      jsonLn["reviews"] = []

print("Users selected: ", len(users))
mergeSort(users, lambda left, right: left["user_id"] < right["user_id"])
print("Sorted user list")
userTree = sortedArrayToBST(users, lambda value: value["user_id"])
print("Treeified users list: (height) ", height(userTree))

reviews = []
revFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_review.json')
fwrite = open(os.path.dirname(__file__) + '/../consolidated_review_data.json', 'w+')
for line in revFile:
   jsonLn = json.loads(line)
   business = searchTree(jsonLn["business_id"], businessTree)
   user = searchTree(jsonLn["user_id"], userTree)
   if business != None and user != None:
      user["reviews"].append(jsonLn)
      reviews.append(jsonLn)
      fwrite.write(json.dumps(jsonLn) + "\n")

print("Completed writing reviews to file: " + str(len(reviews)))

for user in users:
  if len(user["reviews"]) < 27:
    users.remove(user)

print("Restaurant reviewers selected: " + str(len(users)))

userTree = sortedArrayToBST(users, lambda value: len(value["reviews"]))

