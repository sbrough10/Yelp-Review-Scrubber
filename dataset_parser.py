import json

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
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

def treeify(alist):
   node = []
   queue = [{"parent": None, "branch": None, "list": alist}]
   while 0 < len(queue):
      qdict = queue.pop()
      qlist = qdict["list"]
      if 0 < len(qlist):
         mid = len(qlist) // 2
         node.append({"value": qlist[mid], "left": None, "right": None})
         if qdict["parent"] != None:
            print(qdict["parent"])
            qdict["parent"][qdict["branch"]] = node
         queue.append({"parent": node, "branch": "right", "list": qlist[mid:]})
         queue.append({"parent": node, "branch": "left", "list": qlist[:mid]})
   return node[0]

def searchTree(value, tree):
   if value == tree["value"]:
      return True
   elif tree["left"] != None and value < tree["value"]:
      return searchTree(value, tree["left"])
   elif tree["right"] != None and tree["value"] < value:
      return searchTree(value, tree["right"])
   else:
      return False



businesses = []
minReviewCount = 10

bizFile = open('../yelp_academic_dataset_business.json')
for line in bizFile:
   jsonLn = json.loads(line)
   for category in jsonLn["categories"]:
      if category == "Restaurants":
         businesses.append(jsonLn["business_id"])
         continue

print("Restaurants identified: ", len(businesses))
mergeSort(businesses)
print("Sorted restauraunt list")
businessTree = treeify(businesses)
print("Treeified restaurant list")

users = []
usrFile = open('../yelp_academic_dataset_user.json')
for line in usrFile:
   jsonLn = json.loads(line)
   if minReviewCount <= jsonLn["review_count"]:
      users.append(jsonLn["user_id"])

print("Users selected: ", len(users))
mergeSort(users)
print("Sorted users")

reviews = []
revFile = open('../yelp_academic_dataset_review.json')
i = 0
for line in revFile:
   jsonLn = json.loads(line)
   hashKey = jsonLn["business_id"][0:1]
   if searchTree(jsonLn["business_id"], businessTree) and jsonLn["user_id"] in users:
      if 99 < i:
         print(len(reviews))
         i = 0
      i += 1
      reviews.append(jsonLn)

print(reviews)
print(len(reviews))
