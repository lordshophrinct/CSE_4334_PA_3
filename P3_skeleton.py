import pandas as pd
import time

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
    #You algorithm goes here
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
