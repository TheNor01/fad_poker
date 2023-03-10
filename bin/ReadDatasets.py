import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter
from numpy.random import seed
from numpy.random import randint
import random
import pickle

#10 predictive features 
# 
# SUIT  Ordinal:(1-4) representing {Hearts, Spades, Diamonds, Clubs} //picche
# Rank Numerical: (1-13) (Ace, 2, 3, ... , Queen, King)
# 1 output Goal: Ordinal (0-9)
"""
0: Nothing in hand; not a recognized poker hand 
      1: One pair; one pair of equal ranks within five cards // coppia
      2: Two pairs; two pairs of equal ranks within five cards // doppia coppia
      3: Three of a kind; three equal ranks within five cards //tris
      4: Straight; five cards, sequentially ranked with no gaps //scala
      5: Flush; five cards with the same suit //colore
      6: Full house; pair + different rank three of a kind // Full (tris + coppia)
      7: Four of a kind; four equal ranks within five cards (poker)
      8: Straight flush; straight + flush // scala colore
      9: Royal flush; {Ace, King, Queen, Jack, Ten} + flush // scala reale

      suit_name = {
        1: 'Cuori',
        2: 'Picche',
        3: 'Quadri',
        4: 'Fiori'
        }
"""

#Questions 
    #We can regroup features: S1,C1 --->
    #We can balance samples??? For instance adding more examples of less frequent classes?

    #What about discard 0 label rows

    #Order Column ascendent based on RANK?
#

def ReadDataset(path):
    features = np.array(['S1', 'R1','S2', 'R2','S3', 'R3','S4', 'R4','S5','R5','G'])
    columnsFeatures = pd.Series(features)
    trainingDataset = pd.read_csv(path,names=columnsFeatures)
    return trainingDataset

def CheckIntegrityDataset(dataset):
    print("Checking null or NAN values...")

    checkNan = dataset.isnull().values.any() #returns true if there is one true at least
    print(checkNan)

    print("\nChecking numerical value for every columns ... i = integer")
    checksNumerical = [(c, dataset[c].dtype.kind in 'i') for c in dataset.columns]
    print(checksNumerical)

    print("\nChecking range predictive (1,13) columns")
    checkRange1 = [(c, trainingDataset[c].between(1,13).values.any()) for c in trainingDataset.columns.delete(-1)]
    print(checkRange1) #removing goal

    print("\nChecking range goal (0,9) column")
    checkRange2 = trainingDataset["G"].between(0,9).values.any()
    print(checkRange2)



def PrintShapeGraph(dataset):
    print("SIZE OF : (Records,Features)")
    print(dataset.shape)

    g_classes = len(set(dataset['G'].values))  # count distinct values
    poker_hands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    hand_name = {
    0: 'Nothing in hand',
    1: 'One pair',
    2: 'Two pairs',
    3: 'Three of a kind',
    4: 'Straight',
    5: 'Flush',
    6: 'Full house',
    7: 'Four of a kind',
    8: 'Straight flush',
    9: 'Royal flush',
    }

    print(g_classes)
    cls = {}
    for i in range(g_classes):
        cls[i] = len(dataset[dataset.G==i])
    print(cls)

    #classes are unbalanced
    plt.bar(poker_hands, [cls[i] for i in poker_hands], align='center')
    plt.xlabel('classes id')
    plt.ylabel('Number of instances')
    plt.title("Classes of Dataset")
    plt.show()

def PlotCrossTab(trainingDataset):
    allS = []
    allR = []
    for col in trainingDataset.columns:
        #print(col)
        filteredCol = list(trainingDataset[col].values)
        if(str(col).startswith("S")):
            print("S",str(col))
            allS=allS+filteredCol
        elif(str(col).startswith("R")):
            print("R",str(col))
            allR=allR+filteredCol
        else:
            continue

    s = allS
    r = allR

    random.seed(10)
    #Incremental k sample
    # generate some integers
    kSample=4000
    indexes = random.sample(range(1, len(allS)), k=kSample)
    #print(indexes)
    subS  = [s[i] for i in indexes]
    subR  = [r[i] for i in indexes]

    #I don't make any difference but a R5 could be a R1 in terms of position
    dfHeat = pd.DataFrame()
    dfHeat["subS"] = subS
    dfHeat["subR"] = subR
    df2 = pd.crosstab(dfHeat['subS'], dfHeat['subR']).div(len(dfHeat))
    sns.heatmap(df2, annot=True)

    plt.xlabel('Ranks', fontsize=14)
    plt.ylabel('Suits', fontsize=14)
    plt.title("Cards occurrence")
    #plt.close()
    #plt.show()


def ApplyTrasformation(trainingDataset,typeOfDs):
        #listRank contains Ranks from ace to king
        #listSuits contains how many suits there are for any group
        #G label
        Allrows = []
        for index,rows in trainingDataset.iterrows():
            
            
            listRank=[0,0,0,0,0,0,0,0,0,0,0,0,0]
            listSuit=[0,0,0,0]
            listLabel=[0]


            for item in rows.items():
                KindOfCard = str(item[0])
                value = item[1]
                if(KindOfCard.startswith('S')):
                    value=value-1
                    listSuit[value] =  listSuit[value] + 1

                elif(KindOfCard.startswith('R')):
                    value=value-1
                    listRank[value] = 1
                else:
                    listLabel[0] = value


            tmpAggregator = listRank+listSuit+listLabel
            print(tmpAggregator)
            Allrows.append(tmpAggregator)
        print(len(Allrows))

        newColumns = ['Asso', 'Due', 'Tre', 'Quattro', 'Cinque', 'Sei', 'Sette', 'Otto'
                        ,'' 'Nove', 'Dieci', 'Principe','Regina','Re','rankCuori','rankPicche','rankQuadri','rankFiori','label']

        encodedDf = pd.DataFrame(Allrows, columns=newColumns)
        print(encodedDf)
        print(encodedDf.shape)
        
        with open("./bin/resources/"+typeOfDs+"_encodedDf.pickle", 'wb') as output:
            pickle.dump(encodedDf, output)
        return encodedDf

            
if __name__ == "__main__":
    trainingDataset = ReadDataset("./bin/resources/poker-hand-training-true.data")
    #fare in modo che se c'?? un false esce

    print("### TRAINING ###")
    CheckIntegrityDataset(trainingDataset)

    print(trainingDataset)

    #fare in modo che se c'?? un false esce
    CheckIntegrityDataset(trainingDataset)

    print("Dropping duplicates...")
    trainingDataset = trainingDataset.drop_duplicates()
    PrintShapeGraph(trainingDataset)


    print("\n\n### TESTING ###")
    testingDataset = ReadDataset("./bin/resources/poker-hand-testing.data")
    CheckIntegrityDataset(testingDataset)

    plt.close()
    PrintShapeGraph(testingDataset)


    #Linear transformation from 11D to 18D
    lsencodedDf = ApplyTrasformation(trainingDataset,"training")
    testing_encodedDf = ApplyTrasformation(trainingDataset,"testing")


    
    

    #print(trainingDataset[trainingDataset['G']==9])
    
    plt.close()
    PlotCrossTab(trainingDataset)

