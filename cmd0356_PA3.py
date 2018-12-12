import pandas as pd
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
        # For some reason, I was getting an off-by-one error compared
        # with the sample results. Adding one fixed the issue.
        return self.r - self.l + 1


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


def readfiles():    
    #read from the csv file and return a Pandas DataFrame.
    nba = pd.read_csv("1991-2004-nba.dat",  delimiter='#')
        
    #Pandas DataFrame allows you to select columns. 
    #We use column selection to split the data. 
    #We only need 2 columns in the data file: Player ID and Points.
    columns = ['ID', 'PTS']
    nba_records = nba[columns]
    
    #For each player, store the player's points in all games in an ordered list.
    #Store all players' sequences in a dictionary.
    pts = {}    
    cur_player = 'NULL'
    #The data file is already sorted by player IDs, followed by dates.
    for index, row in nba_records.iterrows():
        player, points = row
        if player != cur_player:
            cur_player = player
            pts[player] = []            
        pts[player].append(points)

    return pts


def prominent_streaks(sequences):
    #Your algorithm goes here
    streaks = [] # Streaks

    # Compute the LPS streaks for each player
    # Add all the LPS streaks into one giant list
    # Do the skyline algorithm to calculate the final streaks
    
    lps_streaks = []
    for player, scores in sequences.items():
        LPS(scores, player, lps_streaks)
    
    skylines = Skyline(lps_streaks)

    for s in skylines:
        streaks.append(s.getData())

    return streaks
    #You have the freedom to define any other functions that you deem necessary. 
    
    
t0 = time.time()
sequences = readfiles()
t1 = time.time()
print("Reading the data file takes ", t1-t0, " seconds.")

t1 = time.time()
streaks = prominent_streaks(sequences)
t2 = time.time()
print("Computing prominent streaks takes ", t2-t1, " seconds.")
print(streaks)