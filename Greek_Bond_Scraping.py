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
    """
    
    def __init__(self):
        
        from bs4 import BeautifulSoup
        import pandas as pd
        import requests
        from datetime import date
        
        """Here we are requesting and getting the HTML code"""
        
        #####################################################################################
        #####################################################################################
        ########################### You may change links here. ##############################
        ############ You should change filename - check notification down ###################
        #####################################################################################
        #####################################################################################

        greek_bonds = requests.get("http://www.worldgovernmentbonds.com/country/greece/")
        soup = BeautifulSoup(greek_bonds.text, "html.parser")

        """Here we are capturing the table from the html"""

        tags = soup.find("table", class_ = "w3-table w3-white table-padding-custom w3-small font-family-arial table-valign-middle")

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

        """We are making a pd.DataFrame of from the values and now we are ready to append"""
        final_product = pd.concat([pd.Series(maturity), pd.Series(yields)], axis = 1)
        final_product.columns = ["Maturity", "Yields"]

        """ We are reforming the DataFrame so as for the daata to be ready to be appended in .csv"""
        final_product = final_product.transpose()
        final_product.columns = final_product.iloc[0]
        final_product = final_product.reset_index().drop(0).drop("index", axis = 1)

        """ Inserting today's values to data"""
        today = date.today()
        final_product["Date"] = today
        final_product = final_product.set_index("Date").reset_index()

        """Checking if the file exists and then proceed accordingly, to write, append or pass"""
        
        
        #############################################################################################
        #############################################################################################
        ##################### If you wish a different file, change filename here ####################
        #############################################################################################
        #############################################################################################
        
        
        file_name = "greek_worldgov.csv" 

        try:
            file = pd.read_csv(file_name)
            file = True
        except:
            file = None

        if file:
            
            """
            Before we proceed to update the file, we need to check if it is already updated.
            """
            
            file = pd.read_csv(file_name)
            if str(today) in file["Date"].values:
                print("File is up-to-date")
            else:
                final_product.to_csv(file_name , mode='a', index=False, header=False)
                print("File was updated")
        else:
            final_product.to_csv(file_name , mode='w', index=False, header=True)
            print("Bond Yield .csv was created") 


# In[ ]:


WorldGovBonds_Greece()

