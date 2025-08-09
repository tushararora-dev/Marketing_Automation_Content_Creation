# 🛠 Brand Analysis Tool — Function Overview

## Main Functions

### `analyze_brand_from_url(url)`
**Purpose:** Main orchestrator function that analyzes a complete brand website  
**Does:** Calls all other functions to extract comprehensive brand data  
**Returns:** Complete dictionary with all brand information  

### `get_website_text_content(url)`
**Purpose:** Downloads and cleans website content  
**Does:** Fetches HTML, removes tags, extracts clean text  
**Returns:** Clean text content from the website  


## 📌 Brand Information Extractors

### `extract_brand_name(content, url)`
**Purpose:** Finds the brand/company name  
**Does:** Looks for patterns like `"Welcome to [Brand]"`, page titles, or uses domain name  
**Returns:** Brand name as string  

### `extract_domain_name(url)`
**Purpose:** Backup method to get brand name from URL  
**Does:** Cleans domain name (removes `www`, `.com`, etc.)  
**Returns:** Clean domain name  

### `extract_brand_description(content)`
**Purpose:** Finds company description or mission statement  
**Does:** Searches for `"About us"`, `"We are"`, `"Our mission"` sections  
**Returns:** Brand description text  

### `extract_products(content)`
**Purpose:** Identifies products or services offered  
**Does:** Looks for `"Products:"`, `"We offer:"`, `"Services:"` patterns  
**Returns:** List of product/service names  

### `extract_target_audience(content)`
**Purpose:** Determines who the brand targets  
**Does:** Searches for `"designed for"`, `"targeting"`, demographic keywords  
**Returns:** Target audience description  

### `extract_value_propositions(content)`
**Purpose:** Finds what makes the brand special/beneficial  
**Does:** Looks for benefit words like `"save"`, `"improve"`, `"faster"`, quality indicators  
**Returns:** List of value propositions  


## 📊 Analysis Functions

### `extract_keywords(content)`
**Purpose:** Finds most important/frequent words  
**Does:** Counts word frequency, excludes common words (`the`, `and`, etc.)  
**Returns:** List of relevant keywords  

### `analyze_brand_tone(content)`
**Purpose:** Determines brand communication style  
**Does:** Counts formal vs casual vs professional vs friendly words  
**Returns:** Dominant tone (e.g., `"Professional"`, `"Casual"`)  

### `extract_competitors(content)`
**Purpose:** Finds mentioned competitors  
**Does:** Looks for `"vs"`, `"unlike"`, `"compared to"` patterns  
**Returns:** List of competitor names  


## 📞 Contact & Social Functions

### `extract_contact_info(content)`
**Purpose:** Finds contact details  
**Does:** Uses regex to find emails, phone numbers, addresses  
**Returns:** Dictionary with contact information  

### `extract_social_links(url)`
**Purpose:** Finds social media profiles  
**Does:** Searches HTML for Facebook, Twitter, Instagram, etc. links  
**Returns:** Dictionary with social media URLs  


## 🎨 Additional Analysis

### `extract_brand_colors(url)`
**Purpose:** Identifies brand color scheme  
**Does:** Parses CSS for color codes (`#ffffff`, etc.)  
**Returns:** List of brand colors  

### `extract_content_themes(content)`
**Purpose:** Categorizes the business type  
**Does:** Looks for keywords to classify (technology, health, business, etc.)  
**Returns:** List of content themes  

### `extract_pricing_info(content)`
**Purpose:** Finds pricing information  
**Does:** Searches for price patterns (`$99`, `"from $50"`), pricing models  
**Returns:** Dictionary with pricing data  


## ⚙ Utility Functions

### `validate_url(url)`
**Purpose:** Checks if website is accessible  
**Does:** Makes HTTP HEAD request to test connectivity  
**Returns:** True/False  

### `get_website_metadata(url)`
**Purpose:** Gets HTML meta information  
**Does:** Extracts title, meta description, meta keywords from HTML  
**Returns:** Dictionary with metadata  


## 📌 Summary
This tool essentially scrapes any website and creates a **marketing profile** by extracting:

- **Basic info:** name, description  
- **Business details:** products, audience, competitors  
- **Brand characteristics:** tone, colors, themes  
- **Contact information:** email, phone, social media  
- **Marketing data:** keywords, value props, pricing  

💡 *It's like having an automated marketing research assistant that can analyze any brand's website in seconds!*
