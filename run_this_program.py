import requests
from bs4 import BeautifulSoup
import gpt_functions as gpt
from text_cleaner import truncate_text 
import web_scraper as scrape
import time
import pandas as pd
import sys
import math

#initialise websites list
websites = []
loop = True

"""remove_nan_from_end removes nan values from the end of a list"""
def remove_nan_from_end(lst):
    reversed_lst = list(reversed(lst))
    result = []
    found_non_nan = False

    for item in reversed_lst:
        try:
            if math.isnan(item) and not found_non_nan:
                continue
        except TypeError:
            pass
        found_non_nan = True
        result.append(item)

    return list(reversed(result))

"""recover_descriptions is used to recover the descriptions and bad urls generated this session"""
def recover_descriptions():
    padding_length = len(my_csv) - len(long_desc_col)
    padded_values = long_desc_col + [''] * padding_length
    my_csv['Long Description'] = padded_values

    padding_length = len(my_csv) - len(short_desc_col)
    padded_values = short_desc_col + [''] * padding_length
    my_csv['Short Description'] = padded_values

    padding_length = len(my_csv) - len(shortest_desc_col)
    padded_values = shortest_desc_col + [''] * padding_length
    my_csv['Rollover Description'] = padded_values

    my_csv.to_csv(filename, index=False)
    all_denied_urls_csv = pd.DataFrame({'Denied URLs': all_denied_urls})
    all_denied_urls_csv.to_csv("denied_urls.csv", index=False)
    print("Descriptions recovered successfully.")

"""save_descriptions writes the generated descriptions to the csv file"""
def save_descriptions():
    padding_length = len(my_csv) - len(long_desc_col)
    padded_values = long_desc_col + [''] * padding_length
    my_csv['Long Description'] = padded_values

    padding_length = len(my_csv) - len(short_desc_col)
    padded_values = short_desc_col + [''] * padding_length
    my_csv['Short Description'] = padded_values

    padding_length = len(my_csv) - len(shortest_desc_col)
    padded_values = shortest_desc_col + [''] * padding_length
    my_csv['Rollover Description'] = padded_values
    my_csv.to_csv(filename, index=False)

#Collect the csv file name to read/ write to via user input.
while (loop == True):
    print("Please input the name of your CSV file:")
    filename = input("")
    try:
        my_csv = pd.read_csv(filename)
        loop = False
    except:
        print("Error: Failed to read file. Please note:")
        print("-The file should be a .csv file in the same directory as this program.")
        print("-Your input should not be enclosed in quotation marks.")
        print("-You should include the .csv extension at the end of your file name.")
        print()

#check for existing descriptions
last_valid_index = my_csv['Rollover Description'].last_valid_index()

#if there are none, then we can start fresh
if last_valid_index is None:
    start_index = 0
    #initialise the lists of descriptions as empty
    long_desc_col = []
    short_desc_col = []
    shortest_desc_col = []
else: #if there are existing descriptions already
    start_index = my_csv['Rollover Description'].last_valid_index() + 1
    #remove nan values from the ends of the description columns
    #and turn the results into lists
    long_desc_col = remove_nan_from_end(my_csv['Long Description'].tolist())
    short_desc_col = remove_nan_from_end(my_csv['Short Description'].tolist())
    shortest_desc_col = remove_nan_from_end(my_csv['Rollover Description'].tolist())

#list of urls will begin where we left off last time,
#if this is a new file it'll start at the beginning
websites = my_csv['Tool URL'][start_index:].tolist()

"""The following code handles the description generation and the writing
of the csv files"""
#Initialise variables for time elapsed
length = len(websites)
iterator = 0
overall_start = time.perf_counter()

#initialise list of denied URLS
denied_urls_csv = pd.read_csv("denied_urls.csv")
all_denied_urls = denied_urls_csv["Denied URLs"].tolist()

#If GPT response contains these, it means it can't generate a description.
bad_phrases = ["I'm sorry", "I apologize", "JavaScript"] 
    
#Iterate through the list of websites and generate 3 descriptions per URL 
for website in websites:
    print("Accessing", website, "...")
    print()
    start = time.perf_counter() #start the timer for this iteration
    
    try:
        #attempt to scrape the website for text
        page_text = scrape.extract_website_info(website)
        
    except:
        iterator += 1
        all_denied_urls.append(website)#add URL to list of denied urls
        all_denied_urls_csv = pd.DataFrame({'Denied URLs': all_denied_urls})
        all_denied_urls_csv.to_csv("denied_urls.csv", index=False)
        long_desc_col.append("") #add blanks to the description lists
        short_desc_col.append("")
        shortest_desc_col.append("")
        save_descriptions()
        print("Unable to generate description. Website added to denied_urls.csv.")
        print(">>>>>>>>>", iterator, " out of ", length, " websites complete.")
        print()
        continue
    
    #shorten to 600 words to avoid token limit
    page_text = truncate_text(page_text) 

    #Ask GPT for descriptions of the resource
    try:
        long_desc = gpt.long_describe(page_text)
        short_desc = gpt.short_describe(page_text)
        shortest_desc = gpt.link_describe(page_text)
        
    #If the rate limit has been exceeded, stop executing.
    except Exception as e:
        print(f"Error: {str(e)}") 
        print()                   
        recover_descriptions()    
        print("Process exited. You may now close the program.")
        sys.exit()
        
    iterator += 1
    end = time.perf_counter() #end the timer for this iteration
    elapsed = round(end - start)
    if (not gpt.paid_account) and elapsed < 62:
        naptime = 62 - elapsed #calculate time to back off for
    else:
        naptime = False

    #Detect websites that are down or cannot be scraped/ described.
    found_phrases = False
    for phrase in bad_phrases:
        if phrase in long_desc or phrase in short_desc or phrase in shortest_desc:
            found_phrases = True
            break

    if "github.com" in website: #GPT struggles to describe scraped github pages accurately
            found_phrases = True
            
    if found_phrases:
        #add URL to list of denied urls
        all_denied_urls.append(website)
        all_denied_urls_csv = pd.DataFrame({'Denied URLs': all_denied_urls})
        all_denied_urls_csv.to_csv("denied_urls.csv", index=False)
        
        long_desc_col.append("") #add blanks to the description lists
        short_desc_col.append("")
        shortest_desc_col.append("")
        save_descriptions()
        print("Unable to generate description. URL added to denied_urls.csv.")
    else:
        long_desc_col.append(long_desc) #else add descriptions to lists
        short_desc_col.append(short_desc)
        shortest_desc_col.append(shortest_desc)
        print("********LONG DESCRIPTION********")
        print(long_desc)
        print("********SHORT DESCRIPTION********")
        print(short_desc)
        print("********ROLLOVER DESCRIPTION********")
        print(shortest_desc)
        print()
        save_descriptions()
        print("Descriptions saved to", filename)
        
    print(">>>>>>>>>", iterator, " out of", length, "websites complete.")
    print("Time elapsed:", elapsed, "seconds.")
    #Rate limit is 3 requests per min, so we need to back off until a minute has elapsed
    if (iterator < length) and naptime:
        print("Cooling off for", naptime, "seconds...")
        time.sleep(naptime)
        print()
        
        
overall_end = time.perf_counter() #stop the timer
overall_elapsed = overall_end - overall_start   #calculate overall time elapsed
print()
print("Process complete. Total time elapsed:", overall_elapsed, "seconds.")
#Hooray!

print("You may now close the program.")
