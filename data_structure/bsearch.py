#!/usr/bin/env python
#-*- coding: utf-8 -*-

def bsearch(list, val):

    list_size = len(list) - 1

    idx0 = 0
    idxn = list_size
    # Find the middle most value

    while idx0 <= idxn:
        midval = (idx0 + idxn) // 2

        if list[midval] == val:
            return midval
# Compare the value the middle most value
        if val > list[midval]:
            idx0 = midval + 1
        else:
            idxn = midval - 1

        if idx0 > idxn:
            return None

# Initialize the sorted list
list = [2, 7, 19, 34, 53, 72]

# Print the search result
print((bsearch(list, 72)))
print((bsearch(list, 11)))

def bsearch(list, idx0, idxn, val):

    if (idxn < idx0):
        return None
    else:
        midval = idx0 + ((idxn - idx0) // 2)
        # Compare the search item with middle most value

        if list[midval] > val:
            return bsearch(list, idx0, midval - 1, val)
        elif list[midval] < val:
            return bsearch(list, midval + 1, idxn, val)
        else:
            return midval

list = [8, 11, 24, 56, 88, 131]
print((bsearch(list, 0, 5, 24)))
print((bsearch(list, 0, 5, 51)))