import json
import os.path

class TreeNode(object):
  def __init__(self, value, left, right):
    self.value = value
    self.left = left
    self.right = right

  def setChild(self, node, branch):
    if branch == "left":
      self.left = node
    else:
      self.right = node


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
   nodes = []
   queue = [{"parent": None, "branch": None, "list": alist}]
   i = 0
   while 0 < len(queue):
      qdict = queue.pop()
      qlist = qdict["list"]
      if 1 < len(qlist):
        mid = len(qlist) // 2
        #print("length: ", len(qlist), "mid: ", mid)
        node = Tree(qlist[mid], None, None)
        if qdict["parent"] != None:
          qdict["parent"].setChild(node, qdict["branch"])
        nodes.append(node)
        queue.append({"parent": node, "branch": "right", "list": qlist[mid:]})
        queue.append({"parent": node, "branch": "left", "list": qlist[:mid]})
   return nodes[0]


# @param num, a list of integers
# @return a tree node
def sortedArrayToBST(num):
    return sortedArrayToBSTRec(num, 0, len(num)-1)
    
def sortedArrayToBSTRec(num, begin, end):
    if begin>end:
        return None
    midPoint = (begin+end)//2
    root = TreeNode(num[midPoint], None, None)
    root.left = sortedArrayToBSTRec(num, begin, midPoint-1)
    root.right = sortedArrayToBSTRec(num, midPoint+1,end)
    return root

def searchTree(value, tree):
   if value == tree.value:
      return True
   elif tree.left != None and value < tree.value:
      return searchTree(value, tree.left)
   elif tree.right != None and tree.right < value:
      return searchTree(value, tree.right)
   else:
      return False

def height(node):
    if node is None:
        return 0
    else:
        return max(height(node.left), height(node.right)) + 1

def getTreeHeight(tree):
  queue = [tree]
  height = 1
  while 0 < len(queue):
    continues = False
    for item in queue:
      if item.left != None:
        continues = True
        queue.append(item.left)
      if item.right != None:
        continues = True
        queue.append(item.right)
    if continues:
      height += 1
  return height


businesses = []
minReviewCount = 10

bizFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_business.json')
for line in bizFile:
   jsonLn = json.loads(line)
   for category in jsonLn["categories"]:
      if category == "Restaurants":
         businesses.append(jsonLn["business_id"])
         continue

print("Restaurants identified: ", len(businesses))
mergeSort(businesses)
print("Sorted restauraunt list")
businessTree = sortedArrayToBST(businesses)
print("Treeified restaurant list: (height) ", height(businessTree))

users = []
usrFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_user.json')
for line in usrFile:
   jsonLn = json.loads(line)
   if minReviewCount <= jsonLn["review_count"]:
      users.append(jsonLn["user_id"])

print("Users selected: ", len(users))
mergeSort(users)
print("Sorted user list")
userTree = sortedArrayToBST(users)
print("Treeified users list: (height) ", height(userTree))

reviews = []
revFile = open(os.path.dirname(__file__) + '/../yelp_academic_dataset_review.json')
i = 0
for line in revFile:
   jsonLn = json.loads(line)
   if searchTree(jsonLn["business_id"], businessTree) and searchTree(jsonLn["user_id"], userTree):
      if 99 < i:
         print(len(reviews))
         i = 0
      i += 1
      reviews.append(jsonLn)

print(reviews)
print(len(reviews))

