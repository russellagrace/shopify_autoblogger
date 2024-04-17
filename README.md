# shopify_autoblogger
About the script

This script  will read products from your Shopify store and create a blog post for each one automatically using ChatGPT 3.5 Turbo. Each blog post will be exported to an HTML file, and the first variant image will be saved. The code will create a subfolder and generate a meta title, a meta description, an excerpt and tags based on your content. The content generated is saved to a folder named generated_content. Each subfolder is named as the product title.
This is local app and has no security functions and limited error handling. You will be running this app in your terminal, I prefer Visual Studio Code. This script will generate blog content that you will have to manually publish in your Shopify store. This script just removes the tedious task of generating content one at a time. If you have 30 products, it will create content for all 30 products or 25,000 products.

Basic Instructions

1. You will need to create a custom app (dev app) in Shopify and give it a name.
2. Click Configure Admin API Scopes and specify one scope ( read_products ).
3. Once you have selected the correct scope under Products, click install.
4. This will install the App, and create API keys.
5. Scroll down and you will see your Shopify API key for your app. Save API Key to the text file.
6. Save your app.

- Editing files

9. Download all the files in the repository as a zip file and extract.
10. Edit the API text files and password file with your own. You will need an OpenAPI key as well (i'll leave those instructions to someone else).
12. Open the folder in Visual Studio Code
13. There are two files you can change to tell chatgpt how to handle your content sample_format.html and system_prompt.txt.
14. The sample_format.html gives chatgpt a sample of how to format your blog post content and title. Please adjust this to suit your needs.
15. The sample_prompt.txt are instructions on how to write your content. Please adjust this to suite your needs.
16. These are foundation files.
10. You can also edit the code to adjust for chatgpt temp (line 204). This is chatgpt's creativity setting. 2.0 is the max. I found this setting to be stable. Any higher the code may crash.

- Running the script

13. In terminal you will need to install these libraies:
    > python -m pip install nltk or pip install nltk
    > python -m pip install openai or pip install openai
    > python -m pip install ShopifyAPI or pip install ShopifyAPI
14. Once you installed these libraries right click on shopify_autoblogger.py and select Run Python File in Terminal

15. Enjoy!

If you experience problems, please comment. 
