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


def getUserCity(user):
   reviews = user.reviews
   cities = {}
   for review in reviews:
      city = review.business.city
      if city not in cities:
         cities[city] = 0
      cities[city] = cities[city] + 1

   maxCity = None
   maxStars = 0
   for city in cities:
      if maxCity == None or maxStars < cities[city]:
         maxCity = city
         maxStars = cities[city]

   return maxCity