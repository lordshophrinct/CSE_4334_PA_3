# Local prominent streak algorithm.

class Streak:
    def __init__(self, start, end, min_val):
        self.l = start
        self.r = end
        self.v = min_val
    
    def printStreak(self):
        print("<[{0}, {1}], {2}>".format(self.l, self.r, self.v))

    def getLength(self):
        return self.r - self.l

# Find the LPS streaks from a set of points
def LPS(vals):
    lps_streaks = []
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
            streak_list.append(Streak(i, i, current))
        # Otherwise, make a new streak going to this point
        else:
            l = streak_list[max_index].l
            streak_list.append(Streak(l, i, current))
        
        # Remove all the streaks that we marked
        for item in sorted(to_remove, reverse=True):
            streak_list.pop(item)

    # After the algorithm is done, any streaks that we're still keeping
    # track of need to be added to the LPS list
    for item in streak_list:
        lps_streaks.append(item)

    return lps_streaks

""" Main """
vals = [3, 1, 7, 7, 7, 2, 5, 4, 6, 7, 3]
vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 0, 2, 1]
streaks = LPS(vals)

for s in streaks:
    s.printStreak()