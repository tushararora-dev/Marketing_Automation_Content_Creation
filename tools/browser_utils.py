import requests
import trafilatura
import json
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import time

def analyze_brand_from_url(url: str) -> Dict[str, Any]:
    """
    Analyze a brand's website to extract key information for marketing campaigns
    
    Args:
        url: Brand website URL
    
    Returns:
        Comprehensive brand analysis data
    """
    
    try:
        # Get website content
        website_content = get_website_text_content(url)
        
        if not website_content:
            raise Exception(f"Failed to extract content from {url}")
        
        # Extract brand information
        brand_analysis = {
            "url": url,
            "brand_name": extract_brand_name(website_content, url),
            "description": extract_brand_description(website_content),
            "products": extract_products(website_content),
            "target_audience": extract_target_audience(website_content),
            "value_propositions": extract_value_propositions(website_content),
            "keywords": extract_keywords(website_content),
            "colors": extract_brand_colors(url),
            "tone": analyze_brand_tone(website_content),
            "competitors": extract_competitors(website_content),
            "contact_info": extract_contact_info(website_content),
            "social_links": extract_social_links(url),
            "content_themes": extract_content_themes(website_content),
            "pricing_info": extract_pricing_info(website_content),
            "analyzed_at": time.time()
        }
        
        return brand_analysis
        
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "brand_name": extract_domain_name(url),
            "description": "Brand analysis failed - using fallback data",
            "products": ["Product or Service"],
            "target_audience": "General consumers",
            "analyzed_at": time.time()
        }

def get_website_text_content(url: str) -> str:
    """
    Extract clean text content from website using trafilatura
    
    Args:
        url: Website URL
    
    Returns:
        Clean text content from the website
    """
    
    try:
        # Download the webpage
        downloaded = trafilatura.fetch_url(url)
        
        if not downloaded:
            raise Exception(f"Failed to download content from {url}")
        
        # Extract main text content
        text_content = trafilatura.extract(downloaded)
        
        if not text_content:
            raise Exception(f"Failed to extract text from {url}")
        
        return text_content
        
    except Exception as e:
        # Fallback: try basic requests
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            if response.status_code == 200:
                # Basic text extraction from HTML
                html_content = response.text
                # Remove HTML tags (basic approach)
                text_content = re.sub(r'<[^>]+>', ' ', html_content)
                # Clean up whitespace
                text_content = ' '.join(text_content.split())
                return text_content[:5000]  # Limit to first 5000 chars
            else:
                raise Exception(f"HTTP {response.status_code}")
                
        except Exception as fallback_error:
            raise Exception(f"All extraction methods failed: {str(e)}, {str(fallback_error)}")

def extract_brand_name(content: str, url: str) -> str:
    """Extract brand name from website content"""
    
    # Look for common brand name patterns
    patterns = [
        r'<title[^>]*>([^<]+)</title>',
        r'brand[:\s]+([A-Za-z0-9\s]+)',
        r'company[:\s]+([A-Za-z0-9\s]+)',
        r'welcome to ([A-Za-z0-9\s]+)',
        r'about ([A-Za-z0-9\s]+)'
    ]
    
    content_lower = content.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        if matches:
            # Clean and return first match
            brand_name = matches[0].strip()
            # Remove common words
            brand_name = re.sub(r'\b(the|inc|llc|ltd|company|corp|corporation)\b', '', brand_name, flags=re.IGNORECASE)
            brand_name = brand_name.strip()
            if len(brand_name) > 2 and len(brand_name) < 50:
                return brand_name.title()
    
    # Fallback: extract from domain
    return extract_domain_name(url)

def extract_domain_name(url: str) -> str:
    """Extract clean domain name as brand name fallback"""
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Remove www and common extensions
        domain = re.sub(r'^www\.', '', domain)
        domain = re.sub(r'\.(com|org|net|io|co|us|uk|ca)$', '', domain, flags=re.IGNORECASE)
        
        return domain.title()
        
    except:
        return "Brand"

def extract_brand_description(content: str) -> str:
    """Extract brand description or mission statement"""
    
    # Look for description patterns
    patterns = [
        r'(?:we are|we\'re|our mission|about us|description)[:\s]+([^.!?]{20,200}[.!?])',
        r'(?:providing|offering|specializing in|focused on)[:\s]+([^.!?]{20,200}[.!?])',
        r'(?:helping|enabling|empowering)[^.!?]*?([^.!?]{20,200}[.!?])'
    ]
    
    content_lower = content.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE | re.DOTALL)
        if matches:
            description = matches[0].strip()
            # Clean up the description
            description = re.sub(r'\s+', ' ', description)
            if len(description) > 20:
                return description.capitalize()
    
    # Fallback: extract first meaningful paragraph
    sentences = content.split('.')
    for sentence in sentences[:10]:
        sentence = sentence.strip()
        if len(sentence) > 50 and len(sentence) < 300:
            # Check if it's descriptive (contains certain keywords)
            if any(word in sentence.lower() for word in ['provide', 'offer', 'help', 'solution', 'service', 'product']):
                return sentence + '.'
    
    return "A leading provider of quality products and services."

def extract_products(content: str) -> List[str]:
    """Extract product or service names from content"""
    
    products = []
    content_lower = content.lower()
    
    # Look for product/service patterns
    product_patterns = [
        r'(?:products?|services?|offering|solutions?)[:\s]+([^.!?]{10,100})',
        r'(?:we offer|we provide|available)[:\s]+([^.!?]{10,100})',
        r'(?:including|featuring|such as)[:\s]+([^.!?]{10,100})'
    ]
    
    for pattern in product_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            # Split on common separators
            items = re.split(r'[,;|&]', match)
            for item in items[:5]:  # Limit to first 5 items
                item = item.strip()
                if len(item) > 3 and len(item) < 50:
                    products.append(item.title())
    
    # Look for common product keywords
    product_keywords = [
        'software', 'app', 'platform', 'tool', 'service', 'solution',
        'product', 'system', 'course', 'training', 'consulting',
        'design', 'development', 'marketing', 'analytics'
    ]
    
    words = content_lower.split()
    for i, word in enumerate(words):
        if word in product_keywords and i > 0:
            # Get context around the keyword
            start = max(0, i-2)
            end = min(len(words), i+3)
            context = ' '.join(words[start:end])
            if len(context) < 50:
                products.append(context.title())
    
    # Remove duplicates and return top 5
    unique_products = list(set(products))
    return unique_products[:5] if unique_products else ["Products and Services"]

def extract_target_audience(content: str) -> str:
    """Extract target audience information"""
    
    content_lower = content.lower()
    
    # Look for audience patterns
    audience_patterns = [
        r'(?:for|targeting|designed for|perfect for|ideal for)[:\s]+([^.!?]{10,100})',
        r'(?:customers?|clients?|users?|professionals?)[:\s]+([^.!?]{10,100})',
        r'(?:businesses?|companies?|individuals?|people who)[^.!?]*?([^.!?]{10,100})'
    ]
    
    for pattern in audience_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        if matches:
            audience = matches[0].strip()
            if len(audience) > 10:
                return audience.capitalize()
    
    # Look for demographic keywords
    demo_keywords = {
        'small business': 'Small business owners',
        'enterprise': 'Enterprise clients',
        'startup': 'Startups and entrepreneurs',
        'professional': 'Working professionals',
        'student': 'Students and learners',
        'developer': 'Developers and technical teams',
        'marketer': 'Marketing professionals',
        'designer': 'Designers and creatives'
    }
    
    for keyword, audience in demo_keywords.items():
        if keyword in content_lower:
            return audience
    
    return "General consumers and businesses"

def extract_value_propositions(content: str) -> List[str]:
    """Extract key value propositions"""
    
    value_props = []
    content_lower = content.lower()
    
    # Look for benefit patterns
    benefit_patterns = [
        r'(?:save|saves?|saving)[^.!?]*?([^.!?]{10,100}[.!?])',
        r'(?:increase|increases?|boost|improve)[^.!?]*?([^.!?]{10,100}[.!?])',
        r'(?:reduce|reduces?|eliminate|cut)[^.!?]*?([^.!?]{10,100}[.!?])',
        r'(?:faster|quicker|easier|better)[^.!?]*?([^.!?]{10,100}[.!?])'
    ]
    
    for pattern in benefit_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE | re.DOTALL)
        for match in matches[:3]:  # Limit to 3 per pattern
            prop = match.strip()
            if len(prop) > 15:
                value_props.append(prop.capitalize())
    
    # Look for quality indicators
    quality_keywords = [
        'award-winning', 'industry-leading', 'best-in-class',
        'proven', 'trusted', 'reliable', 'innovative', 'cutting-edge'
    ]
    
    for keyword in quality_keywords:
        if keyword in content_lower:
            value_props.append(f"{keyword.title()} solution")
    
    return value_props[:5] if value_props else ["High-quality products and services"]

def extract_keywords(content: str) -> List[str]:
    """Extract relevant keywords from content"""
    
    # Common stop words to exclude
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
        'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
    }
    
    # Clean and split content
    words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
    
    # Count word frequency
    word_count = {}
    for word in words:
        if word not in stop_words:
            word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, count in sorted_words[:20] if count > 1]
    
    return keywords

def extract_brand_colors(url: str) -> List[str]:
    """Extract brand colors from website (basic implementation)"""
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            html_content = response.text
            
            # Look for CSS color definitions
            color_patterns = [
                r'color[:\s]*([#][0-9a-fA-F]{6})',
                r'background-color[:\s]*([#][0-9a-fA-F]{6})',
                r'border-color[:\s]*([#][0-9a-fA-F]{6})'
            ]
            
            colors = set()
            for pattern in color_patterns:
                matches = re.findall(pattern, html_content)
                colors.update(matches)
            
            # Return common brand colors (excluding common web colors)
            exclude_colors = {'#ffffff', '#000000', '#f0f0f0', '#e0e0e0'}
            brand_colors = [color for color in colors if color.lower() not in exclude_colors]
            
            return brand_colors[:5] if brand_colors else ['#007bff', '#6c757d']
            
    except:
        pass
    
    # Default color scheme
    return ['#007bff', '#6c757d']

def analyze_brand_tone(content: str) -> str:
    """Analyze brand tone from content"""
    
    content_lower = content.lower()
    
    # Tone indicators
    formal_indicators = ['pursuant', 'therefore', 'hereby', 'whereas', 'furthermore']
    casual_indicators = ['hey', 'awesome', 'cool', 'amazing', 'love', 'super']
    professional_indicators = ['solution', 'expertise', 'professional', 'industry', 'enterprise']
    friendly_indicators = ['welcome', 'help', 'support', 'team', 'together']
    
    scores = {
        'formal': sum(1 for word in formal_indicators if word in content_lower),
        'casual': sum(1 for word in casual_indicators if word in content_lower),
        'professional': sum(1 for word in professional_indicators if word in content_lower),
        'friendly': sum(1 for word in friendly_indicators if word in content_lower)
    }
    
    # Determine dominant tone
    max_tone = max(scores, key=scores.get)
    
    if scores[max_tone] == 0:
        return "Professional"
    
    return max_tone.capitalize()

def extract_competitors(content: str) -> List[str]:
    """Extract potential competitors mentioned in content"""
    
    competitors = []
    content_lower = content.lower()
    
    # Look for competitor patterns
    competitor_patterns = [
        r'(?:unlike|compared to|better than|vs\.?|versus)[:\s]+([A-Za-z0-9\s]{3,30})',
        r'(?:alternative to|competitor|competing with)[:\s]+([A-Za-z0-9\s]{3,30})'
    ]
    
    for pattern in competitor_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            competitor = match.strip()
            if len(competitor) > 2 and len(competitor) < 30:
                competitors.append(competitor.title())
    
    return competitors[:5]

def extract_contact_info(content: str) -> Dict[str, str]:
    """Extract contact information"""
    
    contact_info = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, content)
    if emails:
        contact_info['email'] = emails[0]
    
    # Phone pattern
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
    phones = re.findall(phone_pattern, content)
    if phones:
        contact_info['phone'] = phones[0]
    
    # Address pattern (basic)
    address_patterns = [
        r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr))',
        r'([A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5})'
    ]
    
    for pattern in address_patterns:
        addresses = re.findall(pattern, content, re.IGNORECASE)
        if addresses:
            contact_info['address'] = addresses[0]
            break
    
    return contact_info

def extract_social_links(url: str) -> Dict[str, str]:
    """Extract social media links from website"""
    
    social_links = {}
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            html_content = response.text
            
            # Social media patterns
            social_patterns = {
                'facebook': r'(?:facebook\.com/|fb\.com/)([A-Za-z0-9\.]+)',
                'twitter': r'(?:twitter\.com/|x\.com/)([A-Za-z0-9_]+)',
                'instagram': r'instagram\.com/([A-Za-z0-9_.]+)',
                'linkedin': r'linkedin\.com/(?:company/|in/)([A-Za-z0-9-]+)',
                'youtube': r'youtube\.com/(?:channel/|user/|c/)([A-Za-z0-9_-]+)',
                'tiktok': r'tiktok\.com/@([A-Za-z0-9_.]+)'
            }
            
            for platform, pattern in social_patterns.items():
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    social_links[platform] = f"https://{platform}.com/{matches[0]}"
    
    except:
        pass
    
    return social_links

def extract_content_themes(content: str) -> List[str]:
    """Extract main content themes"""
    
    themes = []
    content_lower = content.lower()
    
    # Theme categories
    theme_keywords = {
        'technology': ['software', 'tech', 'digital', 'ai', 'automation', 'platform'],
        'health': ['health', 'wellness', 'medical', 'fitness', 'nutrition'],
        'business': ['business', 'enterprise', 'corporate', 'b2b', 'professional'],
        'education': ['education', 'learning', 'training', 'course', 'skill'],
        'lifestyle': ['lifestyle', 'personal', 'home', 'family', 'life'],
        'finance': ['finance', 'money', 'investment', 'financial', 'payment'],
        'ecommerce': ['shop', 'store', 'buy', 'purchase', 'product', 'retail'],
        'service': ['service', 'support', 'help', 'assistance', 'consultation']
    }
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            themes.append(theme.title())
    
    return themes[:3] if themes else ['Business']

def extract_pricing_info(content: str) -> Dict[str, Any]:
    """Extract pricing information if available"""
    
    pricing_info = {
        'has_pricing': False,
        'pricing_model': 'Unknown',
        'price_points': []
    }
    
    content_lower = content.lower()
    
    # Look for pricing indicators
    pricing_keywords = ['price', 'pricing', 'cost', 'fee', 'subscription', 'plan']
    if any(keyword in content_lower for keyword in pricing_keywords):
        pricing_info['has_pricing'] = True
    
    # Price patterns
    price_patterns = [
        r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars?|usd)',
        r'from\s*\$?(\d+)',
        r'starting\s*at\s*\$?(\d+)'
    ]
    
    prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, content_lower)
        prices.extend(matches)
    
    if prices:
        pricing_info['price_points'] = [f"${price}" for price in prices[:5]]
    
    # Pricing model detection
    if 'subscription' in content_lower or 'monthly' in content_lower:
        pricing_info['pricing_model'] = 'Subscription'
    elif 'one-time' in content_lower or 'lifetime' in content_lower:
        pricing_info['pricing_model'] = 'One-time'
    elif 'freemium' in content_lower or 'free trial' in content_lower:
        pricing_info['pricing_model'] = 'Freemium'
    
    return pricing_info

def validate_url(url: str) -> bool:
    """Validate if URL is accessible"""
    
    try:
        response = requests.head(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return response.status_code == 200
    except:
        return False

def get_website_metadata(url: str) -> Dict[str, str]:
    """Get website metadata (title, description, etc.)"""
    
    metadata = {}
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            html_content = response.text
            
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()
            
            # Extract meta keywords
            keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
            if keywords_match:
                metadata['keywords'] = keywords_match.group(1).strip()
    
    except:
        pass
    
    return metadata
