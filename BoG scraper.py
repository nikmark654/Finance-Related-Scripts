#!/usr/bin/env python
# coding: utf-8

class BoG_scrapper:
    
    """
    A class for a quick CSV file creation, with Greek Bond yields data from Bank of Greece.
    
    In the initial call, the first file will be created.

    Takes no argument.
    
    Dependencies:
        * BeatifulSoup
        * pandas
        * requests
        * os
        
    ****** Work to do: ******
        
        # Need to make that a start-up app, so it will update each day the data.
        
    """
    def constant(self):
        
        """
        This method is a set of processes that are common for both first time & update.
        """
        
        from bs4 import BeautifulSoup
        import pandas as pd
        import requests

        ### Importing greek bond html and scrapping yield, price and date infos ###

        greek_bonds = requests.get("https://www.bankofgreece.gr/statistika/xrhmatopistwtikes-agores/titloi-ellhnikoy-dhmosioy").text #accessing and scrapping the page of BoG
        soup = BeautifulSoup(greek_bonds, "lxml")   # BeautifulSoup instance 
        tags = soup.find_all("tr")                  #Finding all the "tr" which hold the values of the matrix

        ### DataFraming html data ###

        # Texting list elements
        text_list = []
        for i in tags:
            text_list.append(i.text.split())

        # Droping "tr" titles
        self.pre_df = pd.Series(text_list[3:]).drop([32, 41, 42, 43])
        
        # Creating bond categories
        self.bonds = self.pre_df[0]
        for i in range(len(self.bonds)):
            self.bonds[i] = self.bonds[i]+" years"

        # Creating columns
        self.columns = self.pre_df[1]

        # Removing (%) from columns list
        while "(%)" in self.columns:
            self.columns.remove("(%)")
    
    def first_time(self):
        
        """
        Method only for the first time.
        """
        
        self.constant()
        
        import pandas as pd

        # Creating dataframe index  
        dates = []
        for i in self.pre_df[2:32]:     # [2:32 are ok]
            dates.append(i[0])

        for i in self.pre_df[32:]:      # [32:] needed to correct date elements.
            dates.append(i[0] + " " + i[1])

        # Creating values matrix for the dataframe
        values = []
        for i in self.pre_df[2:32]:     # [2:32 are ok]
            values.append(i[1:])

        for i in self.pre_df[32:]:      # [32:] needed to append from [2:] instead from [1:] as previously.
            values.append(i[2:])

        # Finaly, DataFraming the whole thing
        Greek = pd.DataFrame(index = dates, columns = self.columns[3:], data = values)
        Greek = Greek.drop("Τιμή", axis = 1)                   # Droping "Τιμή" column.
        Greek.columns = self.bonds

        # Converting values to float:
        Greek.replace(",", ".", regex = True, inplace = True)  # Values are in Greek float forms. 
        Greek = Greek.astype("float64")

        # Correcting the DataFrame's index
        Greek.reset_index(inplace = True)
        Greek.sort_index(ascending= False, inplace = True)
        Greek.rename(columns = {Greek.columns[0] : "Date"}, inplace = True)
        Greek.set_index("Date", inplace = True)

        # Saving csv file.
        Greek.to_csv("greek_bonds.csv")

        print("Greek bond yields have been added to a new CSV file")
        
        del self


    def regular_t(self):
        
        """
        Method for each update.
        """
        
        self.constant()
        
        import pandas as pd
        
        # Creating dataframe index  
        dates = []
        for i in self.pre_df[2:32]:     # [2:32 are ok]
            dates.append(i[0])

        # Loading CSV file and checking which dates exist already inside the file.
        csv_data = pd.read_csv("greek_bonds.csv")
        indexer = []
        for i in range(len(dates)):
            indexer.append(dates[i] not in csv_data["Date"].values)


        # Creating values matrix for the dataframe
        values = []
        for i in self.pre_df[2:32][indexer]:     # [2:32 are ok]
            if i != None:
                values.append(i[1:])

        # Since dates is the gross list, we need to grab only those dates that are actually new. 
        # Otherwise, we will have problem with DataFrame
        correct_dates = []
        for i in range(len(indexer)):
            if indexer[i]:
                correct_dates.append(dates[i])

        ##### Forming DataFrame #####
        # Finaly, DataFraming the whole thing
        Greek = pd.DataFrame(index = correct_dates, columns = self.columns[3:], data = values)   # Values & Dates are of the new
        Greek = Greek.drop("Τιμή", axis = 1)                                                # Droping "Τιμή" column.
        Greek.columns = self.bonds

        # Converting values to float:
        Greek.replace(",", ".", regex = True, inplace = True)  # Values are in Greek float forms. 
        Greek = Greek.astype("float64")

        # Correcting the DataFrame's index
        Greek.reset_index(inplace = True)
        Greek.sort_index(ascending= False, inplace = True)
        Greek.rename(columns = {Greek.columns[0] : "Date"}, inplace = True)
        Greek.dropna(inplace = True)

        # Appending CSV file
        Greek.to_csv('greek_bonds.csv', mode='a', index=False, header=False)
        
        print("CSV file has been updated")
        
        del self
            
    def __init__(self):
        
        """
        Automating things method.
        """
        import os
        if os.path.isfile("greek_bonds.csv"):
            self.regular_t()
        else:
            self.first_time()


BoG_scrapper()