from typing import Dict, Any, List
from tools.video_editor_api import create_video_content, edit_video_clips
from tools.llm_manager import get_llm_response

def generate_video_content(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str
) -> List[Dict[str, Any]]:
    """
    Generate video content including scripts and editing instructions
    
    Args:
        content_strategy: Content strategy and requirements
        target_audience: Target audience description
        brand_tone: Brand tone/voice
    
    Returns:
        List of video content with scripts, editing instructions, and metadata
    """
    
    videos = []
    
    # Generate different types of video content
    video_types = [
        {"type": "product_demo", "duration": "30-60 seconds"},
        {"type": "testimonial", "duration": "15-30 seconds"},
        {"type": "behind_scenes", "duration": "30-45 seconds"}
    ]
    
    for video_type in video_types:
        video = generate_single_video_content(
            content_strategy=content_strategy,
            target_audience=target_audience,
            brand_tone=brand_tone,
            video_type=video_type["type"],
            duration=video_type["duration"]
        )
        videos.append(video)
    
    return videos

def generate_single_video_content(
    content_strategy: Dict[str, Any],
    target_audience: str,
    brand_tone: str,
    video_type: str,
    duration: str
) -> Dict[str, Any]:
    """Generate a single video content piece"""
    
    # Create video script prompt
    script_prompt = f"""
    Create a video script for a {video_type} video.
    
    Product/Service: {content_strategy.get('product_description', 'Product')}
    Target Audience: {target_audience}
    Brand Tone: {brand_tone}
    Duration: {duration}
    Content Pillars: {', '.join(content_strategy.get('content_pillars', []))}
    
    Include:
    1. Hook (first 3 seconds)
    2. Main content/demonstration
    3. Call to action
    4. Visual cues and directions
    5. Text overlays suggestions
    6. Music/sound effect suggestions
    
    Format as a detailed video script with timestamps.
    """
    
    # Get script from LLM
    script_response = get_llm_response(
        prompt=script_prompt,
        system_message="You are an expert video content creator specializing in short-form social media videos. Create engaging, platform-optimized video scripts."
    )
    
    # Parse the script
    video = parse_video_script(script_response, video_type, duration)
    
    # Add editing instructions
    video["editing_instructions"] = generate_editing_instructions(video, video_type)
    
    # Add platform optimizations
    video["platform_versions"] = create_platform_versions(video)
    
    return video

def parse_video_script(script_text: str, video_type: str, duration: str) -> Dict[str, Any]:
    """Parse video script from LLM response"""
    
    video = {
        "type": video_type,
        "duration": duration,
        "script": script_text,
        "scenes": extract_scenes(script_text),
        "hook": extract_hook(script_text),
        "cta": extract_video_cta(script_text),
        "visual_cues": extract_visual_cues(script_text),
        "text_overlays": extract_text_overlays(script_text),
        "audio_suggestions": extract_audio_suggestions(script_text),
        "full_script": script_text
    }
    
    return video

def extract_scenes(script_text: str) -> List[Dict[str, Any]]:
    """Extract scenes from video script"""
    
    scenes = []
    lines = script_text.split('\n')
    current_scene = None
    
    for line in lines:
        line_clean = line.strip()
        
        # Look for scene indicators
        if any(indicator in line_clean.lower() for indicator in ['scene', 'shot', 'timestamp', ':']):
            if current_scene:
                scenes.append(current_scene)
            
            # Extract timestamp if present
            timestamp = extract_timestamp(line_clean)
            
            current_scene = {
                "timestamp": timestamp,
                "description": line_clean,
                "content": []
            }
        elif current_scene and line_clean:
            current_scene["content"].append(line_clean)
    
    # Add final scene
    if current_scene:
        scenes.append(current_scene)
    
    # If no scenes found, create default structure
    if not scenes:
        scenes = [
            {
                "timestamp": "0-3s",
                "description": "Hook/Opening",
                "content": [script_text[:100] + "..."]
            },
            {
                "timestamp": "3-15s",
                "description": "Main Content",
                "content": [script_text[100:300] + "..."]
            },
            {
                "timestamp": "15s-end",
                "description": "Call to Action",
                "content": [script_text[-100:]]
            }
        ]
    
    return scenes

def extract_timestamp(text: str) -> str:
    """Extract timestamp from text"""
    
    import re
    
    # Look for timestamp patterns like "0:00-0:03" or "0-3s"
    timestamp_patterns = [
        r'\d+:\d+-\d+:\d+',
        r'\d+-\d+s',
        r'\d+s-\d+s',
        r'Scene \d+',
        r'Shot \d+'
    ]
    
    for pattern in timestamp_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    
    return "0s"

def extract_hook(script_text: str) -> str:
    """Extract the video hook/opening"""
    
    lines = script_text.split('\n')
    
    # Look for hook indicators
    for line in lines:
        line_clean = line.strip()
        if 'hook' in line_clean.lower():
            # Get the next few lines after hook indicator
            hook_lines = []
            start_index = lines.index(line)
            for i in range(start_index + 1, min(start_index + 4, len(lines))):
                if lines[i].strip():
                    hook_lines.append(lines[i].strip())
            return ' '.join(hook_lines)
    
    # Fallback: use first 50 words
    words = script_text.split()[:50]
    return ' '.join(words) + "..."

def extract_video_cta(script_text: str) -> str:
    """Extract call-to-action from video script"""
    
    lines = script_text.split('\n')
    
    # Look for CTA indicators
    cta_indicators = ['cta', 'call to action', 'follow', 'like', 'subscribe', 'buy', 'shop', 'visit']
    
    for line in lines:
        line_lower = line.lower()
        if any(indicator in line_lower for indicator in cta_indicators):
            return line.strip()
    
    # Look for typical CTA phrases
    cta_phrases = ['follow for more', 'link in bio', 'comment below', 'try it now']
    
    for line in lines:
        line_lower = line.lower()
        for phrase in cta_phrases:
            if phrase in line_lower:
                return line.strip()
    
    return "Follow for more amazing content!"

def extract_visual_cues(script_text: str) -> List[str]:
    """Extract visual cues and directions"""
    
    visual_cues = []
    lines = script_text.split('\n')
    
    # Look for visual direction keywords
    visual_keywords = ['show', 'display', 'zoom', 'close-up', 'wide shot', 'cut to', 'transition']
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in visual_keywords):
            visual_cues.append(line.strip())
    
    # Add default visual cues if none found
    if not visual_cues:
        visual_cues = [
            "Start with close-up product shot",
            "Show product in use",
            "Include lifestyle shots",
            "End with brand logo"
        ]
    
    return visual_cues

def extract_text_overlays(script_text: str) -> List[Dict[str, str]]:
    """Extract text overlay suggestions"""
    
    overlays = []
    lines = script_text.split('\n')
    
    # Look for text overlay indicators
    overlay_keywords = ['text:', 'overlay:', 'caption:', 'title:']
    
    for line in lines:
        line_lower = line.lower()
        for keyword in overlay_keywords:
            if keyword in line_lower:
                text = line.split(':', 1)[1].strip()
                overlays.append({
                    "text": text,
                    "timing": "TBD",
                    "style": "bold, white text with shadow"
                })
    
    # Add default overlays
    if not overlays:
        overlays = [
            {"text": "🔥 AMAZING RESULTS", "timing": "0-3s", "style": "large, bold, animated"},
            {"text": "Try it yourself!", "timing": "end", "style": "medium, call-to-action style"}
        ]
    
    return overlays

def extract_audio_suggestions(script_text: str) -> Dict[str, Any]:
    """Extract audio and music suggestions"""
    
    audio = {
        "music_style": "upbeat, modern",
        "sound_effects": [],
        "voice_over": True,
        "music_volume": "background level"
    }
    
    # Look for audio cues in script
    if 'upbeat' in script_text.lower() or 'energetic' in script_text.lower():
        audio["music_style"] = "upbeat, energetic"
    elif 'calm' in script_text.lower() or 'peaceful' in script_text.lower():
        audio["music_style"] = "calm, ambient"
    elif 'dramatic' in script_text.lower():
        audio["music_style"] = "dramatic, cinematic"
    
    # Extract sound effect suggestions
    sound_keywords = ['whoosh', 'pop', 'ding', 'swoosh', 'chime', 'click']
    
    for keyword in sound_keywords:
        if keyword in script_text.lower():
            audio["sound_effects"].append(keyword)
    
    return audio

def generate_editing_instructions(video: Dict[str, Any], video_type: str) -> Dict[str, Any]:
    """Generate detailed editing instructions"""
    
    instructions = {
        "pacing": get_pacing_instructions(video_type),
        "transitions": get_transition_suggestions(video_type),
        "color_grading": get_color_grading_instructions(video_type),
        "cuts": get_cutting_instructions(video),
        "effects": get_effects_suggestions(video_type),
        "aspect_ratios": {
            "instagram_feed": "1:1",
            "instagram_story": "9:16",
            "tiktok": "9:16",
            "youtube_shorts": "9:16",
            "facebook": "16:9 or 1:1"
        }
    }
    
    return instructions

def get_pacing_instructions(video_type: str) -> str:
    """Get pacing instructions based on video type"""
    
    pacing_guide = {
        "product_demo": "Fast-paced with quick cuts every 2-3 seconds to maintain attention",
        "testimonial": "Moderate pacing with longer cuts to build trust and credibility",
        "behind_scenes": "Relaxed pacing with natural flow, cuts every 4-5 seconds"
    }
    
    return pacing_guide.get(video_type, "Moderate pacing appropriate for content type")

def get_transition_suggestions(video_type: str) -> List[str]:
    """Get transition suggestions"""
    
    transitions = {
        "product_demo": ["Quick cuts", "Zoom transitions", "Slide transitions"],
        "testimonial": ["Fade transitions", "Simple cuts", "Cross dissolve"],
        "behind_scenes": ["Natural cuts", "Match cuts", "Jump cuts"]
    }
    
    return transitions.get(video_type, ["Simple cuts", "Fade transitions"])

def get_color_grading_instructions(video_type: str) -> str:
    """Get color grading instructions"""
    
    color_guides = {
        "product_demo": "Bright, vibrant colors to showcase product appeal",
        "testimonial": "Warm, natural colors to enhance trustworthiness",
        "behind_scenes": "Authentic, slightly desaturated for genuine feel"
    }
    
    return color_guides.get(video_type, "Balanced, natural color grading")

def get_cutting_instructions(video: Dict[str, Any]) -> List[str]:
    """Get cutting instructions based on content"""
    
    instructions = [
        "Cut on action to maintain flow",
        "Use jump cuts to remove dead space",
        "Match audio with visual beats",
        "Keep cuts tight for social media attention spans"
    ]
    
    # Add specific instructions based on scenes
    scenes = video.get("scenes", [])
    if len(scenes) > 3:
        instructions.append("Ensure smooth transitions between multiple scenes")
    
    return instructions

def get_effects_suggestions(video_type: str) -> List[str]:
    """Get visual effects suggestions"""
    
    effects = {
        "product_demo": ["Speed ramping", "Zoom effects", "Text animations"],
        "testimonial": ["Subtle zoom", "Color correction", "Audio cleanup"],
        "behind_scenes": ["Natural stabilization", "Light color correction"]
    }
    
    return effects.get(video_type, ["Basic color correction", "Audio optimization"])

def create_platform_versions(video: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Create platform-specific versions of video content"""
    
    platforms = {
        "tiktok": {
            "aspect_ratio": "9:16",
            "duration": "15-30 seconds",
            "style": "Trendy, fast-paced, music-driven",
            "captions": "Auto-captions enabled",
            "hashtags": "Use trending hashtags",
            "hook_timing": "First 1-2 seconds critical"
        },
        "instagram_reels": {
            "aspect_ratio": "9:16",
            "duration": "15-30 seconds",
            "style": "Polished, aesthetic, story-driven",
            "captions": "Stylized text overlays",
            "music": "Instagram audio library preferred",
            "hook_timing": "First 3 seconds"
        },
        "youtube_shorts": {
            "aspect_ratio": "9:16",
            "duration": "Up to 60 seconds",
            "style": "Educational or entertaining",
            "captions": "Clear, readable text",
            "thumbnails": "Eye-catching first frame",
            "seo": "Keyword-optimized title and description"
        },
        "facebook": {
            "aspect_ratio": "16:9 or 1:1",
            "duration": "15-60 seconds",
            "style": "Community-focused, engaging",
            "captions": "Auto-play friendly with captions",
            "call_to_action": "Clear CTA for engagement",
            "native_upload": "Upload directly to Facebook"
        },
        "linkedin": {
            "aspect_ratio": "16:9 or 1:1",
            "duration": "30-90 seconds",
            "style": "Professional, value-driven",
            "captions": "Professional language",
            "content": "Industry insights or tips",
            "networking": "Encourage professional discussion"
        }
    }
    
    return platforms

def generate_video_editing_checklist(video: Dict[str, Any]) -> List[str]:
    """Generate a checklist for video editing"""
    
    checklist = [
        "✅ Import all raw footage and assets",
        "✅ Create sequence with correct aspect ratio",
        "✅ Add background music at appropriate level",
        "✅ Implement cuts according to pacing instructions",
        "✅ Add text overlays with proper timing",
        "✅ Apply color grading and visual effects",
        "✅ Add sound effects where specified",
        "✅ Ensure smooth transitions between scenes",
        "✅ Add captions for accessibility",
        "✅ Export in platform-specific formats",
        "✅ Create thumbnail variations",
        "✅ Test video on different devices"
    ]
    
    return checklist
