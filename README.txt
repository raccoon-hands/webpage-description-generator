***************QUICK START GUIDE********************

1. This program requires the following to be installed:
Python 3.11 & Python IDLE (or any code editor with an interactive shell)
pandas - pip install pandas
Beautiful Soup - pip install beautifulsoup4
Python bindings for OpenAI API access - pip install openai
requests - pip install requests

---------------------------------------------------------------------------------------------------------
2. To get your secret API key, go to: https://platform.openai.com/
You'll need to create an account or log in.
Click on "Personal" (top right corner), then select "View API Keys" from the menu.

You can create a key which you can only view once, so copy and paste it somewhere straight away.
--------------------------------------------------------------------------------------------------------
3. To use the key, the program assumes you have stored your API key in a user environment variable 'OPENAI_API_KEY'.
If you don't want to or can't do this then you can edit gpt_functions.py, line 6 to be the following:

openai.api_key = 'your key here'

But this is not recommended for security reasons, and you should keep your files confidential if you choose to
do it this way.

Tutorials on creating an environment variable for your key:
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

Please note: You will need to restart IDLE or whatever editor you are using for the environment variable change
to be picked up by python.

IMPORTANT: You will need to select what type of account you use by changing the paid_account variable
in gpt_functions.py. This will afect the rate limit and the program may not function if this variable
is not set appropriately. If your account is paid, set it as True. If it's a free account, set it 
to False. If you are in your free trial period, results may vary depending on your internet speed, so experiment
with either.
--------------------------------------------------------------------------------------------------------

4. Place the .csv file you want to parse in the same directory as the .py files.
   If the file is an excel file, you will need to export it as a csv.
   The csv file must contain the column "Tool URL" which contains the URLs.
   The csv file must contain the columns "Short Description", "Long Description", "Rollover Description".

--------------------------------------------------------------------------------------------------------

5. OPTIONAL There is a test.csv already in the directory. If you want to check that everything works before you
start with your actual file, then you can run run_this_program.py from IDLE and type test.csv when prompted. (no quotation marks)
This should populate the long description, short description and rollover description columns of test.csv with
appropriate description data, except for:

https://en-gb.facebook.com/ - Usually cannot be scraped (very rarely it may succeed though)

https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List - github pages cannot be accurately described by this tool

https://www.thinkuknow.co.uk/- bad SSL certificate, script should give an error message but continue to run.

https://www.stopitnow.org.uk/wp-content/uploads/2021/05/HSB-Prevention-Toolkit_MCH21.pdf - this URL is a pdf file. 
Should give error message but continue to run.

For those 4 URLs the description columns should be empty (unless facebook randomly decides to allow the scrape attempt).
This test should take about 7 minutes.



****************HOW TO USE***********************
1. Open the file run_this_program.py by editing it with IDLE. Then run it from IDLE by hitting F5 or selecting
run > run module.
2. When prompted, enter or paste the name of your csv file without quotation marks and hit enter.
For example: my_file.csv

What happens:
3. The script will begin scraping data from the urls within the column "Tool URL" of the csv file.
If the csv file already contains generated description data then the script will pick up where this ends.
4. Three requests to generate a description will be made to Chat GPT.
5. If the descriptions can be generated then they are shown to you and added to their relevant columns. 
   If not, the URL is added to denied_urls.csv.
6. The script will need to cool off between GPT requests to avoid hitting the rate limit for OpenAI's API.
7. The script will inform you when the process is complete and you can exit.
8. If you hit the rate limit, the script will inform you and save your descriptions and unscrapable urls to their relevant csv files.

IMPORTANT ISSUES: 
The descriptions won't always be perfect and may occasionally contain instances of ChatGPT "breaking character" or behaving
like a salesman.

GitHub tools, websites that rely on JavaScript, and websites that block scraping attempts will all be either innacurately described or not described at all, so they will be added to the denied_urls.csv.

There is a 200 request per day rate limit, so the tool can only generate descriptions for 66 tools per day
when using the free version of OpenAI's API.

The .csv file is written once all descriptions are generated, so if an uncaught error occurs the descriptions generated
so far will not yet be written to the csv file. To finish the process, execute the function:

recover_descriptions()

This will write all the descriptions generated so far to your .csv file. It will also write the list of unscrapable
URLs to the denied_urls.csv.
