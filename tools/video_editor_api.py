import requests
import json
import time
from typing import Dict, Any, List, Optional

def create_video_content(
    script: str,
    video_type: str = "ugc",
    duration: str = "30 seconds",
    platform: str = "instagram"
) -> Dict[str, Any]:
    """
    Create video content instructions and metadata
    
    Args:
        script: Video script content
        video_type: Type of video (ugc, product_demo, testimonial)
        duration: Target duration
        platform: Target platform (instagram, tiktok, youtube, etc.)
    
    Returns:
        Video content structure with editing instructions
    """
    
    video_content = {
        "script": script,
        "video_type": video_type,
        "duration": duration,
        "platform": platform,
        "editing_instructions": generate_editing_instructions(script, video_type, platform),
        "audio_requirements": get_audio_requirements(video_type, platform),
        "visual_requirements": get_visual_requirements(video_type, platform),
        "export_settings": get_export_settings(platform),
        "optimization_tips": get_optimization_tips(platform),
        "created_at": str(int(time.time()))
    }
    
    return video_content

def generate_editing_instructions(script: str, video_type: str, platform: str) -> Dict[str, Any]:
    """Generate detailed editing instructions for video content"""
    
    instructions = {
        "pacing": get_pacing_guidelines(video_type, platform),
        "cuts": get_cutting_guidelines(script, video_type),
        "transitions": get_transition_guidelines(video_type, platform),
        "text_overlays": extract_text_overlays(script),
        "effects": get_effects_guidelines(video_type, platform),
        "color_grading": get_color_grading_guidelines(video_type),
        "audio_sync": get_audio_sync_guidelines(script)
    }
    
    return instructions

def get_pacing_guidelines(video_type: str, platform: str) -> Dict[str, Any]:
    """Get pacing guidelines based on video type and platform"""
    
    platform_pacing = {
        "tiktok": {
            "cut_frequency": "Every 1-2 seconds",
            "hook_duration": "First 1-2 seconds",
            "content_pace": "Fast, high energy",
            "attention_span": "3-15 seconds peak engagement"
        },
        "instagram": {
            "cut_frequency": "Every 2-3 seconds", 
            "hook_duration": "First 3 seconds",
            "content_pace": "Medium to fast",
            "attention_span": "15-30 seconds optimal"
        },
        "youtube": {
            "cut_frequency": "Every 3-5 seconds",
            "hook_duration": "First 5-10 seconds", 
            "content_pace": "Moderate, story-driven",
            "attention_span": "30-60 seconds acceptable"
        },
        "facebook": {
            "cut_frequency": "Every 4-6 seconds",
            "hook_duration": "First 3-5 seconds",
            "content_pace": "Moderate",
            "attention_span": "15-45 seconds"
        }
    }
    
    video_type_modifiers = {
        "ugc": {"style": "Authentic, unpolished feel"},
        "product_demo": {"style": "Clear, instructional pacing"},
        "testimonial": {"style": "Natural, conversational rhythm"},
        "unboxing": {"style": "Building anticipation, reveal moments"},
        "before_after": {"style": "Dramatic reveal pacing"}
    }
    
    base_pacing = platform_pacing.get(platform, platform_pacing["instagram"])
    type_modifier = video_type_modifiers.get(video_type, {"style": "Professional"})
    
    return {**base_pacing, **type_modifier}

def get_cutting_guidelines(script: str, video_type: str) -> List[str]:
    """Get cutting guidelines based on script content and video type"""
    
    guidelines = [
        "Cut on action to maintain flow",
        "Remove dead space and filler words",
        "Keep cuts tight for social media attention spans",
        "Use jump cuts to compress time naturally",
        "Match cuts to audio beats when possible"
    ]
    
    # Add type-specific guidelines
    if video_type == "ugc":
        guidelines.extend([
            "Maintain authentic feel - don't over-edit",
            "Keep some natural pauses and reactions",
            "Include genuine mistakes or adjustments"
        ])
    elif video_type == "product_demo":
        guidelines.extend([
            "Cut to highlight key features clearly",
            "Show setup and results distinctly",
            "Use close-ups for important details"
        ])
    elif video_type == "testimonial":
        guidelines.extend([
            "Cut to emphasize emotional moments",
            "Keep natural speech patterns",
            "Show credibility through natural delivery"
        ])
    
    return guidelines

def get_transition_guidelines(video_type: str, platform: str) -> List[str]:
    """Get transition guidelines for video editing"""
    
    platform_transitions = {
        "tiktok": ["Quick cuts", "Zoom transitions", "Speed ramps", "Beat drops"],
        "instagram": ["Smooth fades", "Slide transitions", "Zoom effects", "Cross dissolves"],
        "youtube": ["Simple cuts", "Fade transitions", "Dissolves", "Match cuts"],
        "facebook": ["Gentle transitions", "Fades", "Simple cuts", "Cross dissolves"]
    }
    
    base_transitions = platform_transitions.get(platform, ["Simple cuts", "Fade transitions"])
    
    # Add video type specific transitions
    if video_type == "before_after":
        base_transitions.extend(["Split screen reveals", "Dramatic wipes"])
    elif video_type == "unboxing":
        base_transitions.extend(["Anticipation builds", "Reveal cuts"])
    
    return base_transitions

def extract_text_overlays(script: str) -> List[Dict[str, str]]:
    """Extract text overlay opportunities from script"""
    
    overlays = []
    
    # Look for key phrases that should be highlighted
    key_phrases = [
        "amazing", "incredible", "wow", "perfect", "love it",
        "game changer", "must have", "obsessed", "holy grail",
        "before", "after", "results", "transformation"
    ]
    
    script_lower = script.lower()
    
    for phrase in key_phrases:
        if phrase in script_lower:
            overlays.append({
                "text": phrase.upper(),
                "style": "bold, animated",
                "timing": "when mentioned in audio",
                "position": "center or bottom third"
            })
    
    # Add default overlays
    default_overlays = [
        {
            "text": "MUST WATCH ⚡",
            "style": "attention-grabbing",
            "timing": "opening 2 seconds",
            "position": "top center"
        },
        {
            "text": "FOLLOW FOR MORE",
            "style": "call-to-action",
            "timing": "final 3 seconds", 
            "position": "bottom center"
        }
    ]
    
    overlays.extend(default_overlays)
    
    return overlays

def get_audio_requirements(video_type: str, platform: str) -> Dict[str, Any]:
    """Get audio requirements for video content"""
    
    requirements = {
        "voice_over": True,
        "background_music": True,
        "sound_effects": False,
        "auto_captions": True,
        "audio_quality": "High quality, clear speech"
    }
    
    # Platform-specific audio requirements
    platform_audio = {
        "tiktok": {
            "trending_audio": "Highly recommended",
            "original_audio": "Can work but trending is better",
            "music_volume": "Prominent but not overwhelming",
            "voiceover_style": "Energetic, casual"
        },
        "instagram": {
            "trending_audio": "Recommended",
            "original_audio": "Acceptable for brand content",
            "music_volume": "Balanced with voiceover",
            "voiceover_style": "Polished but authentic"
        },
        "youtube": {
            "trending_audio": "Optional",
            "original_audio": "Preferred for educational content",
            "music_volume": "Background level",
            "voiceover_style": "Clear, educational"
        }
    }
    
    # Video type specific audio
    type_audio = {
        "ugc": {
            "authenticity": "Keep natural audio imperfections",
            "music_style": "Trendy, upbeat",
            "effects": "Minimal, natural sounds"
        },
        "product_demo": {
            "clarity": "Clear narration essential",
            "music_style": "Professional, non-distracting",
            "effects": "Product interaction sounds"
        },
        "testimonial": {
            "naturalness": "Conversational, genuine",
            "music_style": "Warm, trustworthy background",
            "effects": "None, focus on speech"
        }
    }
    
    platform_specific = platform_audio.get(platform, {})
    type_specific = type_audio.get(video_type, {})
    
    return {**requirements, **platform_specific, **type_specific}

def get_visual_requirements(video_type: str, platform: str) -> Dict[str, Any]:
    """Get visual requirements for video content"""
    
    base_requirements = {
        "aspect_ratio": get_aspect_ratio(platform),
        "resolution": get_resolution(platform),
        "frame_rate": "30fps standard, 60fps for smooth motion",
        "lighting": "Good lighting essential for engagement"
    }
    
    # Platform visual requirements
    platform_visuals = {
        "tiktok": {
            "style": "Vertical, mobile-first",
            "captions": "Auto-captions essential",
            "effects": "Use trending effects",
            "branding": "Subtle, organic integration"
        },
        "instagram": {
            "style": "Polished, aesthetic",
            "captions": "Stylized text overlays",
            "effects": "Professional but not overdone",
            "branding": "Clean brand integration"
        },
        "youtube": {
            "style": "Professional, educational",
            "captions": "Clear, readable",
            "effects": "Minimal, purpose-driven",
            "branding": "Prominent brand presence"
        }
    }
    
    # Video type visual requirements
    type_visuals = {
        "ugc": {
            "authenticity": "Unpolished, real environment",
            "camera_work": "Handheld, natural movement",
            "composition": "Casual framing"
        },
        "product_demo": {
            "clarity": "Clear product visibility",
            "camera_work": "Steady, focused shots",
            "composition": "Product-centered framing"
        },
        "testimonial": {
            "trust": "Good lighting, clear face",
            "camera_work": "Stable, eye-level shots",
            "composition": "Personal, direct-to-camera"
        }
    }
    
    platform_specific = platform_visuals.get(platform, {})
    type_specific = type_visuals.get(video_type, {})
    
    return {**base_requirements, **platform_specific, **type_specific}

def get_aspect_ratio(platform: str) -> str:
    """Get optimal aspect ratio for platform"""
    
    ratios = {
        "tiktok": "9:16 (vertical)",
        "instagram_reels": "9:16 (vertical)",
        "instagram_feed": "1:1 (square) or 4:5 (vertical)",
        "youtube_shorts": "9:16 (vertical)",
        "youtube_regular": "16:9 (horizontal)",
        "facebook": "1:1 (square) or 16:9 (horizontal)",
        "linkedin": "1:1 (square) or 16:9 (horizontal)"
    }
    
    return ratios.get(platform, "9:16 (vertical)")

def get_resolution(platform: str) -> str:
    """Get optimal resolution for platform"""
    
    resolutions = {
        "tiktok": "1080x1920",
        "instagram": "1080x1920 (reels), 1080x1080 (feed)",
        "youtube": "1080x1920 (shorts), 1920x1080 (regular)",
        "facebook": "1080x1080 or 1920x1080"
    }
    
    return resolutions.get(platform, "1080x1920")

def get_export_settings(platform: str) -> Dict[str, Any]:
    """Get export settings for different platforms"""
    
    settings = {
        "format": "MP4",
        "codec": "H.264",
        "bitrate": "High quality",
        "file_size": "Under platform limits"
    }
    
    platform_settings = {
        "tiktok": {
            "max_duration": "10 minutes",
            "recommended_duration": "15-30 seconds",
            "max_file_size": "287MB",
            "recommended_bitrate": "1-2 Mbps"
        },
        "instagram": {
            "max_duration": "90 seconds (reels), 60 seconds (stories)",
            "recommended_duration": "15-30 seconds",
            "max_file_size": "4GB",
            "recommended_bitrate": "3.5 Mbps"
        },
        "youtube": {
            "max_duration": "60 seconds (shorts), unlimited (regular)",
            "recommended_duration": "30-60 seconds (shorts)",
            "max_file_size": "256GB",
            "recommended_bitrate": "8 Mbps (1080p)"
        }
    }
    
    platform_specific = platform_settings.get(platform, {})
    
    return {**settings, **platform_specific}

def get_optimization_tips(platform: str) -> List[str]:
    """Get optimization tips for platform success"""
    
    general_tips = [
        "Hook viewers in the first 3 seconds",
        "Include captions for accessibility",
        "Optimize for mobile viewing",
        "Test different thumbnail options",
        "Use trending audio when appropriate"
    ]
    
    platform_tips = {
        "tiktok": [
            "Use trending hashtags and sounds",
            "Post during peak hours (6-10am, 7-9pm)",
            "Engage with comments quickly",
            "Create series or follow-up content",
            "Use TikTok's native editing tools"
        ],
        "instagram": [
            "Cross-post to feed and stories",
            "Use Instagram's creator tools",
            "Post consistently at optimal times",
            "Engage with your community",
            "Use relevant hashtags (5-10 max)"
        ],
        "youtube": [
            "Optimize title and description for SEO",
            "Create eye-catching thumbnails",
            "Use end screens and cards",
            "Encourage subscriptions and notifications",
            "Analyze performance in YouTube Analytics"
        ]
    }
    
    platform_specific = platform_tips.get(platform, [])
    
    return general_tips + platform_specific

def get_effects_guidelines(video_type: str, platform: str) -> List[str]:
    """Get effects guidelines for video editing"""
    
    effects = []
    
    # Platform-based effects
    if platform == "tiktok":
        effects.extend([
            "Use trending effects and filters",
            "Speed ramps for dramatic effect",
            "Quick zoom transitions",
            "Beat-synced effects"
        ])
    elif platform == "instagram":
        effects.extend([
            "Subtle color grading",
            "Smooth transitions",
            "Professional overlays",
            "Brand-consistent filters"
        ])
    
    # Video type based effects
    if video_type == "ugc":
        effects.extend([
            "Minimal effects to maintain authenticity",
            "Natural color correction only",
            "Simple text overlays"
        ])
    elif video_type == "product_demo":
        effects.extend([
            "Highlight effects for key features",
            "Clean, professional effects",
            "Call-out graphics and arrows"
        ])
    
    return effects

def get_color_grading_guidelines(video_type: str) -> Dict[str, str]:
    """Get color grading guidelines based on video type"""
    
    guidelines = {
        "ugc": "Minimal grading, natural colors, authentic feel",
        "product_demo": "Clean, bright, professional look",
        "testimonial": "Warm, trustworthy, natural skin tones",
        "unboxing": "Vibrant, exciting, enhanced colors",
        "before_after": "Dramatic contrast to show transformation"
    }
    
    return {
        "style": guidelines.get(video_type, "Natural, professional"),
        "contrast": "Moderate enhancement",
        "saturation": "Slightly enhanced for engagement",
        "brightness": "Optimized for mobile viewing"
    }

def get_audio_sync_guidelines(script: str) -> List[str]:
    """Get audio synchronization guidelines"""
    
    return [
        "Sync cuts to natural speech pauses",
        "Match visual actions to audio mentions",
        "Use audio peaks to time transitions",
        "Ensure lip-sync accuracy for talking heads",
        "Balance background music with speech",
        "Add audio cues for visual effects",
        "Time text overlays with audio mentions"
    ]

def edit_video_clips(
    clips_info: List[Dict[str, Any]],
    editing_style: str = "social_media"
) -> Dict[str, Any]:
    """
    Process video clips with editing instructions
    
    Args:
        clips_info: List of clip information and requirements
        editing_style: Style of editing (social_media, professional, ugc)
    
    Returns:
        Editing instructions and timeline
    """
    
    editing_timeline = {
        "total_clips": len(clips_info),
        "editing_style": editing_style,
        "timeline": [],
        "effects_needed": [],
        "audio_tracks": [],
        "export_specs": {}
    }
    
    current_time = 0
    
    for i, clip in enumerate(clips_info):
        clip_duration = clip.get("duration", 3)  # Default 3 seconds
        
        timeline_entry = {
            "clip_number": i + 1,
            "start_time": current_time,
            "end_time": current_time + clip_duration,
            "source_file": clip.get("source", f"clip_{i+1}"),
            "effects": clip.get("effects", []),
            "transitions": clip.get("transitions", ["cut"]),
            "audio_level": clip.get("audio_level", 100)
        }
        
        editing_timeline["timeline"].append(timeline_entry)
        current_time += clip_duration
    
    editing_timeline["total_duration"] = current_time
    
    return editing_timeline

def create_editing_checklist(platform: str, video_type: str) -> List[str]:
    """Create a comprehensive editing checklist"""
    
    checklist = [
        "✅ Import all source footage and audio",
        "✅ Create sequence with correct aspect ratio",
        "✅ Add background music at appropriate level",
        "✅ Sync audio and video properly",
        "✅ Add text overlays with proper timing",
        "✅ Apply color correction and grading",
        "✅ Add transitions between clips",
        "✅ Include captions for accessibility",
        "✅ Add effects as specified",
        "✅ Check audio levels throughout",
        "✅ Preview on mobile device",
        "✅ Export in correct format and resolution",
        "✅ Create thumbnail options",
        "✅ Test upload to platform"
    ]
    
    # Add platform-specific items
    if platform == "tiktok":
        checklist.extend([
            "✅ Use trending audio if applicable",
            "✅ Add trending effects",
            "✅ Optimize for vertical viewing"
        ])
    elif platform == "youtube":
        checklist.extend([
            "✅ Create compelling thumbnail",
            "✅ Add end screen elements",
            "✅ Include SEO-optimized title"
        ])
    
    return checklist
