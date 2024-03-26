# shopify_autoblogger
Read products from your Shopify store and create a blog post for each one automatically using ChatGPT 3.5 Turbo. Each blog post will be exported to an HTML file, and the first variant image will be saved. The code will create a subfolder an generate a meta title, a meta description, an excerpt and tags based on your content. This is local app and has no security functions. You will be running this app in your terminal, I prefer Visual Studio Code.

Create a Shopify App

1. You will need to create a custom app (dev app) in Shopify and give it a name.
2. Click Configure Admin API Scopes and specify one scope ( read_products ).
3. Once you have selected the correct scope under Products, click install.
4. this will install the App, and create API keys. Click revel access token, and save to a txt file.
5. Below that, you will see your Shopify API for your app. Save API Key and Secret API Key to text files.
6. Save your app.

