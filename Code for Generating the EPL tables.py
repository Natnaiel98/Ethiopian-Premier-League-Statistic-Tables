# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 14:08:45 2021

@author: natem
"""
#dict containing all of our league tables, keep it out  of the loop to keep memory global
EPL={}

#We should try to do this from wikipedia
#Links to all the pages we want to turn into a table(In order)

Links=['https://en.wikipedia.org/wiki/2009–10_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2010–11_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2011–12_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2012–13_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2013–14_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2014–15_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2015–16_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2016–17_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2017–18_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2018–19_Ethiopian_Premier_League','https://en.wikipedia.org/wiki/2020–21_Ethiopian_Premier_League']    
for i in range(len(Links)):    
    
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page=Links[i]
    pageTree = requests.get(page, headers=headers)
    #parses the collected html data
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    #retrieves all lines of the table
    My_table = pageSoup.find("table",{"class":"wikitable"})        


    #Convert the HTML code into a dataframe
    df=pd.read_html(str(My_table))
    # convert list to dataframe
    
    EPL["keys%s" %i]= pd.DataFrame(df[0])
 
    

#Epl is dictionary with all the tables
#We can concat all into one table:

AllTab=[]
for i in range(len(Links)):
     AllTab.append(EPL["keys%s" %i] )

#before that, add season to each table, will prove useful for later analysis
seasons=['2009/10','2010/11','2011/12','2012/13','2013/14','2014/15','2015/16','2016/17','2017/18','2018/19','2020/21']

for i in range(len(seasons)):
    AllTab[i]['Season']=seasons[i]
dff=pd.concat(AllTab,ignore_index=True)


#The points metric is biased in favor of teams that have stayed in the league  the longest 
# create a new variable for the data frame entitled 'PPG'(Points per game) to remedy this
dff['PPG']=dff['Pts']/dff['Pld']

# Next steps:
#table Normalization, cumulative table
ee=dff
#NORMALIZATION(All the different names used for a team need to be standardized)

for i in range(len(ee['Team'])):
    if ('George') in ee['Team'][i] or ('Kedus') in ee['Team'][i] :
        ee['Team'][i]='Kidus Giorgis'
    elif ('Adama') in ee['Team'][i]:
        ee['Team'][i]='Adama Kenema'
    elif ('Arba Minch') in ee['Team'][i]:
        ee['Team'][i]='Arba Minch Kenema'
    elif ('Awassa') in ee['Team'][i] or ('Hawassa') in ee['Team'][i]:
        ee['Team'][i]='Hawassa Kenema'
    elif ('Dire Dawa') in ee['Team'][i]:
        ee['Team'][i]='Dire Dawa Kenema'  
    elif ('Dashen') in ee['Team'][i]:
        ee['Team'][i]='Dashen Bira'     
    elif ('Dedebit') in ee['Team'][i]:
        ee['Team'][i]='Dedebit'     
    elif ('Ethiopian Coffee') in ee['Team'][i] or ('Ethiopia Bunna') in ee['Team'][i]:
        ee['Team'][i]='Ethiopia Bunna'
    elif ('Bank') in ee['Team'][i]:
        ee['Team'][i]='CBA'
    elif ('Harar' ) in ee['Team'][i] or ('Harrar')in ee['Team'][i]:
        ee['Team'][i]='Harar Bira'
    elif ('Fasil') in ee['Team'][i]:
        ee['Team'][i]='Fasil Kenema'
    elif ('Hossana') in ee['Team'][i]:
        ee['Team'][i]='Hadiya Hossana'
    elif ('Mebrat') in ee['Team'][i]:
        ee['Team'][i]='EEPCO'     
    elif ('Insurance') in ee['Team'][i]:
        ee['Team'][i]='Ethiopian Insurance'     
    elif ('Defence') in ee['Team'][i]:
        ee['Team'][i]='Mekelakeya'     
    elif ('Sidama') in ee['Team'][i]:
        ee['Team'][i]='Sidama Bunna'
    elif ('Dicha') in ee['Team'][i]:
        ee['Team'][i]='Wolayta Dicha'
    elif ('Woldya') in ee['Team'][i] or ('Woldia') in ee['Team'][i]:
        ee['Team'][i]='Woldia Kenema'     
    elif ('Muger' ) in ee['Team'][i] or ('Mugher') in ee['Team'][i]:
        ee['Team'][i]='Muger Cemento'    
    elif ('Mekelle') in ee['Team'][i]:
        ee['Team'][i]='Mekelle Kenema'
    elif ('Sebeta') in ee['Team'][i]:
        ee['Team'][i]='Sebeta Kenema'
    elif ('Southern' ) in ee['Team'][i] or ('Debub')in ee['Team'][i]:
        ee['Team'][i]='Debub Police'

#Creating a table with all iteration of teams that have played in the 
#Ethiopian Premier league since 2009/10 (same clubs from different seasons are included)
tottable=ee 
tottable['index']
tottable=tottable.sort_values('PPG',ascending=False)
#tottable=tottable.reset_index() 
#fixing new positions for the clubs 
tottable['Pos']=range(1,166)

#export this table
tottable.to_csv('All_Time_EPL_Table.csv',index=False,header=True)



#cumulative table for the period of 2009-2021
CuEPL=ee.groupby('Team').agg({'Pld':'sum','W':'sum','D':'sum','L':'sum','GF':'sum','GA':'sum','Pts':'sum'})
#Add new relevant stats
CuEPL['PPG']=CuEPL['Pts']/CuEPL['Pld']
CuEPL['GF90']=CuEPL['GF']/CuEPL['Pld']
CuEPL['GA90']=CuEPL['GA']/CuEPL['Pld']
CuEPL['GD90']=CuEPL['GF90']-CuEPL['GA90']
CuEPL=CuEPL.sort_values('PPG', ascending=False)
#sort by point total
CuEPL.insert(0,'Pos',range(1,37))
#export this table
tottable.to_csv('Cumulative_EPL_Table.csv',index=False,header=True)


