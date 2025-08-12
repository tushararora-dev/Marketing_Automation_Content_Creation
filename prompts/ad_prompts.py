from typing import Dict, Any, List

def get_ad_copy_prompt(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str,
    variant_number: int
) -> str:
    """
    Generate comprehensive prompt for ad copy creation
    
    Args:
        content_strategy: Content strategy and requirements
        target_audience: Target audience description
        brand_tone: Brand tone/voice
        variant_number: Ad copy variant number
    
    Returns:
        Detailed prompt for ad copy generation
    """
    
    product_description = content_strategy.get("product_description", "product")
    content_pillars = content_strategy.get("content_pillars", [])
    key_messages = content_strategy.get("key_messages", [])
    
    prompt = f"""
    Create high-converting ad copy (Variant #{variant_number}) for the following product/service.
    
    PRODUCT/SERVICE DETAILS:
    - Product/Service: {product_description}
    - Target Audience: {target_audience}
    - Brand Tone: {brand_tone}
    - Content Pillars: {', '.join(content_pillars)}
    - Key Messages: {', '.join(key_messages)}
    
    AD COPY REQUIREMENTS:
    1. Headline: Attention-grabbing headline (25-40 characters for mobile)
    2. Primary Text: Compelling body copy (150-200 words maximum)
    3. Call-to-Action: Clear, action-oriented CTA (2-5 words)
    4. Description: Supporting description (30-90 characters)
    
    COPY PRINCIPLES:
    - Hook: Start with attention-grabbing opening
    - Problem/Solution: Address customer pain points
    - Benefits: Focus on customer benefits, not just features
    - Social Proof: Include credibility indicators
    - Urgency: Create appropriate urgency
    - Clarity: Use simple, clear language
    
    TONE GUIDELINES:
    - {brand_tone}: Maintain {brand_tone.lower()} tone throughout
    - Audience-appropriate: Match {target_audience} expectations
    - Benefit-focused: Emphasize value to customer
    - Action-oriented: Drive specific actions
    
    PLATFORM CONSIDERATIONS:
    - Facebook/Instagram: Conversational, visual storytelling
    - Google Ads: Search intent focused, solution-oriented
    - LinkedIn: Professional, value-driven, B2B appropriate
    - Twitter: Concise, trending, shareable
    
    PERSUASION TECHNIQUES:
    {get_persuasion_techniques(variant_number)}
    
    TARGET AUDIENCE INSIGHTS:
    {get_audience_insights(target_audience)}
    
    OUTPUT FORMAT:
    Headline: [Your headline here]
    Primary Text: [Your primary text here]
    CTA: [Your call-to-action here]
    Description: [Your description here]
    
    Create ad copy that resonates with {target_audience} and drives conversions.
    """
    
    return prompt

def get_social_caption_prompt(
    platform: str,
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> str:
    """
    Generate prompt for social media caption creation
    
    Args:
        platform: Social media platform (instagram, tiktok, linkedin, etc.)
        content_strategy: Content strategy and requirements
        target_audience: Target audience description
        brand_tone: Brand tone/voice
    
    Returns:
        Platform-specific prompt for social caption generation
    """
    
    product_description = content_strategy.get("product_description", "product")
    content_pillars = content_strategy.get("content_pillars", [])
    
    platform_specs = get_platform_specifications(platform)
    
    prompt = f"""
    Create engaging {platform.title()} captions for the following product/service.
    
    PRODUCT/SERVICE DETAILS:
    - Product/Service: {product_description}
    - Target Audience: {target_audience}
    - Brand Tone: {brand_tone}
    - Content Pillars: {', '.join(content_pillars)}
    
    PLATFORM: {platform.upper()}
    {platform_specs}
    
    CAPTION REQUIREMENTS:
    1. Hook: Attention-grabbing opening line
    2. Value: Clear value proposition
    3. Engagement: Encourage interaction
    4. Hashtags: Relevant and trending hashtags
    5. CTA: Clear call-to-action
    
    CONTENT STYLE:
    - {brand_tone}: Maintain {brand_tone.lower()} voice
    - Authentic: Sound genuine and relatable
    - Engaging: Encourage comments and shares
    - Visual: Reference visual elements
    - Community: Build sense of community
    
    ENGAGEMENT TACTICS:
    {get_engagement_tactics(platform)}
    
    PLATFORM BEST PRACTICES:
    {get_platform_best_practices(platform)}

    IMPORTANT:
    Only output the captions exactly in the format below.
    Do NOT include any explanations, summaries, or additional text.
    
    OUTPUT FORMAT:
    Caption 1:
    [Your first caption here]
    #hashtag1 #hashtag2 #hashtag3
    
    Caption 2:
    [Your second caption here]
    #hashtag1 #hashtag2 #hashtag3
    
    Caption 3:
    [Your third caption here]
    #hashtag1 #hashtag2 #hashtag3
    
    Create captions that drive engagement and align with {platform} culture.
    """
    
    return prompt

def get_persuasion_techniques(variant_number: int) -> str:
    """Get persuasion techniques based on variant number"""
    
    techniques = {
        1: """
        - Social Proof: Use testimonials, reviews, or user count
        - Scarcity: Limited time offers or limited quantities
        - Authority: Expert endorsements or certifications
        """,
        2: """
        - Reciprocity: Offer something valuable first
        - Commitment: Get small commitments leading to larger ones
        - Liking: Show similarity and shared values
        """,
        3: """
        - Loss Aversion: Focus on what they'll miss out on
        - Urgency: Time-sensitive offers and deadlines
        - Contrast: Compare to alternatives or previous state
        """
    }
    
    return techniques.get(variant_number, techniques[1])

def get_audience_insights(target_audience: str) -> str:
    """Get insights about target audience for better targeting"""
    
    audience_lower = target_audience.lower()
    
    if "small business" in audience_lower:
        return """
        - Pain Points: Limited budget, time constraints, need for ROI
        - Motivations: Growth, efficiency, competitive advantage
        - Language: Professional but approachable, ROI-focused
        - Channels: LinkedIn, Google, industry publications
        """
    elif "enterprise" in audience_lower:
        return """
        - Pain Points: Complex processes, security concerns, scalability
        - Motivations: Innovation, competitive edge, risk mitigation
        - Language: Professional, technical, strategic
        - Channels: LinkedIn, industry events, B2B publications
        """
    elif "consumer" in audience_lower or "general" in audience_lower:
        return """
        - Pain Points: Price sensitivity, time constraints, trust issues
        - Motivations: Convenience, value, social status
        - Language: Conversational, benefit-focused, relatable
        - Channels: Facebook, Instagram, Google, TikTok
        """
    elif "professional" in audience_lower:
        return """
        - Pain Points: Career advancement, skill development, efficiency
        - Motivations: Professional growth, recognition, expertise
        - Language: Professional yet personal, achievement-focused
        - Channels: LinkedIn, industry forums, professional networks
        """
    else:
        return """
        - Pain Points: Varies by specific audience segment
        - Motivations: Value, convenience, quality, trust
        - Language: Clear, benefit-focused, audience-appropriate
        - Channels: Multi-channel approach recommended
        """

def get_platform_specifications(platform: str) -> str:
    """Get platform-specific specifications and requirements"""
    
    specs = {
        "instagram": """
        - Character Limit: 2,200 characters
        - Optimal Length: 138-150 characters for best engagement
        - Hashtags: 5-10 relevant hashtags (up to 30 allowed)
        - Format: Visual storytelling, behind-the-scenes, lifestyle
        - Best Times: 11 AM - 2 PM, 5 PM - 7 PM
        """,
        "tiktok": """
        - Character Limit: 300 characters
        - Optimal Length: Under 100 characters
        - Hashtags: 3-5 trending + niche hashtags
        - Format: Trendy, entertaining, authentic, music-driven
        - Best Times: 6 AM - 10 AM, 7 PM - 9 PM
        """,
        "linkedin": """
        - Character Limit: 3,000 characters
        - Optimal Length: 150-300 characters for posts
        - Hashtags: 3-5 professional hashtags
        - Format: Professional insights, industry news, thought leadership
        - Best Times: 8 AM - 10 AM, 12 PM - 2 PM
        """,
        "facebook": """
        - Character Limit: 63,206 characters
        - Optimal Length: 40-80 characters for best engagement
        - Hashtags: 1-2 hashtags (less emphasis than other platforms)
        - Format: Community-building, storytelling, user-generated content
        - Best Times: 9 AM - 10 AM, 3 PM - 4 PM
        """,
        "twitter": """
        - Character Limit: 280 characters
        - Optimal Length: 100-280 characters
        - Hashtags: 1-2 hashtags maximum
        - Format: News, real-time updates, conversations, threads
        - Best Times: 8 AM - 10 AM, 6 PM - 9 PM
        """
    }
    
    return specs.get(platform, "Standard social media best practices apply")

def get_engagement_tactics(platform: str) -> str:
    """Get platform-specific engagement tactics"""
    
    tactics = {
        "instagram": """
        - Ask questions in captions
        - Use Instagram Stories polls and questions
        - Encourage user-generated content with branded hashtags
        - Share behind-the-scenes content
        - Use location tags and tag relevant accounts
        """,
        "tiktok": """
        - Use trending sounds and effects
        - Participate in challenges and trends
        - Ask viewers to duet or stitch your content
        - Use trending hashtags strategically
        - Create educational or entertaining content
        """,
        "linkedin": """
        - Share industry insights and professional tips
        - Ask for opinions on industry topics
        - Share company culture and team highlights
        - Post case studies and success stories
        - Engage in meaningful professional discussions
        """,
        "facebook": """
        - Create community-focused content
        - Share user testimonials and reviews
        - Host live Q&As and events
        - Create shareable, relatable content
        - Use Facebook Groups for deeper engagement
        """,
        "twitter": """
        - Join trending conversations
        - Create Twitter threads for detailed content
        - Retweet and comment on relevant content
        - Use Twitter Spaces for audio conversations
        - Share real-time updates and news
        """
    }
    
    return tactics.get(platform, "Focus on authentic engagement and community building")

def get_platform_best_practices(platform: str) -> str:
    """Get platform-specific best practices"""
    
    practices = {
        "instagram": """
        - Post consistently (1-2 times per day)
        - Use high-quality visuals
        - Mix content types (photos, videos, carousels, Stories)
        - Engage with followers within 1-2 hours of posting
        - Use Instagram Shopping features for products
        """,
        "tiktok": """
        - Post 1-4 times per day
        - Keep videos under 30 seconds for best performance
        - Use vertical video format (9:16)
        - Jump on trends quickly while they're hot
        - Collaborate with other creators
        """,
        "linkedin": """
        - Post 2-3 times per week
        - Share valuable, professional content
        - Use professional headshots and company branding
        - Engage thoughtfully with connections
        - Share articles and industry insights
        """,
        "facebook": """
        - Post 1-2 times per day
        - Use Facebook Insights to optimize timing
        - Create event pages for promotions
        - Use Facebook Live for real-time engagement
        - Cross-post to Instagram when appropriate
        """,
        "twitter": """
        - Tweet 3-5 times per day
        - Use Twitter Lists to organize and monitor
        - Participate in Twitter chats
        - Retweet with commentary to add value
        - Use Twitter Analytics to track performance
        """
    }
    
    return practices.get(platform, "Follow general social media best practices")

def get_hashtag_strategies() -> Dict[str, List[str]]:
    """Get hashtag strategies for different platforms"""
    
    return {
        "instagram": [
            "Mix popular and niche hashtags",
            "Use 5-10 hashtags for optimal reach",
            "Create branded hashtags for campaigns",
            "Research competitor hashtags",
            "Use location-based hashtags"
        ],
        "tiktok": [
            "Use trending hashtags while relevant",
            "Mix trending with niche hashtags",
            "Create challenge hashtags",
            "Use 3-5 hashtags maximum",
            "Monitor hashtag performance"
        ],
        "linkedin": [
            "Use professional industry hashtags",
            "Limit to 3-5 hashtags",
            "Focus on niche professional topics",
            "Avoid overly broad hashtags",
            "Use company and event hashtags"
        ],
        "twitter": [
            "Use 1-2 hashtags maximum",
            "Join trending conversations",
            "Create event-specific hashtags",
            "Use hashtags in Twitter chats",
            "Monitor hashtag conversations"
        ]
    }

def create_content_calendar_prompts(timeframe: str) -> List[str]:
    """Create prompts for content calendar planning"""
    
    if timeframe == "weekly":
        return [
            "Create Monday motivation content",
            "Design Tuesday tips or tutorials", 
            "Develop Wednesday wisdom or insights",
            "Generate Thursday throwback or testimonials",
            "Plan Friday fun or behind-the-scenes content",
            "Schedule Saturday lifestyle or community content",
            "Prepare Sunday reflection or inspiration"
        ]
    elif timeframe == "monthly":
        return [
            "Week 1: Product launch and announcements",
            "Week 2: Educational content and tutorials",
            "Week 3: User-generated content and testimonials", 
            "Week 4: Community engagement and Q&A"
        ]
    else:
        return [
            "Create consistent daily content themes",
            "Plan seasonal and holiday content",
            "Develop evergreen content pillars",
            "Schedule promotional content strategically"
        ]

def get_conversion_optimization_tips() -> List[str]:
    """Get tips for optimizing ad copy for conversions"""
    
    return [
        "Use action-oriented verbs in headlines",
        "Address specific customer pain points",
        "Include clear value propositions",
        "Create urgency without being pushy",
        "Use social proof and testimonials",
        "Test different CTA buttons and text",
        "Optimize for mobile viewing",
        "A/B test headlines and descriptions",
        "Use emotional triggers appropriately",
        "Include clear next steps for users"
    ]

def get_brand_voice_guidelines(brand_tone: str) -> Dict[str, Any]:
    """Get detailed brand voice guidelines"""
    
    guidelines = {
        "professional": {
            "characteristics": ["Expert", "Reliable", "Authoritative", "Respectful"],
            "language": ["Industry terminology", "Formal structure", "Clear communication"],
            "avoid": ["Slang", "Overly casual language", "Humor that undermines authority"],
            "examples": ["We provide comprehensive solutions", "Our expertise ensures success"]
        },
        "casual": {
            "characteristics": ["Friendly", "Approachable", "Conversational", "Relatable"],
            "language": ["Everyday words", "Contractions", "Personal pronouns"],
            "avoid": ["Overly formal language", "Jargon", "Corporate speak"],
            "examples": ["We're here to help", "Let's figure this out together"]
        },
        "playful": {
            "characteristics": ["Fun", "Creative", "Energetic", "Memorable"],
            "language": ["Humor", "Wordplay", "Pop culture references", "Emojis"],
            "avoid": ["Being too serious", "Boring language", "Overly corporate"],
            "examples": ["Ready to rock your world?", "This is going to be awesome!"]
        },
        "luxury": {
            "characteristics": ["Sophisticated", "Exclusive", "Premium", "Elegant"],
            "language": ["Refined vocabulary", "Quality descriptors", "Exclusivity"],
            "avoid": ["Common language", "Discount messaging", "Mass market appeal"],
            "examples": ["Exclusively crafted", "Unparalleled excellence"]
        }
    }
    
    return guidelines.get(brand_tone.lower(), guidelines["professional"])
