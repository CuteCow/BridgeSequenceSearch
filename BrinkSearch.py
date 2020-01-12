# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 19:06:31 2019

@author: james
"""
import pandas as pd
import pandasql as ps
import sys
import webbrowser

path = 'C:\\Users\\james\\Dropbox\\Python Scripts\\Brink\\brink.pkl'
url  = 'C:\\Users\\james\\Dropbox\\Python Scripts\\Brink\\brink.htm'

seat = ' SWNE'

# Read in dataframe
df = pd.read_pickle(path)

# SQL queries
#q1 = """SELECT * FROM df where bd_open ='1' AND BIDDING like '1H%' order by file desc"""
#q1 = """SELECT * FROM df where bd_open ='1' 
#            AND ((direction = 'NS' AND vul = 'EW')
#                OR (direction = 'EW' AND vul = 'NS'))
#            AND BIDDING like 'p1N%' order by file desc"""
q1 = """SELECT * FROM df where bd_open ='1' 
            AND ((direction = 'NS' AND vul = 'EW')
                OR (direction = 'EW' AND vul = 'NS'))
            AND BIDDING like '1Cp1S%' order by file desc"""

# Execute
my_res = ps.sqldf(q1, locals())

# Redirect output to file
original = sys.stdout
sys.stdout = open(url, 'w', encoding="utf-8")

# Format matching hands
print('<pre><code>')
print(str(len(my_res)) + ' results')
for index, row in my_res.iterrows():
    
    print(' Board:  ' + row['deal'] + 10*' ' + row['file'])
    print(' Vul:    ' + row['vul'])
    print(' Dealer: ' + (seat[int(row['dealer'])]))
    if row['dealer'] == '3':
        print(6*' ' + '<em style="color: red;">' + row['p1'] + '</em>')
    else :
        print(6*' ' + row['p1'])
    print(6*' ' + '\u2660 ' + row['ns'])
    print(6*' ' + '\u2661 ' + row['nh'])
    print(6*' ' + '\u2662 ' + row['nd'])
    print(6*' ' + '\u2663 ' + row['nc'])
    print()
    if row['dealer'] == '2':
        print('<em style="color: red;">' + row['p2'] + '</em>' + (12 - len(row['p2']))*' ' + row['p4'])
    elif row['dealer'] == '4':
        print(row['p2'] + (12 - len(row['p2']))*' ' + '<em style="color: red;">' + row['p4'] + '</em>')
    else :
        print(row['p2'] + (12 - len(row['p2']))*' ' + row['p4'])
    print('\u2660 ' + row['ws'] + (10 - len(row['ws']))*' ' + '\u2660 ' + row['es'])
    print('\u2661 ' + row['wh'] + (10 - len(row['wh']))*' ' + '\u2661 ' + row['eh'])
    print('\u2662 ' + row['wd'] + (10 - len(row['wd']))*' ' + '\u2662 ' + row['ed'])
    print('\u2663 ' + row['wc'] + (10 - len(row['wc']))*' ' + '\u2663 ' + row['ec'])
    print('')
    if row['dealer'] == '1':
        print(6*' ' + '<em style="color: red;">' + row['p3'] + '</em>' )
    else :
        print(6*' ' + row['p3'])
    print(6*' ' + '\u2660 ' + row['ss'])
    print(6*' ' + '\u2661 ' + row['sh'])
    print(6*' ' + '\u2662 ' + row['sd'])
    print(6*' ' + '\u2663 ' + row['sc'])

    if row['dealer'] == '1':
        print('S    W    N    E')
    if row['dealer'] == '2':
        print('W    N    E    S')
    if row['dealer'] == '3':
        print('N    E    S    W')
    if row['dealer'] == '4':
        print('W    S    W    N')

    bid_list = row['bidding1'].split(' ')
    bid_len = len(bid_list)
    count = 0

    while count < bid_len :
        print(bid_list[count] + (5 - len(bid_list[count]))*' ', end = '')
        if (count+1)%4 == 0:
            print()
        count = count + 1
                
    print('\n----------------------------------')

print('<\code><\pre>')
sys.stdout = original

webbrowser.open('file://' + url, new=2)

def hcp(row):
    list(row)[12:28]
