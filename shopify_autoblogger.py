import os
import re
import nltk
import random
from openai import OpenAI  
import shopify
import urllib.request

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# File paths for individual API keys
SHOP_API_KEY_FILE = 'shopify_api_key.txt'
SHOP_PASSWORD_FILE = 'shopify_password.txt'
SHOP_STORE_URL_FILE = 'shopify_store_url.txt'
OPENAI_API_KEY_FILE = 'openai_api_key.txt'

# Reading API keys from files
SHOPIFY_API_KEY = read_api_key(SHOP_API_KEY_FILE)
SHOPIFY_PASSWORD = read_api_key(SHOP_PASSWORD_FILE)
SHOPIFY_STORE_URL = read_api_key(SHOP_STORE_URL_FILE)
OPENAI_API_KEY = read_api_key(OPENAI_API_KEY_FILE)

print("SHOPIFY_API_KEY:", SHOPIFY_API_KEY)
print("SHOPIFY_PASSWORD:", SHOPIFY_PASSWORD)
print("SHOPIFY_STORE_URL:", SHOPIFY_STORE_URL)
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# Connect to Shopify
print("Connecting to Shopify...")
try:
    shopify.ShopifyResource.set_site(SHOPIFY_STORE_URL)
    shopify.ShopifyResource.set_user(SHOPIFY_API_KEY)
    shopify.ShopifyResource.set_password(SHOPIFY_PASSWORD)
    print("Connected!")
except Exception as e:
    print(f"Error connecting to Shopify: {e}")
    exit()

# Get the number of products in the store
num_products = len(shopify.Product.find())

print(f"Number of products in the store: {num_products}")

# Ask the user if they want to continue
# Ask the user if they want to continue
while True:
    user_input = input("Generate blog content for all your products? (yes/no): ").strip().lower()
    if user_input == "yes" or user_input == "y":
        break
    elif user_input == "no":
        continue
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

# Function to clean filename
def clean_filename(title):
    title = title.lower()
    title = re.sub(r'[^\w ]+', '', title)
    title = title.replace(' ', '-')
    return title

def strip_html_tags_from_metadata(html):
    clean_text = re.sub('<.*?>', '', html)
    clean_text = re.sub(r'</?h[2-4].*?>', '', clean_text)  # Remove <h2>, <h3>, <h4> tags
    return clean_text

# Function to strip HTML tags  
def strip_html_tags(html):
    clean_text = re.sub('<.*?>', '', html)
    return clean_text

# Function to summarize text
def summarize_text(text, max_sentences=2):
    sentences = sent_tokenize(text)
    return ' '.join(sentences[:max_sentences])

# Function to extract keywords
def extract_keywords(text, max_keywords=5):
    stop_words = set(stopwords.words('english'))
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(max_keywords)]

# Function to generate creative meta title within character limit
def generate_meta_title(title):
    templates = [
        f"Discover the {title} You've Been Dreaming Of",
f"Unlock the Secrets of {title}: Your Ultimate Guide",
f"Mastering {title}: The Complete Handbook",
f"Transform Your Life with {title}: The Ultimate Resource",
f"The Art of {title}: Your Journey Starts Here",
f"Explore the Wonders of {title} and Unleash Your Potential",
f"Unraveling the Mysteries of {title}: Your Pathway to Success",
f"Embrace the Power of {title} and Rewrite Your Story",
f"Navigate the Complexities of {title} with Confidence",
f"Unleash Your Creativity with {title}: A Journey of Self-Discovery",
f"Discover the Essence of {title} and Ignite Your Passion",
f"Crack the Code of {title} and Achieve Unprecedented Success",
f"Elevate Your Skills with {title}: Your Blueprint for Excellence",
f"Unlocking the Magic of {title}: Your Gateway to Success",
f"Embrace the Journey of {title}: Your Path to Greatness Begins Now",
f"Unveil the Potential of {title} and Become the Master of Your Destiny",
f"Embark on a Quest for Mastery with {title} as Your Guide",
f"Discover the Hidden Treasures of {title} and Forge Your Own Path",
f"Deciphering the Secrets of {title}: Your Key to Unlocking Success",
f"Embrace the Adventure of {title} and Redefine Your Limits"

    ]
    meta_title = random.choice(templates)
    return meta_title[:60]  # Limit to 60 characters, but ChatGPT may generate shorter titles

# Function to generate creative meta description within character limit
def generate_meta_description(summary):
    templates = [
        f"Delve into the essence of {summary}. Gain profound insights, insider tips, and invaluable advice.",
f"Peel back the layers of {summary} and reveal its true essence. Unearth invaluable insights and practical wisdom.",
f"Embark on an expedition into the heart of {summary}. Unravel its mysteries and uncover transformative insights.",
f"Immerse yourself in the world of {summary}. Discover its unique charm and practical wisdom.",
f"Let {summary} be your guide to exploration. Uncover its hidden treasures and practical knowledge.",
f"Prepare to be captivated by {summary}. Join us on a journey of discovery and enlightenment.",
f"Unlock the secrets of {summary} and tap into its transformative power. Let knowledge be your guide.",
f"Set sail on the seas of {summary} and chart a course for enlightenment. Discover its hidden wonders and practical guidance.",
f"Embark on an odyssey of discovery with {summary}. Uncover its hidden depths and practical insights.",
f"Discover the magic of {summary}. Unlock its hidden potential and transform your understanding.",
f"Let {summary} be your compass on the journey of discovery. Explore its depths and uncover priceless insights.",
f"Journey into the heart of {summary} and unlock its transformative potential. Let wisdom be your guide.",
f"Discover the enchantment of {summary}. Unlock its hidden treasures and practical wisdom.",
f"Embark on a voyage of discovery with {summary}. Explore its intricacies and uncover valuable insights.",
f"Unravel the mysteries of {summary} and unlock its hidden potential. Let curiosity be your guide.",
f"Prepare for an adventure of the mind with {summary}. Explore its depths and unlock invaluable insights.",
f"Embark on a quest for knowledge with {summary} as your guide. Discover its hidden gems and practical tips.",
f"Uncover the beauty of {summary} and unlock its transformative power. Let exploration be your path.",
f"Journey into the unknown with {summary} as your companion. Discover its secrets and practical wisdom.",
f"Prepare to be enlightened by {summary}. Dive deep into its essence and unlock its transformative potential."

    ]
    meta_description = random.choice(templates)
    return meta_description[:160]  # Limit to 160 characters, but ChatGPT may generate shorter descriptions

# Initialize clients
client = OpenAI(api_key=OPENAI_API_KEY)

# Connect to Shopify
print("Connecting to Shopify...")
try:
    shopify.ShopifyResource.set_site(SHOPIFY_STORE_URL)
    shopify.ShopifyResource.set_user(SHOPIFY_API_KEY)
    shopify.ShopifyResource.set_password(SHOPIFY_PASSWORD)
    print("Connected!")
except Exception as e:
    print(f"Error connecting to Shopify: {e}")
    exit()
  
# Create folder for posts   
os.makedirs("generated_posts", exist_ok=True)

# Generate posts
print("Generating posts...")

try:
    products = shopify.Product.find()
    num_products = len(products)

    for index, product in enumerate(products, start=1):  # enumerate with start=1 to count from 1
        # Get product details
        title = product.title
        image_filename = f"{clean_filename(title)}.jpg"
        post_folder = f"generated_posts/{clean_filename(title)}"
        os.makedirs(post_folder, exist_ok=True)
        description = strip_html_tags(product.body_html)
        product_handle = product.handle
        product_url = f"{SHOPIFY_STORE_URL}/products/{product_handle}"
        buy_link = f'<p><a href="{product_url}">Buy Now!</a></p>'
    
        # Extract first image
        first_image = None
        if len(product.images) > 0:
            first_image = product.images[0].src
    
        # Load system prompt text 
        with open('system_prompt.txt') as f:
            system_prompt = f.read()

        # Load sample format  
        with open('sample_format.html') as f:
            sample_format = f.read()

        # Generate prompt with both system prompt and format example
        prompt = f"Write a blog post about: {title} | {description} | {first_image}. The format should follow this example: {sample_format}. Do not deviate from this sample, do not be creative with the formatting, please follow the same provided and the output should be formatted correctly."

        # Generate blog post
        completion = client.chat.completions.create(
            temperature=1.2,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        blog_post = completion.choices[0].message.content
        blog_post = blog_post.replace('*', '')


        # Save generated post
        filename = f"{clean_filename(title)}.html"
        image_path = f"{post_folder}/{image_filename}" 
        urllib.request.urlretrieve(first_image, image_path)

        print(f"-Saved image to {image_path}")

        # Generate metadata
        summary = summarize_text(blog_post)
        keywords = extract_keywords(blog_post)
        meta_title = generate_meta_title(title)
        meta_description = generate_meta_description(summary)
        meta_excerpt = summary
        meta_tags = ", ".join(keywords)

        # Write metadata to individual .txt files
        metadata_folder = os.path.join(post_folder, "metadata")
        os.makedirs(metadata_folder, exist_ok=True)

        title_filename = "meta_title.txt"
        description_filename = "meta_description.txt"
        excerpt_filename = "excerpt.txt"
        tags_filename = "tags.txt"

        with open(os.path.join(metadata_folder, title_filename), "w") as title_file:
            title_file.write(f"{meta_title}\n")
        print(f"-Saved meta title to {os.path.join(metadata_folder, title_filename)}")

        with open(os.path.join(metadata_folder, description_filename), "w") as description_file:
            description_file.write(f"{strip_html_tags_from_metadata(meta_description)}\n")
        print(f"-Saved meta description to {os.path.join(metadata_folder, description_filename)}")

        with open(os.path.join(metadata_folder, excerpt_filename), "w") as excerpt_file:
            excerpt_file.write(f"{strip_html_tags_from_metadata(meta_excerpt)}\n")
        print(f"-Saved excerpt to {os.path.join(metadata_folder, excerpt_filename)}")

        with open(os.path.join(metadata_folder, tags_filename), "w") as tags_file:
            tags_file.write(f"{meta_tags}\n")
        print(f"-Saved tags to {os.path.join(metadata_folder, tags_filename)}")

        # Generate HTML
        post_html_path = f"{post_folder}/blog_content.html"
        post_html = f"<html><body>{blog_post}</body>{buy_link}</html>"
    
        with open(post_html_path, "w", encoding='utf-8') as f:
            f.write(post_html)
      
        print(f"-Saved post content to {post_html_path}")
        print(f"Completed generating files for product {index} out of {num_products} total.")
except Exception as e:
    print(f"Error generating posts: {e}")


      

