# Local prominent streak algorithm.

import random
import time

# Data Object for keeping track of streaks
class Streak:
    def __init__(self, start, end, min_val, playerID):
        self.l = start # start index
        self.r = end # ending index
        self.v = min_val # minimum value
        self.playerID = playerID # the player id
    
    # Get the string representation of this streak in the form:
    # <'{PlayerID}': [{startIndex}, {endIndex}], {min value}>
    def getString(self):
        return "<{0}: [{1}, {2}], {3}>".format(self.playerID, self.l, self.r, self.v)

    # Get the data object
    # ('{PlayerID}', {startIndex}, {length}, {min value})
    def getData(self):
        return (self.playerID, self.l, self.getLength(), self.v)

    # Get the Length of this streak
    def getLength(self):
        return self.r - self.l


# Determine if 2 streaks dominate each other
# Return 0 if neither dominates, 1 if a dominates,
# and -1 if b dominates
def dominates(a, b):
    result = 0
    
    # One streak dominates the other if:
    # its length is greater and its min value is at least equal
    # OR if its length is at least equal and its min value is greater

    if ( a.getLength() > b.getLength() ) and ( a.v >= b.v ):
        result = 1
    
    elif ( a.v > b.v ) and ( a.getLength() >= b.getLength() ):
        result = 1

    elif ( b.getLength() > a.getLength() ) and ( b.v >= a.v ):
        result = -1

    elif ( b.v > a.v ) and ( b.getLength() >= a.getLength() ):
        result = -1

    return result
        

# Find the LPS streaks from a set of points
# (Note that it uses indeces starting at 0)
def LPS(vals, playerID, lps_streaks):
    streak_list = []

    # (With streaks as s and next value as k)
    # For every s with v < k, continue to extend
    # For every s with v > k, s is an LPS
    # For the longest s with v >= k, add a new streak from s.l to this point
    # If every s has v < k, add a new streak starting at k.

    for i in range(0, len(vals)):
        
        to_remove = [] # keep track of the streaks we will remove
        max_index = None # the index of the longest streak with v >= k
        current = vals[i] # the current data point we're looking at

        for j in range(0, len(streak_list)):
            s = streak_list[j] # keep track of the current streak

            # If the min value of s is less than the current point,
            # we should continue to expand s to the right
            if(s.v < current):
                s.r = i
                continue

            # If the min value of s is greater than the current point,
            # s is a local prominent streak
            elif(s.v > current):
                lps_streaks.append(s)
                to_remove.append(j) # we will need to remove this s
            
            # If the min value of s is equal to the current point,
            # we will need to remove s from the list of streaks
            else:
                to_remove.append(j)

            # For every s with min value greater or equal to the current
            # point, we will need to keep track of the longest one--
            # it will be added to the LPS list and a new streak going
            # to this point will take its place.
            if(s.v >= current):
                if(max_index is None):
                    max_index = j
                elif(s.l < streak_list[max_index].l):
                    max_index = j

        # If every streak had a min value less than the point,
        # we need to start a new streak from this point.
        if(max_index is None):
            streak_list.append(Streak(i, i, current, playerID))
        # Otherwise, make a new streak going to this point
        else:
            l = streak_list[max_index].l
            streak_list.append(Streak(l, i, current, playerID))
        
        # Remove all the streaks that we marked.
        # Source for removing multiple values:
        # https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time
        for item in sorted(to_remove, reverse=True):
            streak_list.pop(item)

    # After the algorithm is done, any streaks that we're still keeping
    # track of need to be added to the LPS list
    for item in streak_list:
        lps_streaks.append(item)


# Find the Skyline points from a list of candidate Streaks
def Skyline(candidates):
    skylines = []
    for i in range(0, len(candidates)):
        to_remove = []
        result = True

        for j in range(0, len(skylines)):
            dom = dominates(candidates[i], skylines[j])
            if dom is 0:
                continue
            elif dom is 1:
                to_remove.append(j)
            elif dom is -1:
                result = False
                break
        
        if result is True:
            skylines.append(candidates[i])
        
        for index in sorted(to_remove, reverse=True):
            skylines.pop(index)

    return skylines



# Get a random list of integers
def randList(bottom, top, size):

    if bottom > top:
        temp = bottom
        bottom = top
        top = temp

    values = []
    for i in range(0, size):
        x = random.randint(bottom, top)
        values.append(x)
    return values

""" Main """
vals = [3, 1, 7, 7, 2, 5, 4, 6, 7, 3]
vals2 = [10, 3, 4, 5, 6, 7, 8, 9, 10]
skylines = []
lps_streaks = []
LPS(vals, "Christopher", lps_streaks)
LPS(vals2, "Alex", lps_streaks)

for s in lps_streaks:
    print(s.getString())
print()

streaks = Skyline(lps_streaks)

for s in streaks:
    skylines.append(s.getData())

print(skylines)