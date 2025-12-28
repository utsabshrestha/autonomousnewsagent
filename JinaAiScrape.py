import requests
import re

def JinaAiScrape(state):
    """
    Node 3: The Reader
    Takes a URL from the state, scrapes it using Jina Reader, 
    and returns clean Markdown.
    """
    url_to_scrape = state["url"]
    
    # Jina Reader API works by simply prepending 'https://r.jina.ai/'
    jina_url = f"https://r.jina.ai/{url_to_scrape}"
    
    headers = {
       "Authorization": "Bearer jina_42695fb14f2f42e1b6395dc5420c5e223C1WcbBpIJo-tgZZWEfP-Lf8yrWk",
        # "X-Retain-Images": "none",
        "X-Return-Format": "markdown"
    }
        
    try:
        response = requests.get(jina_url, headers=headers)
        
        if response.status_code == 200:
            main_image_url = extract_main_image_url(response.text)
            clean_content = clean_news_data(response.text)
            return {"article_content": clean_content, "image_url": main_image_url}
        else:
            return {"error": f"Failed to read page: {response.status_code}", "article_content":""}
            
    except Exception as e:
        return {f"Error @ {JinaAiScrape.__name__}": str(e)}

def clean_news_data(markdown_text):
    try:

        """
        Cleans raw Markdown news data by removing navigation, ads, 
        cookie notices, and metadata.
        """
        
        # 1. REMOVE IMAGES
        # Pattern: ![Alt Text](URL)
        # Why: LLMs don't need image URLs for text analysis.
        text = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)

        # 2. REMOVE "SKIP TO" & ACCESSIBILITY LINKS
        # Pattern: [Skip to content](...) or similar
        text = re.sub(r'(?i)\[skip to.*?\]\(.*?\)', '', text)

        # 3. REMOVE EMPTY LINKS (Logos/Icons)
        # Pattern: [](https://...) -> often used for site logos
        text = re.sub(r'\[\]\(http.*?\)', '', text)

        # 4. REMOVE ADVERTISEMENT MARKERS
        # Pattern: [SKIP ADVERTISEMENT], [Advertiser Content], etc.
        text = re.sub(r'(?i)\[(skip advertisement|advertiser content|partner content).*?\]\(.*?\)', '', text)
        text = re.sub(r'(?i)^\s*(advertisement|supported by)\s*$', '', text, flags=re.MULTILINE)

        # 5. REMOVE NAVIGATION LISTS (Crucial for The Verge/NYT)
        # Pattern: Lines that start with * [Link] and nothing else.
        # This removes the huge "Tech, Science, Reviews" menus.
        # Logic: Look for a newline, a bullet, a link, and immediate newline.
        text = re.sub(r'(?m)^\s*[\*\-]\s+\[.*?\]\(.*?\)\s*$', '', text)

        # 6. REMOVE COOKIE/PRIVACY CONSENT BLOCKS (Crucial for Wired/Verge)
        # Pattern: aggressive matching for "Manage your consent" blocks
        # We remove lines containing specific "legal" keywords commonly found in these popups.
        privacy_keywords = [
            "manage your consent", "strictly necessary cookies", "performance cookies", 
            "functional cookies", "targeting cookies", "confirm my choices", 
            "reject all", "accept all", "vendor list", "privacy policy", 
            "allow sale/targeted advertising"
        ]
        for keyword in privacy_keywords:
            # Removes the whole line if it contains the keyword
            text = re.sub(r'(?i)^.*' + re.escape(keyword) + r'.*$', '', text, flags=re.MULTILINE)

        # 7. REMOVE SOCIAL & METADATA
        # Pattern: "Share full article", "Most Popular", "Read X comments"
        meta_patterns = [
            r'(?i)^.*share full article.*$', 
            r'(?i)^.*read \d+ comments.*$',
            r'(?i)^.*most popular.*$',
            r'(?i)^.*newsletter.*$',
            r'(?i)^.*sign up.*$'
        ]
        for pattern in meta_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)

        # 8. CLEAN UP FORMATTING
        # Links inside text: [Text](URL) -> Text (Keep the text, kill the URL)
        # Note: We do this LAST so we don't accidentally break the navigation regex above.
        text = re.sub(r'\[([^\]]+)\]\(http[s]?://.*?\)', r'\1', text)
        
        # Collapse multiple newlines (3 or more) into just 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    except Exception as error:
        print(f"Error @ : {clean_news_data.__name__} : {error}")
        return markdown_text

def extract_main_image_url(markdown_text: str) -> str:
    try:
        # Regex to find all markdown images: ![Alt Text](URL)
        # Group 1 captures the URL
        image_patterns = re.findall(r'!\[.*?\]\((https?://.*?)\)', markdown_text)
        
        # Valid extensions for a "main" news image
        # We skip .svg because they are usually logos/icons, not news photos
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        
        for img_url in image_patterns:
            # Check 1: Does it look like an image file?
            # We convert to lower case to match .JPG and .jpg
            lower_url = img_url.lower()
            
            # Check 2: Filter out common "garbage" images often found in scraping
            if "logo" in lower_url or "icon" in lower_url or "avatar" in lower_url:
                continue
                
            # Check 3: Must have a valid extension (or look like a CDN image)
            if any(ext in lower_url for ext in valid_extensions):
                return img_url
        
        # Fallback: If no perfect match found, but we found *some* image, return the first one
        if image_patterns:
             return image_patterns[0]
             
        return "" # No image found
        
    except Exception as e:
        print(f"Error extraction image: {e}")
        return ""