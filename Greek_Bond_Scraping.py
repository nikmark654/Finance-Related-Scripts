#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class WorldGovBonds_Greece:
    
    """
    __init__ webscraps and updates daily Greek bond yields. Just run(call) it.
        
        Dependencies:
        * bs4.BeatifulSoup
        * pandas
        * requests
        * datetime.date
        
        Algorithm's Steps:

        __init__(self):
        
        [1st step] Request info from url (You may change url here)
        [2nd step] Check if the .csv exists and check if data is up-to-date.    
                                (Here you may change file name, 
                                if you've changed url)
                                
            [2.1]   If file exists, check if the date of last update on website 
                    exists in the file
                
                [2.1.1] If date exists, print("The file is up-to-date")
                
                [2.1.2] If it does not exist, run The_Processing method, update 
                        the file and print("File was updated")
            
            [2.2] If file does not exist - run The_Processing method & create the file

        The_Processing(self, tags, date):
        
        [1st Step]  Capture the date and do some cleaning. We also assign the 
                    bond maturity to var Maturity & yield to var Yield.
        [2nd Step]  Create the DataFrame and do some forming. Create self.final_product 
                    attribute that we will use in __init__(self) to create/update the .csv
                    
                    
    
    """
    
    def __init__(self):
        
        from bs4 import BeautifulSoup
        import pandas as pd
        import requests
        from datetime import date
        
        #                  #
        ##### 1st Step #####
        #                  #
        
        
        """ Here we are requesting the website code and capture the table & update date. """
        
        """
        You may change links here.
        If You do so, you should change filename as well.
        check notification down 
        """
        
        greek_bonds = requests.get("http://www.worldgovernmentbonds.com/country/greece/")   # Change here #
        soup = BeautifulSoup(greek_bonds.text, "html.parser")

        """Here we are capturing the table from the html"""

        tags = soup.find("table", class_ = "w3-table w3-white table-padding-custom w3-small font-family-arial table-valign-middle")
        
        """ before anything else, lets capture last update date"""
        
        xtra_tags = soup.find(class_="w3-tiny w3-text-gray")
        date =  xtra_tags.text.strip()[13:24]
        
        
        #                  #
        ##### 2nd Step #####    Checking if the file exists and then proceed accordingly, to write, append or pass   # 
        #                  #
        
        """ If you wish a different file, change filename here """

        file_name = "greek_worldgov.csv"   # Change Here #
        
        """ Now, let's check if file is up-to-date"""
        try:
            file = pd.read_csv(file_name)
            file = True
        except:
            file = None
        
        if file:   #           #   
                   ### [2.1] ###    """ The file exists """
                   #           #
            
            file = pd.read_csv(file_name)
            
            if str(date) in file["Date"].values:       #              #
                print("File is up-to-date")            ###  [2.1.1] ###    """The file is up-to-date"""
                                                       #              #
            else:
                self.The_Processing(tags, date)                                              #              #  """ The file
                self.final_product.to_csv(file_name , mode='a', index=False, header=False)   ###  [2.1.2] ###      is not
                print("File was updated")                                                    #              #      up-to-date """
        
        else:   #           #
                ### [2.2] ###    """ The file does not exist """
                #           #
            self.The_Processing(tags, date)
            self.final_product.to_csv(file_name , mode='w', index=False, header=True)
            print("Bond Yield .csv was created") 
            
    
    
    def The_Processing(self, tags, date):
        
        import pandas as pd
        
        #                  #
        ##### 1st Step #####
        #                  #
        
        """Here we capture the data of the table"""

        tbody = tags.find_all("td")

        """Now we are capture the bond maturity, yield and price. For reasons, we do not do .text.strip() and we get [] as well"""

        lists_of_yields = []
        for i in tbody:
            lists_of_yields.append(i.find_all("b"))

        """Now we are cleaning []"""

        actual_list = []
        for i in lists_of_yields:
            if i:
                actual_list.append(i)

        """And now we are getting only the values/text"""
        bonds = []
        for i in actual_list:
            bonds.append(i[0].text)

        """We categorize the values in maturity values and yield values"""

        maturity = []
        yields = []
        for i in bonds:
            if "month" in i or "year" in i:
                maturity.append(i)
            elif "%" in i:
                yields.append(i)
        
        #                  #
        ##### 2nd Step #####
        #                  #
        
        """We are making a pd.DataFrame of from the values and now we are ready to append"""
        final_product = pd.concat([pd.Series(maturity), pd.Series(yields)], axis = 1)
        final_product.columns = ["Maturity", "Yields"]

        """ We are reforming the DataFrame so as for the daata to be ready to be appended in .csv"""
        final_product = final_product.transpose()
        final_product.columns = final_product.iloc[0]
        final_product = final_product.reset_index().drop(0).drop("index", axis = 1)

        """ Inserting today's values to data"""
        final_product["Date"] = date
        self.final_product = final_product.set_index("Date").reset_index()
                


# In[ ]:


WorldGovBonds_Greece()


# In[ ]:




