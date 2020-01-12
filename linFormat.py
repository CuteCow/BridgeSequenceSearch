#!/usr/bin/env python3
# -*- coding: utf-8 -*-
  
import os
#import sys
import re
import pandas as pd

vuls = ['None', 'NS','EW', 'All'   \
        ,'NS', 'EW','All', 'None'  \
        ,'EW', 'None','All', 'NS'  \
        ,'All', 'None','NS', 'EW'  \
        , 'None', 'NS','EW', 'All' \
        ,'NS', 'EW','All', 'None'  \
        ,'EW', 'None','All', 'NS'  \
        ,'All', 'None','NS', 'EW' ]

path = 'C:\\Users\\james\\Dropbox\\Python Scripts\\Brink'

df = pd.DataFrame(columns=['p1', 'p2', 'p3', 'p4' \
                           , 'room','deal', 'dealer', 'vul' \
                           , 'direction', 'bidding', 'bidding1', 'bd_open' \
                           , 'ns', 'nh', 'nd', 'nc' \
                           , 'es', 'eh', 'ed', 'ec' \
                           , 'ss', 'sh', 'sd', 'sc' \
                           , 'ws', 'wh', 'wd', 'wc'
                           , 'file' ])

for file in os.listdir(path):
    if file[-4:] == '.lin':
        current = os.path.join(path, file)
        
        if os.path.isfile(current):
            # Open file
            data = open(current, "rb")
            # extract hands in .lin format
            contents = str(data.read(), 'utf-8')
            data.close()
            
            # Strip out annoying commentator comments
            contents = re.sub("nt\|.*?\|?pg\|", '', contents)
            
            # Remove \r\n
            contents = re.sub("\\r\\n?", '', contents)
            #print(contents)
            
            # Extract players - name order starts with south in open room
            p = re.compile("pn\|((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])((.*?)[,\|])")
            result = p.search(contents)
            
            names = []
            names.append(result.group(2));   names.append(result.group(4))
            names.append(result.group(6));   names.append(result.group(8))
            names.append(result.group(10));  names.append(result.group(12))
            names.append(result.group(14));  names.append(result.group(16))
            #print(names)
            
            # Find if Brink-Drijver playing in open/closed and NS/EW
            for count in range(0,7):
                #print(names[count])
                if  (names[count].lower() == 'brink'):
                    index = count
            # Are B/D in the open or closed room?
            if index < 4:
                room = 'open room'
            else:
                room = 'closed room'
            # NS / EW
            if index%2 == 0:
                direction = 'NS'
            else:
                direction = 'EW'
            #print(room, direction)
            
            if room == 'open room':
                p1 = names[0]; p2 = names[1]; p3 = names[2]; p4 = names[3]
            else:
                p1 = names[4]; p2 = names[5]; p3 = names[6]; p4 = names[7]
            
            # carve up the file into hand chunks from the room of interest
            hand_chunks = contents.split('qx|')
            for chunk in hand_chunks:
                if chunk[0] == room[0]:
                    #print(chunk)
                    # Extract cards from hand details
                    search_re = room[0] + '(\d+)\|st\|\|md\|(\d*)(S([2-9TJQKA]*)H([2-9TJQKA]*)D([2-9TJQKA]*)C([2-9TJQKA]*)[,\|]?)(S([2-9TJQKA]*)H([2-9TJQKA]*)D([2-9TJQKA]*)C([2-9TJQKA]*)[,\|]?)(S([2-9TJQKA]*)H([2-9TJQKA]*)D([2-9TJQKA]*)C([2-9TJQKA]*)[,\|]?)(S([2-9TJQKA]*)H([2-9TJQKA]*)D([2-9TJQKA]*)C([2-9TJQKA]*)[,\|]?)'
                    p = re.compile(search_re)
                    result = p.search(chunk)
                    
                    deal_num = result.group(1)
                    # Dealer: 1 = South, 2 = West, 3 = North, 4 = East
                    dealer = result.group(2)
                    vul = vuls[int(deal_num)%32 - 1]
                    # south spades            south hearts
                    ss = result.group(4);     sh = result.group(5)
                    sd = result.group(6);     sc = result.group(7)
                    # west
                    ws = result.group(9);     wh = result.group(10)
                    wd = result.group(11);    wc = result.group(12)
                    # north
                    ns = result.group(14);    nh = result.group(15)
                    nd = result.group(16);    nc = result.group(17)
                    # east
                    es = result.group(19);    eh = result.group(20)
                    ed = result.group(21);    ec = result.group(22)
                    #print(ns);        print(nh);        print(nd);        print(nc)
                    #print(ws);        print(wh);        print(wd);        print(wc)
                    #print()
                    
                    # Extract raw bidding then split into bids
                    #chunk = re.sub('|+', '|', chunk)
                    
                    # Remove alerts and alerting information
                    chunk = re.sub('an\|.+?\|', '', chunk)
                    chunk = re.sub('\!', '', chunk)
                    
                    # Extract bidding
                    p = re.compile("sv\|\w(\|+mb\|+(.+?))\|+mb\|+p\|+mb\|+p\|+mb\|+p\|+")
                    result = p.search(chunk)
                    #print(chunk)
                    bidding_raw = result.group(2)
                    bidding_raw = re.sub('\|+', '|', bidding_raw)
                    bids = bidding_raw.split('|mb|')
                    bid_seq = ''.join(bids)
                    bid_seq = bid_seq.replace('|', '')
                    bid_seq1 = ' '.join(bids)
                    bid_seq1 = bid_seq1.replace('|', '')
                    
                    # Find 1st call 
                    # i.e. the position of the opener relative to the dealer
                    opener = 0
                    found = False
                    if len(bids) > 1:
                        while found == False:
                            if bids[opener] != 'p':
                                found = True
                            else:
                                opener += 1
            
                    # Use BD_Opened to flag if Brink-Drijver opened the bidding 
                    # Handy for searching bidding sqquences 
                    bd_opened = False
                    if ((opener + int(dealer))%2 == 1 and direction == 'NS'):
                        bd_opened = True
                        #print(deal_num, 1)
                        
                    if ((opener + int(dealer))%2 == 0 and direction == 'EW'):
                        bd_opened = True
                        #print(deal_num, 2)
            
                    # print(bd_opened)
                    
                    # Add hand to dataframe
                    df.loc[len(df) + 1] = [p1, p2, p3, p4 \
                               , room, deal_num, dealer, vul \
                               , direction, bid_seq, bid_seq1, bd_opened \
                               , ns, nh, nd, nc \
                               , es, eh, ed, ec \
                               , ss, sh, sd, sc \
                               , ws, wh, wd, wc \
                               , file ]
                    

df.to_pickle(path + '\\brink.pkl')
print('Finished\n')