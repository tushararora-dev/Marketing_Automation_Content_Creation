from typing import Dict, Any, List
from tools.llm_manager import get_llm_response
from prompts.ad_prompts import get_ad_copy_prompt, get_social_caption_prompt

def generate_ad_copy(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[Dict[str, Any]]:
    """
    Generate ad copy variants for different platforms
    
    Args:
        content_strategy: Content strategy and requirements
        target_audience: Target audience description
        brand_tone: Brand tone/voice
    
    Returns:
        List of ad copy variants with headlines, primary text, and CTAs
    """
    
    ad_copies = []
    
    # Generate multiple ad copy variants
    for i in range(3):  # Generate 3 variants
        ad_copy = generate_single_ad_copy(
            content_strategy=content_strategy,
            target_audience=target_audience,
            brand_tone=brand_tone,
            variant_number=i + 1
        )
        ad_copies.append(ad_copy)
    
    return ad_copies

def generate_single_ad_copy(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str,
    variant_number: int
) -> Dict[str, Any]:
    """Generate a single ad copy variant"""
    
    # Build ad copy generation prompt
    ad_prompt = get_ad_copy_prompt(
        content_strategy=content_strategy,
        target_audience=target_audience,
        brand_tone=brand_tone,
        variant_number=variant_number
    )
    
    # Get ad copy from LLM
    ad_response = get_llm_response(
        prompt=ad_prompt,
        system_message="You are an expert advertising copywriter specializing in high-converting ad copy. Create compelling, persuasive copy that drives action."
    )
    
    # Parse the ad copy response
    ad_copy = parse_ad_copy_response(ad_response, variant_number)
    
    return ad_copy

def parse_ad_copy_response(ad_text: str, variant_number: int) -> Dict[str, Any]:
    """Parse LLM response into structured ad copy format"""
    
    ad_copy = {
        "variant": variant_number,
        "headline": extract_headline(ad_text),
        "primary_text": extract_primary_text(ad_text),
        "cta": extract_cta(ad_text),
        "description": extract_description(ad_text),
        "platform_adaptations": create_platform_adaptations(ad_text),
        "character_counts": {},
        "full_response": ad_text
    }
    
    # Calculate character counts for different platforms
    ad_copy["character_counts"] = {
        "facebook_headline": len(ad_copy["headline"]),
        "facebook_primary": len(ad_copy["primary_text"]),
        "google_headline": len(ad_copy["headline"][:30]),  # Google Ads limit
        "twitter": len(f"{ad_copy['headline']} {ad_copy['primary_text']}")
    }
    
    return ad_copy

def extract_headline(ad_text: str) -> str:
    """Extract headline from ad copy text"""
    
    lines = ad_text.split('\n')
    
    # Look for headline indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('headline:'):
            return line_clean.split(':', 1)[1].strip()
        elif '**Headline:**' in line:
            return line.split('**Headline:**')[1].split('**')[0].strip()
        elif line_clean.lower().startswith('title:'):
            return line_clean.split(':', 1)[1].strip()
    
    # Look for first line that could be a headline (short and punchy)
    for line in lines[:5]:
        line_clean = line.strip()
        if line_clean and len(line_clean) < 100 and not line_clean.startswith('#'):
            return line_clean
    
    return "Transform Your Life Today!"

def extract_primary_text(ad_text: str) -> str:
    """Extract primary text from ad copy"""
    
    lines = ad_text.split('\n')
    primary_lines = []
    
    # Look for primary text indicators
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if line_clean.lower().startswith('primary text:') or line_clean.lower().startswith('body:'):
            # Collect subsequent lines as primary text
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.lower().startswith('cta:') and not next_line.lower().startswith('call to action:'):
                    primary_lines.append(next_line)
                elif next_line.lower().startswith('cta:') or next_line.lower().startswith('call to action:'):
                    break
            break
    
    if primary_lines:
        return ' '.join(primary_lines)
    
    # Fallback: extract body content
    body_lines = []
    skip_patterns = ['headline:', 'title:', 'cta:', 'call to action:', '**', '#']
    
    for line in lines:
        line_clean = line.strip()
        if line_clean and not any(pattern in line_clean.lower() for pattern in skip_patterns):
            body_lines.append(line_clean)
    
    if body_lines:
        return ' '.join(body_lines[:3])  # Take first 3 lines as primary text
    
    return "Discover the perfect solution for your needs. Don't miss out on this amazing opportunity."

def extract_cta(ad_text: str) -> str:
    """Extract call-to-action from ad copy"""
    
    lines = ad_text.split('\n')
    
    # Look for CTA indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('cta:'):
            return line_clean.split(':', 1)[1].strip()
        elif '**CTA:**' in line:
            return line.split('**CTA:**')[1].split('**')[0].strip()
        elif line_clean.lower().startswith('call to action:'):
            return line_clean.split(':', 1)[1].strip()
    
    # Look for button-like text
    cta_patterns = [
        "shop now", "buy now", "get started", "learn more", "sign up",
        "download now", "claim offer", "try free", "book now", "order today"
    ]
    
    for line in lines:
        line_lower = line.lower()
        for pattern in cta_patterns:
            if pattern in line_lower:
                return pattern.title()
    
    return "Get Started Now"

def extract_description(ad_text: str) -> str:
    """Extract description or supporting text"""
    
    lines = ad_text.split('\n')
    
    # Look for description indicators
    for line in lines:
        line_clean = line.strip()
        if line_clean.lower().startswith('description:'):
            return line_clean.split(':', 1)[1].strip()
        elif '**Description:**' in line:
            return line.split('**Description:**')[1].split('**')[0].strip()
    
    # Use primary text as description if no separate description found
    primary_text = extract_primary_text(ad_text)
    return primary_text[:100] + "..." if len(primary_text) > 100 else primary_text

def create_platform_adaptations(ad_text: str) -> Dict[str, Dict[str, str]]:
    """Create platform-specific adaptations of the ad copy"""
    
    headline = extract_headline(ad_text)
    primary_text = extract_primary_text(ad_text)
    cta = extract_cta(ad_text)
    
    adaptations = {
        "facebook": {
            "headline": headline[:40],  # Facebook headline limit
            "primary_text": primary_text[:125],  # Recommended length
            "cta": cta,
            "link_description": primary_text[125:155] if len(primary_text) > 125 else ""
        },
        "google_ads": {
            "headline_1": headline[:30],  # Google Ads headline limit
            "headline_2": create_second_headline(headline, primary_text)[:30],
            "description_1": primary_text[:90],  # Description limit
            "description_2": create_second_description(primary_text)[:90],
            "final_url": "[LANDING_PAGE_URL]"
        },
        "instagram": {
            "caption": f"{headline}\n\n{primary_text}\n\n#{' #'.join(generate_hashtags(primary_text))}",
            "cta": cta
        },
        "linkedin": {
            "headline": headline,
            "intro_text": primary_text[:150],
            "cta": cta
        },
        "twitter": {
            "tweet": optimize_for_twitter(headline, primary_text, cta),
            "thread": create_twitter_thread(headline, primary_text, cta)
        }
    }
    
    return adaptations

def create_second_headline(headline: str, primary_text: str) -> str:
    """Create a second headline for Google Ads"""
    
    # Extract key benefit or feature from primary text
    words = primary_text.split()
    key_phrases = []
    
    benefit_words = ["save", "free", "fast", "easy", "best", "new", "proven", "guaranteed"]
    
    for word in words:
        if word.lower() in benefit_words:
            key_phrases.append(word)
    
    if key_phrases:
        return f"{key_phrases[0].title()} & Reliable"
    
    return "Trusted Solution"

def create_second_description(primary_text: str) -> str:
    """Create a second description for Google Ads"""
    
    # Create a complementary description
    if "save" in primary_text.lower():
        return "Join thousands of satisfied customers. Limited time offer."
    elif "new" in primary_text.lower():
        return "Latest technology. Try risk-free today."
    else:
        return "Trusted by professionals. Start your journey now."

def generate_hashtags(text: str) -> List[str]:
    """Generate relevant hashtags from text"""
    
    # Extract key words and convert to hashtags
    words = text.lower().split()
    
    # Filter out common words and create hashtags
    stop_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    
    hashtags = []
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum())
        if len(clean_word) > 3 and clean_word not in stop_words:
            hashtags.append(clean_word)
    
    # Add common marketing hashtags
    marketing_hashtags = ["business", "success", "innovation", "quality", "lifestyle"]
    hashtags.extend(marketing_hashtags[:2])
    
    return hashtags[:8]  # Limit to 8 hashtags

def optimize_for_twitter(headline: str, primary_text: str, cta: str) -> str:
    """Optimize content for Twitter's character limit"""
    
    # Twitter limit is 280 characters
    full_tweet = f"{headline} {primary_text} {cta}"
    
    if len(full_tweet) <= 250:  # Leave room for links
        return full_tweet
    
    # Shorten if needed
    shortened_primary = primary_text[:100] + "..." if len(primary_text) > 100 else primary_text
    shortened_tweet = f"{headline} {shortened_primary} {cta}"
    
    if len(shortened_tweet) <= 250:
        return shortened_tweet
    
    # Further shorten
    return f"{headline[:50]}... {cta}"

def create_twitter_thread(headline: str, primary_text: str, cta: str) -> List[str]:
    """Create a Twitter thread from the ad copy"""
    
    thread = []
    
    # Tweet 1: Hook/Headline
    thread.append(f"{headline} 🧵")
    
    # Tweet 2: Main benefit/problem
    sentences = primary_text.split('.')
    if len(sentences) > 0:
        thread.append(f"{sentences[0].strip()}.")
    
    # Tweet 3: Solution/features
    if len(sentences) > 1:
        thread.append(f"{sentences[1].strip()}.")
    
    # Tweet 4: CTA
    thread.append(f"{cta} 👇")
    
    return thread

def generate_social_captions(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> Dict[str, List[str]]:
    """Generate social media captions for different platforms"""
    
    captions = {}
    
    # Generate Instagram captions
    captions["instagram"] = generate_instagram_captions(
        content_strategy, target_audience, brand_tone
    )
    
    # Generate TikTok captions
    captions["tiktok"] = generate_tiktok_captions(
        content_strategy, target_audience, brand_tone
    )
    
    # Generate LinkedIn captions
    captions["linkedin"] = generate_linkedin_captions(
        content_strategy, target_audience, brand_tone
    )
    
    return captions

def generate_instagram_captions(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[str]:
    """Generate Instagram-specific captions"""
    
    caption_prompt = get_social_caption_prompt(
        platform="instagram",
        content_strategy=content_strategy,
        target_audience=target_audience,
        brand_tone=brand_tone
    )
    
    caption_response = get_llm_response(
        prompt=caption_prompt,
        system_message="You are an expert Instagram content creator. Create engaging, authentic captions that drive engagement and align with current trends."
    )
    
    # Parse multiple captions from response
    captions = parse_social_captions(caption_response, "instagram")
    
    return captions

def generate_tiktok_captions(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[str]:
    """Generate TikTok-specific captions"""
    
    caption_prompt = get_social_caption_prompt(
        platform="tiktok",
        content_strategy=content_strategy,
        target_audience=target_audience,
        brand_tone=brand_tone
    )
    
    caption_response = get_llm_response(
        prompt=caption_prompt,
        system_message="You are an expert TikTok content creator. Create trendy, engaging captions that resonate with TikTok culture and drive views."
    )
    
    captions = parse_social_captions(caption_response, "tiktok")
    
    return captions

def generate_linkedin_captions(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[str]:
    """Generate LinkedIn-specific captions"""
    
    caption_prompt = get_social_caption_prompt(
        platform="linkedin",
        content_strategy=content_strategy,
        target_audience=target_audience,
        brand_tone=brand_tone
    )
    
    caption_response = get_llm_response(
        prompt=caption_prompt,
        system_message="You are an expert LinkedIn content strategist. Create professional, value-driven captions that establish thought leadership and drive business engagement."
    )
    
    captions = parse_social_captions(caption_response, "linkedin")
    
    return captions

def parse_social_captions(caption_text: str, platform: str) -> List[str]:
    """Parse social media captions from LLM response"""
    
    captions = []
    
    # Split by common separators
    potential_captions = []
    
    # Try different splitting methods
    if "Caption 1:" in caption_text:
        sections = caption_text.split("Caption ")
        for section in sections[1:]:  # Skip first empty section
            if ':' in section:
                caption = section.split(':', 1)[1].strip()
                potential_captions.append(caption)
    elif "\n\n" in caption_text:
        potential_captions = caption_text.split('\n\n')
    else:
        # Single caption
        potential_captions = [caption_text]
    
    # Clean and validate captions
    for caption in potential_captions[:3]:  # Limit to 3 captions
        clean_caption = caption.strip()
        
        # Remove any remaining numbering or formatting
        if clean_caption.startswith(('1.', '2.', '3.', '-', '*')):
            clean_caption = clean_caption[2:].strip()
        
        # Platform-specific validation and optimization
        if platform == "instagram" and len(clean_caption) > 2200:
            clean_caption = clean_caption[:2200] + "..."
        elif platform == "tiktok" and len(clean_caption) > 300:
            clean_caption = clean_caption[:300] + "..."
        elif platform == "linkedin" and len(clean_caption) > 3000:
            clean_caption = clean_caption[:3000] + "..."
        
        if clean_caption and len(clean_caption) > 10:  # Minimum length check
            captions.append(clean_caption)
    
    # Ensure we have at least one caption
    if not captions:
        default_captions = {
            "instagram": "✨ Discover something amazing! What do you think? Drop a comment below! #innovation #lifestyle #quality",
            "tiktok": "This changes everything! 🤯 Have you tried this? #fyp #viral #gamechange",
            "linkedin": "Here's an insight that could transform how you approach your goals. What's your experience with this? Share your thoughts in the comments."
        }
        captions.append(default_captions.get(platform, "Check this out! What are your thoughts?"))
    
    return captions
