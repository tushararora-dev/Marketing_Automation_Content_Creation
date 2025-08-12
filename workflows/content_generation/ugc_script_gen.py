from typing import Dict, Any, List
from tools.llm_manager import get_llm_response

def generate_ugc_scripts(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[Dict[str, Any]]:
    """
    Generate User Generated Content (UGC) scripts for video content
    
    Args:
        content_strategy: Content strategy and requirements
        target_audience: Target audience description
        brand_tone: Brand tone/voice
    
    Returns:
        List of UGC scripts with different styles and purposes
    """
    
    ugc_scripts = []
    
    # Generate different types of UGC scripts
    script_types = [
        {
            "type": "testimonial",
            "duration": "30 seconds",
            "purpose": "Build trust and social proof"
        },
        {
            "type": "product_demo",
            "duration": "45 seconds", 
            "purpose": "Show product in action"
        },
        {
            "type": "unboxing",
            "duration": "60 seconds",
            "purpose": "Create excitement and anticipation"
        },
        {
            "type": "before_after",
            "duration": "30 seconds",
            "purpose": "Demonstrate transformation"
        }
    ]
    
    for script_type in script_types:
        script = generate_single_ugc_script(
            content_strategy=content_strategy,
            target_audience=target_audience,
            brand_tone=brand_tone,
            script_type=script_type["type"],
            duration=script_type["duration"],
            purpose=script_type["purpose"]
        )
        ugc_scripts.append(script)
    
    return ugc_scripts

def generate_single_ugc_script(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str,
    script_type: str,
    duration: str,
    purpose: str
) -> Dict[str, Any]:
    """Generate a single UGC script"""
    
    # Build UGC script generation prompt
    script_prompt = create_ugc_script_prompt(
        content_strategy=content_strategy,
        target_audience=target_audience,
        brand_tone=brand_tone,
        script_type=script_type,
        duration=duration,
        purpose=purpose
    )
    
    # Get script from LLM
    script_response = get_llm_response(
        prompt=script_prompt,
        system_message="You are an expert UGC content creator who specializes in authentic, engaging video scripts that feel natural and convert viewers into customers."
    )
    
    # Parse and structure the script
    ugc_script = parse_ugc_script_response(
        script_response, script_type, duration, purpose
    )
    
    return ugc_script

def create_ugc_script_prompt(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str,
    script_type: str,
    duration: str,
    purpose: str
) -> str:
    """Create a detailed prompt for UGC script generation"""
    
    product_description = content_strategy.get("product_description", "product")
    content_pillars = content_strategy.get("content_pillars", [])
    key_messages = content_strategy.get("key_messages", [])
    
    prompt = f"""
    Create a UGC (User Generated Content) video script for {script_type}.
    
    Product/Service: {product_description}
    Target Audience: {target_audience}
    Brand Tone: {brand_tone}
    Script Type: {script_type}
    Duration: {duration}
    Purpose: {purpose}
    Content Pillars: {', '.join(content_pillars)}
    Key Messages: {', '.join(key_messages)}
    
    Script Requirements:
    1. Authentic, conversational tone (not overly promotional)
    2. Natural speech patterns and realistic dialogue
    3. Clear structure with hook, content, and call-to-action
    4. Specific visual directions and actions
    5. Timing cues for pacing
    6. Platform optimization (TikTok/Instagram style)
    7. Relatable scenarios for target audience
    8. Natural product integration
    
    Format the script with:
    - Timeline/timing cues
    - Spoken dialogue/narration
    - Visual directions
    - Props/setup requirements
    - Editing notes
    """
    
    # Add script-type specific requirements
    type_specific = get_ugc_type_requirements(script_type, product_description)
    prompt += f"\n\nSpecific Requirements for {script_type}:\n{type_specific}"
    
    return prompt

def get_ugc_type_requirements(script_type: str, product_description: str) -> str:
    """Get specific requirements for different UGC script types"""
    
    requirements = {
        "testimonial": f"""
        - Start with personal story/problem
        - Show genuine emotion and enthusiasm
        - Mention specific benefits experienced
        - Include before/after if applicable
        - Natural, unrehearsed feeling
        - End with strong recommendation
        - Use real-person language, not marketing speak
        """,
        
        "product_demo": f"""
        - Show actual product usage in real environment
        - Demonstrate key features naturally
        - Include setup or preparation steps
        - Show results or outcomes
        - Address common questions or concerns
        - Multiple angles and close-ups
        - Natural mistakes or adjustments (authenticity)
        """,
        
        "unboxing": f"""
        - Build anticipation at the beginning
        - Show packaging and first impressions
        - React authentically to each item
        - Explain what you're seeing/feeling
        - Highlight unexpected positives
        - Show size, texture, quality details
        - End with overall impression and excitement
        """,
        
        "before_after": f"""
        - Clear documentation of starting point
        - Show the process or usage period
        - Document journey/timeline
        - Reveal transformation dramatically
        - Express genuine surprise/satisfaction
        - Compare side-by-side if possible
        - Explain what made the difference
        """
    }
    
    return requirements.get(script_type, f"Show authentic usage of {product_description}")

def parse_ugc_script_response(
    script_text: str, 
    script_type: str, 
    duration: str, 
    purpose: str
) -> Dict[str, Any]:
    """Parse UGC script response into structured format"""
    
    ugc_script = {
        "type": script_type,
        "title": generate_script_title(script_type, script_text),
        "duration": duration,
        "purpose": purpose,
        "script": script_text,
        "dialogue": extract_dialogue(script_text),
        "visual_directions": extract_visual_directions(script_text),
        "timing_cues": extract_timing_cues(script_text),
        "props_needed": extract_props_needed(script_text),
        "setup_requirements": extract_setup_requirements(script_text),
        "editing_notes": extract_editing_notes(script_text),
        "platform_versions": create_platform_versions(script_text, script_type),
        "authenticity_tips": get_authenticity_tips(script_type),
        "full_script": script_text
    }
    
    return ugc_script

def generate_script_title(script_type: str, script_text: str) -> str:
    """Generate a catchy title for the UGC script"""
    
    # Look for title in the script text
    # lines = script_text.split('\n')
    # for line in lines[:5]:
    #     if 'title:' in line.lower():
    #         return line.split(':', 1)[1].strip()
    
    # Generate based on script type
    titles = {
        "testimonial": "My Honest Review",
        "product_demo": "Let Me Show You How This Works",
        "unboxing": "Unboxing My New Favorite Thing",
        "before_after": "The Results Speak for Themselves"
    }
    
    return titles.get(script_type, f"{script_type.title()} Script")

def extract_dialogue(script_text: str) -> List[Dict[str, str]]:
    """Extract dialogue/narration from script"""
    
    dialogue = []
    lines = script_text.split('\n')
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        # Look for spoken content (usually in quotes or after timing)
        if line_clean.startswith('"') and line_clean.endswith('"'):
            dialogue.append({
                "timing": extract_timing_from_context(lines, i),
                "text": line_clean.strip('"'),
                "tone": "natural, conversational"
            })
        elif ':' in line_clean and any(word in line_clean.lower() for word in ['say', 'speak', 'talk']):
            text = line_clean.split(':', 1)[1].strip()
            dialogue.append({
                "timing": extract_timing_from_context(lines, i),
                "text": text,
                "tone": "natural, conversational"
            })
    
    # If no specific dialogue found, extract key speaking points
    if not dialogue:
        dialogue = extract_key_speaking_points(script_text)
    
    return dialogue

def extract_timing_from_context(lines: List[str], current_index: int) -> str:
    """Extract timing context from surrounding lines"""
    
    # Look for timing cues in nearby lines
    for i in range(max(0, current_index - 2), min(len(lines), current_index + 3)):
        line = lines[i].lower()
        if any(time_word in line for time_word in ['seconds', 'sec', ':', 'start', 'beginning', 'end']):
            return lines[i].strip()
    
    return "TBD"

def extract_key_speaking_points(script_text: str) -> List[Dict[str, str]]:
    """Extract key speaking points when dialogue isn't clearly marked"""
    
    # Find sentences that sound like spoken content
    sentences = script_text.split('.')
    speaking_points = []
    
    for sentence in sentences:
        sentence_clean = sentence.strip()
        if len(sentence_clean) > 20 and not sentence_clean.lower().startswith(('cut to', 'show', 'camera', 'edit')):
            speaking_points.append({
                "timing": "TBD",
                "text": sentence_clean,
                "tone": "natural, conversational"
            })
    
    return speaking_points[:5]  # Limit to 5 main points

def extract_visual_directions(script_text: str) -> List[str]:
    """Extract visual directions and camera instructions"""
    
    visual_directions = []
    lines = script_text.split('\n')
    
    # Keywords that indicate visual directions
    visual_keywords = [
        'show', 'camera', 'close-up', 'wide shot', 'zoom', 'cut to',
        'display', 'reveal', 'focus on', 'angle', 'shot', 'frame'
    ]
    
    for line in lines:
        line_clean = line.strip().lower()
        if any(keyword in line_clean for keyword in visual_keywords):
            visual_directions.append(line.strip())
    
    # Add default visual directions if none found
    if not visual_directions:
        visual_directions = [
            "Start with medium shot of person",
            "Show product prominently in frame",
            "Include close-ups of key features",
            "End with wide shot showing results"
        ]
    
    return visual_directions

def extract_timing_cues(script_text: str) -> List[Dict[str, str]]:
    """Extract timing and pacing cues"""
    
    timing_cues = []
    lines = script_text.split('\n')
    
    # Look for timing indicators
    timing_indicators = ['0:', '1:', '2:', 'seconds', 'sec', 'start', 'end', 'beginning']
    
    for line in lines:
        line_lower = line.lower()
        if any(indicator in line_lower for indicator in timing_indicators):
            timing_cues.append({
                "timing": extract_time_value(line),
                "action": line.strip(),
                "importance": "critical"
            })
    
    # Add default timing structure
    if not timing_cues:
        timing_cues = [
            {"timing": "0-3 sec", "action": "Hook - grab attention", "importance": "critical"},
            {"timing": "3-15 sec", "action": "Main content - demonstrate/explain", "importance": "high"},
            {"timing": "15+ sec", "action": "Call to action - encourage engagement", "importance": "critical"}
        ]
    
    return timing_cues

def extract_time_value(text: str) -> str:
    """Extract time value from text"""
    
    import re
    
    # Look for time patterns
    time_patterns = [r'\d+:\d+', r'\d+\s*sec', r'\d+-\d+', r'\d+s']
    
    for pattern in time_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    
    return "TBD"

def extract_props_needed(script_text: str) -> List[str]:
    """Extract props and materials needed for the video"""
    
    props = []
    
    # Look for prop-related keywords
    prop_keywords = ['prop', 'need', 'use', 'grab', 'hold', 'wear', 'setup']
    
    lines = script_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in prop_keywords) and 'product' in line_lower:
            props.append(line.strip())
    
    # Add common UGC props
    common_props = [
        "The actual product",
        "Good lighting setup",
        "Clean background",
        "Phone or camera for recording"
    ]
    
    props.extend(common_props)
    
    return list(set(props))  # Remove duplicates

def extract_setup_requirements(script_text: str) -> List[str]:
    """Extract setup and preparation requirements"""
    
    setup_requirements = []
    
    # Look for setup-related content
    setup_keywords = ['setup', 'prepare', 'before', 'location', 'lighting', 'background']
    
    lines = script_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in setup_keywords):
            setup_requirements.append(line.strip())
    
    # Add standard UGC setup requirements
    standard_setup = [
        "Ensure good natural lighting or ring light",
        "Choose clean, uncluttered background",
        "Test audio quality and minimize background noise",
        "Have product easily accessible and ready to use",
        "Charge phone/camera and clear storage space"
    ]
    
    setup_requirements.extend(standard_setup)
    
    return setup_requirements

def extract_editing_notes(script_text: str) -> List[str]:
    """Extract editing and post-production notes"""
    
    editing_notes = []
    
    # Look for editing-related instructions
    edit_keywords = ['edit', 'cut', 'transition', 'music', 'sound', 'caption', 'text']
    
    lines = script_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in edit_keywords):
            editing_notes.append(line.strip())
    
    # Add standard UGC editing notes
    standard_edits = [
        "Keep cuts snappy and engaging",
        "Add captions for accessibility",
        "Include trending music if appropriate",
        "Maintain authentic, unpolished feel",
        "Add subtle text overlays for key points"
    ]
    
    editing_notes.extend(standard_edits)
    
    return editing_notes

def create_platform_versions(script_text: str, script_type: str) -> Dict[str, Dict[str, Any]]:
    """Create platform-specific versions of UGC scripts"""
    
    platforms = {
        "tiktok": {
            "max_duration": "30 seconds",
            "style": "Fast-paced, trendy, music-driven",
            "captions": "Essential for engagement",
            "hashtags": "Use trending + niche hashtags",
            "format": "Vertical 9:16",
            "hook_timing": "First 1-2 seconds critical"
        },
        "instagram_reels": {
            "max_duration": "30 seconds",
            "style": "Polished but authentic",
            "captions": "Stylized text overlays",
            "hashtags": "Mix of popular and niche",
            "format": "Vertical 9:16",
            "hook_timing": "First 3 seconds"
        },
        "youtube_shorts": {
            "max_duration": "60 seconds",
            "style": "More detailed, educational angle",
            "captions": "Clear, easy to read",
            "description": "Detailed with keywords",
            "format": "Vertical 9:16",
            "seo": "Optimize title and description"
        },
        "facebook": {
            "max_duration": "90 seconds",
            "style": "Community-focused, story-driven",
            "captions": "Auto-play friendly",
            "format": "Square 1:1 or vertical",
            "engagement": "Encourage comments and shares"
        }
    }
    
    return platforms

def get_authenticity_tips(script_type: str) -> List[str]:
    """Get tips for maintaining authenticity in UGC content"""
    
    general_tips = [
        "Use natural speech patterns and filler words occasionally",
        "Show genuine reactions and emotions",
        "Include minor imperfections or adjustments",
        "Speak as you would to a friend",
        "Share personal context or story"
    ]
    
    type_specific_tips = {
        "testimonial": [
            "Share specific details about your experience",
            "Mention how long you've been using the product",
            "Include what you were skeptical about initially",
            "Be honest about any minor drawbacks"
        ],
        "product_demo": [
            "Show the learning curve or setup process",
            "Include your thought process while using",
            "Demonstrate in your actual environment",
            "Show different ways to use the product"
        ],
        "unboxing": [
            "React naturally to packaging and presentation",
            "Share your expectations vs. reality",
            "Touch and examine items genuinely",
            "Compare to similar products you've used"
        ],
        "before_after": [
            "Document the actual timeline honestly",
            "Show the process, not just results",
            "Include challenges or setbacks",
            "Explain what you did differently"
        ]
    }
    
    tips = general_tips + type_specific_tips.get(script_type, [])
    
    return tips

def generate_ugc_content_calendar(ugc_scripts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a content calendar for UGC scripts"""
    
    calendar = {
        "week_1": {
            "monday": {"script": "testimonial", "platform": "instagram_reels"},
            "wednesday": {"script": "product_demo", "platform": "tiktok"},
            "friday": {"script": "unboxing", "platform": "youtube_shorts"}
        },
        "week_2": {
            "monday": {"script": "before_after", "platform": "facebook"},
            "wednesday": {"script": "testimonial", "platform": "tiktok"},
            "friday": {"script": "product_demo", "platform": "instagram_reels"}
        },
        "posting_tips": [
            "Post during peak engagement hours for your audience",
            "Engage with comments within first hour",
            "Cross-promote on other platforms",
            "Track performance metrics for optimization"
        ]
    }
    
    return calendar
