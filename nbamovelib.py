import requests
import pickle
import numpy as np
import matplotlib.pyplot as plt
import hmmlearn
from scipy.misc import imread
import math
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

def testLib():
    print "hello test lib"

def getBallData(GameID,EventID):
    strs='http://stats.nba.com/stats/locations_getmoments?GameID=%s&EventID=%d'%(GameID,EventID)
    raw_data=requests.get(strs)
    print raw_data.status_code
    move_data=raw_data.json()['moments']
    print len(move_data)
    ball_moves=[]
    for i in move_data:
        ball_moves.append(i[5][0])
    ballmoves=[[a[2],a[3],a[4]] for a in ball_moves]
    if(ballmoves is not None):
        return ballmoves
    else:
        return[]
    
def getShotDifficulty(mshotspossible,menc,mclf):
    last=0
    ret=[]
    for i in mshotspossible:
        if i[0] is not 0:
            stuff=menc.transform([i[0],i[2]]).toarray()[0].tolist()
            stuff.extend([i[1],i[3],i[4]])
            ans=mclf.predict_proba(stuff)
            last=(ans[0][0]*10)
            ret.append(last)
        else:
            ret.append(last)
    return ret
    
def distance(p1,p2):
    dist=math.sqrt(math.pow((p1[0]-p2[0]),2)+math.pow((p1[1]-p2[1]),2))
    #print dist
    return dist
    
def getRawData(GameID,EventID):
     strs='http://stats.nba.com/stats/locations_getmoments?GameID=%s&EventID=%d'%(GameID,EventID)
     raw_data=requests.get(strs)
     print raw_data.status_code
     move=raw_data.json()['moments']
     visitor=raw_data.json()['visitor']['players']
     home=raw_data.json()['home']['players']
     numbers=[]
     for i in move[0][5]:
        numbers.append(i[1])
     print numbers   
     returner=[move,home,visitor,numbers]
     return returner

def prepareBallData(ballData):
    x= np.array([a[0] for a in ballData])
    y= np.array([a[1] for a in ballData])
    x=x*10
    y=y*10
    return x,y