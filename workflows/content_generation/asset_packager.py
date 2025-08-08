from typing import Dict, Any, List
import json
from datetime import datetime

def package_assets(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]],
    content_strategy: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Package all generated content assets into organized, export-ready formats
    
    Args:
        ad_copy: Generated ad copy variants
        social_captions: Social media captions by platform
        images: Generated images and visuals
        ugc_scripts: UGC video scripts
        email_assets: Email creative assets
        content_strategy: Original content strategy
    
    Returns:
        Complete packaged asset collection ready for use
    """
    
    # Create the main package structure
    asset_package = {
        "package_info": create_package_info(content_strategy),
        "content_summary": create_content_summary(ad_copy, social_captions, images, ugc_scripts, email_assets),
        "organized_assets": organize_assets_by_type(ad_copy, social_captions, images, ugc_scripts, email_assets),
        "platform_kits": create_platform_kits(ad_copy, social_captions, images, ugc_scripts),
        "campaign_ready_sets": create_campaign_sets(ad_copy, social_captions, images, email_assets),
        "usage_guidelines": create_usage_guidelines(),
        "export_formats": prepare_export_formats(ad_copy, social_captions, images, ugc_scripts, email_assets),
        "quality_checklist": create_quality_checklist(),
        "performance_tracking": setup_performance_tracking()
    }
    
    return asset_package

def create_package_info(content_strategy: Dict[str, Any]) -> Dict[str, Any]:
    """Create package metadata and information"""
    
    package_info = {
        "created_at": datetime.now().isoformat(),
        "package_id": generate_package_id(),
        "product_service": content_strategy.get("product_description", "Product"),
        "target_audience": content_strategy.get("target_audience", "General audience"),
        "brand_tone": content_strategy.get("brand_tone", "Professional"),
        "content_pillars": content_strategy.get("content_pillars", []),
        "key_messages": content_strategy.get("key_messages", []),
        "brand_colors": content_strategy.get("brand_colors", ""),
        "version": "1.0",
        "status": "ready_for_use"
    }
    
    return package_info

def generate_package_id() -> str:
    """Generate unique package identifier"""
    return f"content_pkg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def create_content_summary(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create summary of all generated content"""
    
    summary = {
        "total_assets": len(ad_copy) + sum(len(captions) for captions in social_captions.values()) + len(images) + len(ugc_scripts) + len(email_assets),
        "ad_copy_variants": len(ad_copy),
        "social_platforms": len(social_captions.keys()),
        "total_social_captions": sum(len(captions) for captions in social_captions.values()),
        "images_generated": len(images),
        "ugc_scripts": len(ugc_scripts),
        "email_assets": len(email_assets),
        "content_types": list(set([
            "ad_copy" if ad_copy else None,
            "social_captions" if social_captions else None,
            "images" if images else None,
            "ugc_scripts" if ugc_scripts else None,
            "email_assets" if email_assets else None
        ]) - {None}),
        "platforms_covered": list(social_captions.keys()) + ["email", "advertising"],
        "ready_for_deployment": True
    }
    
    return summary

def organize_assets_by_type(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Organize all assets by content type"""
    
    organized = {
        "advertising": {
            "ad_copy_variants": ad_copy,
            "ad_images": [img for img in images if img.get("type") in ["ad_creative", "hero_image"]],
            "platform_adaptations": extract_platform_adaptations(ad_copy)
        },
        "social_media": {
            "captions_by_platform": social_captions,
            "social_images": [img for img in images if img.get("type") in ["social_post", "product_showcase"]],
            "ugc_video_scripts": ugc_scripts,
            "hashtag_collections": extract_hashtags_from_captions(social_captions)
        },
        "email_marketing": {
            "email_creative_assets": email_assets,
            "email_images": [img for img in images if "email" in img.get("type", "").lower()],
            "email_copy_elements": extract_email_copy_elements(ad_copy)
        },
        "video_content": {
            "ugc_scripts": ugc_scripts,
            "video_thumbnails": [img for img in images if img.get("type") in ["hero_image", "product_showcase"]],
            "editing_guidelines": extract_video_editing_guidelines(ugc_scripts)
        }
    }
    
    return organized

def extract_platform_adaptations(ad_copy: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract platform adaptations from ad copy"""
    
    adaptations = {}
    
    for copy in ad_copy:
        platform_adaptations = copy.get("platform_adaptations", {})
        for platform, adaptation in platform_adaptations.items():
            if platform not in adaptations:
                adaptations[platform] = []
            adaptations[platform].append(adaptation)
    
    return adaptations

def extract_hashtags_from_captions(social_captions: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Extract hashtag collections from social captions"""
    
    hashtags = {}
    
    for platform, captions in social_captions.items():
        platform_hashtags = set()
        
        for caption in captions:
            # Extract hashtags from caption
            words = caption.split()
            for word in words:
                if word.startswith('#'):
                    platform_hashtags.add(word)
        
        hashtags[platform] = list(platform_hashtags)
    
    return hashtags

def extract_email_copy_elements(ad_copy: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Extract email-friendly copy elements from ad copy"""
    
    elements = {
        "subject_line_ideas": [],
        "headline_options": [],
        "body_text_snippets": [],
        "cta_buttons": []
    }
    
    for copy in ad_copy:
        elements["subject_line_ideas"].append(copy.get("headline", ""))
        elements["headline_options"].append(copy.get("headline", ""))
        elements["body_text_snippets"].append(copy.get("primary_text", ""))
        elements["cta_buttons"].append(copy.get("cta", ""))
    
    return elements

def extract_video_editing_guidelines(ugc_scripts: List[Dict[str, Any]]) -> List[str]:
    """Extract video editing guidelines from UGC scripts"""
    
    guidelines = []
    
    for script in ugc_scripts:
        editing_notes = script.get("editing_notes", [])
        guidelines.extend(editing_notes)
    
    # Remove duplicates and add standard guidelines
    unique_guidelines = list(set(guidelines))
    
    standard_guidelines = [
        "Maintain authentic, unpolished feel",
        "Keep cuts snappy and engaging",
        "Add captions for accessibility",
        "Use trending audio where appropriate",
        "Optimize for vertical viewing"
    ]
    
    unique_guidelines.extend(standard_guidelines)
    
    return unique_guidelines

def create_platform_kits(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create ready-to-use platform kits"""
    
    platform_kits = {}
    
    # Instagram kit
    platform_kits["instagram"] = {
        "feed_posts": {
            "captions": social_captions.get("instagram", []),
            "images": [img for img in images if img.get("dimensions") == "1080x1080"],
            "hashtags": extract_hashtags_for_platform("instagram", social_captions)
        },
        "stories": {
            "templates": "Coming soon - story templates",
            "dimensions": "1080x1920"
        },
        "reels": {
            "scripts": [script for script in ugc_scripts if "instagram" in script.get("platform_versions", {})],
            "music_suggestions": extract_music_suggestions(ugc_scripts)
        }
    }
    
    # TikTok kit
    platform_kits["tiktok"] = {
        "video_content": {
            "scripts": [script for script in ugc_scripts if "tiktok" in script.get("platform_versions", {})],
            "captions": social_captions.get("tiktok", []),
            "trending_elements": "Use trending audio and effects"
        },
        "posting_strategy": {
            "best_times": "6-10 AM, 7-9 PM",
            "frequency": "1-2 posts per day",
            "engagement_tips": "Respond to comments quickly, use trending hashtags"
        }
    }
    
    # Facebook kit
    platform_kits["facebook"] = {
        "posts": {
            "copy": extract_facebook_copy(ad_copy),
            "images": [img for img in images if img.get("dimensions") in ["1200x628", "1080x1080"]],
            "video_content": social_captions.get("facebook", [])
        },
        "ads": {
            "ad_copy": [copy.get("platform_adaptations", {}).get("facebook", {}) for copy in ad_copy],
            "creative_specs": "1200x628 for feed, 1080x1080 for stories"
        }
    }
    
    # LinkedIn kit
    platform_kits["linkedin"] = {
        "posts": {
            "captions": social_captions.get("linkedin", []),
            "professional_tone": "Maintained throughout all content",
            "content_focus": "Industry insights, thought leadership"
        },
        "articles": {
            "topics": extract_article_topics(ad_copy),
            "format": "Long-form, value-driven content"
        }
    }
    
    return platform_kits

def extract_hashtags_for_platform(platform: str, social_captions: Dict[str, List[str]]) -> List[str]:
    """Extract hashtags for specific platform"""
    
    hashtags = []
    captions = social_captions.get(platform, [])
    
    for caption in captions:
        words = caption.split()
        for word in words:
            if word.startswith('#'):
                hashtags.append(word)
    
    return list(set(hashtags))

def extract_music_suggestions(ugc_scripts: List[Dict[str, Any]]) -> List[str]:
    """Extract music suggestions from UGC scripts"""
    
    music_suggestions = []
    
    for script in ugc_scripts:
        audio_suggestions = script.get("audio_suggestions", {})
        music_style = audio_suggestions.get("music_style", "")
        if music_style:
            music_suggestions.append(music_style)
    
    return list(set(music_suggestions))

def extract_facebook_copy(ad_copy: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Extract Facebook-optimized copy"""
    
    facebook_copy = []
    
    for copy in ad_copy:
        facebook_adaptation = copy.get("platform_adaptations", {}).get("facebook", {})
        if facebook_adaptation:
            facebook_copy.append(facebook_adaptation)
    
    return facebook_copy

def extract_article_topics(ad_copy: List[Dict[str, Any]]) -> List[str]:
    """Extract potential article topics for LinkedIn"""
    
    topics = []
    
    for copy in ad_copy:
        headline = copy.get("headline", "")
        primary_text = copy.get("primary_text", "")
        
        # Create article topic from copy elements
        if headline and primary_text:
            topic = f"How {headline.lower()} can transform your business approach"
            topics.append(topic)
    
    return topics

def create_campaign_sets(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create campaign-ready asset sets"""
    
    campaign_sets = {
        "launch_campaign": {
            "description": "Initial product/service launch campaign",
            "assets": {
                "hero_ad": get_primary_ad_copy(ad_copy),
                "hero_image": get_hero_image(images),
                "social_announcement": get_launch_social_content(social_captions),
                "email_header": get_email_header(email_assets)
            },
            "timeline": "Week 1: Launch announcement across all platforms"
        },
        "engagement_campaign": {
            "description": "Ongoing engagement and awareness campaign", 
            "assets": {
                "social_series": social_captions,
                "visual_content": [img for img in images if img.get("type") == "social_post"],
                "user_content": "UGC scripts for customer engagement"
            },
            "timeline": "Weeks 2-4: Sustained engagement content"
        },
        "conversion_campaign": {
            "description": "Direct response and conversion campaign",
            "assets": {
                "conversion_ads": [copy for copy in ad_copy if "cta" in copy],
                "product_images": [img for img in images if img.get("type") == "product_showcase"],
                "email_sequence": email_assets
            },
            "timeline": "Ongoing: Performance marketing focus"
        }
    }
    
    return campaign_sets

def get_primary_ad_copy(ad_copy: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get the primary ad copy for campaigns"""
    
    if ad_copy:
        # Return the first variant or the one with highest engagement potential
        return ad_copy[0]
    
    return {}

def get_hero_image(images: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get the hero image for campaigns"""
    
    # Look for hero image type first
    for image in images:
        if image.get("type") == "hero_image":
            return image
    
    # Fallback to first available image
    if images:
        return images[0]
    
    return {}

def get_launch_social_content(social_captions: Dict[str, List[str]]) -> Dict[str, str]:
    """Get launch-specific social content"""
    
    launch_content = {}
    
    for platform, captions in social_captions.items():
        if captions:
            # Use first caption as launch content
            launch_content[platform] = captions[0]
    
    return launch_content

def get_email_header(email_assets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get email header asset"""
    
    for asset in email_assets:
        if asset.get("type") == "email_header":
            return asset
    
    return {}

def create_usage_guidelines() -> Dict[str, Any]:
    """Create guidelines for using the generated assets"""
    
    guidelines = {
        "general_guidelines": [
            "Maintain brand consistency across all platforms",
            "Adapt content tone for each platform's audience",
            "Test different variants to optimize performance",
            "Track engagement metrics for continuous improvement",
            "Ensure legal compliance for all markets"
        ],
        "platform_specific": {
            "social_media": [
                "Post during optimal engagement hours",
                "Engage with comments and messages promptly",
                "Use platform-native features (stories, reels, etc.)",
                "Monitor trending topics and hashtags",
                "Maintain consistent posting schedule"
            ],
            "advertising": [
                "A/B test ad copy and creative variants",
                "Monitor ad performance metrics closely",
                "Adjust targeting based on engagement data",
                "Comply with platform advertising policies",
                "Set appropriate budget and bidding strategies"
            ],
            "email_marketing": [
                "Segment audiences for personalization",
                "Test subject lines and send times",
                "Ensure mobile optimization",
                "Include clear unsubscribe options",
                "Monitor deliverability rates"
            ]
        },
        "content_refresh": {
            "frequency": "Review and refresh content monthly",
            "performance_threshold": "Refresh assets with declining engagement",
            "seasonal_updates": "Adapt content for seasonal campaigns",
            "trend_monitoring": "Incorporate current trends and topics"
        }
    }
    
    return guidelines

def prepare_export_formats(
    ad_copy: List[Dict[str, Any]],
    social_captions: Dict[str, List[str]],
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Prepare assets in various export formats"""
    
    export_formats = {
        "json": {
            "full_package": "Complete asset package in JSON format",
            "individual_assets": "Each asset type as separate JSON file",
            "platform_specific": "Platform-optimized JSON exports"
        },
        "csv": {
            "ad_copy_spreadsheet": prepare_ad_copy_csv(ad_copy),
            "social_content_calendar": prepare_social_csv(social_captions),
            "asset_inventory": prepare_asset_inventory_csv(images, ugc_scripts, email_assets)
        },
        "zip_packages": {
            "complete_package": "All assets in organized folder structure",
            "platform_kits": "Individual platform packages",
            "campaign_sets": "Campaign-specific asset bundles"
        },
        "integration_ready": {
            "cms_import": "Format for content management systems",
            "social_schedulers": "Format for social media scheduling tools",
            "email_platforms": "Format for email marketing platforms"
        }
    }
    
    return export_formats

def prepare_ad_copy_csv(ad_copy: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Prepare ad copy data for CSV export"""
    
    csv_data = []
    
    for i, copy in enumerate(ad_copy):
        csv_data.append({
            "variant": f"Variant {i+1}",
            "headline": copy.get("headline", ""),
            "primary_text": copy.get("primary_text", ""),
            "cta": copy.get("cta", ""),
            "description": copy.get("description", ""),
            "facebook_headline": copy.get("platform_adaptations", {}).get("facebook", {}).get("headline", ""),
            "google_headline": copy.get("platform_adaptations", {}).get("google_ads", {}).get("headline_1", ""),
            "character_count": copy.get("character_counts", {}).get("facebook_primary", 0)
        })
    
    return csv_data

def prepare_social_csv(social_captions: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """Prepare social media content for CSV export"""
    
    csv_data = []
    
    for platform, captions in social_captions.items():
        for i, caption in enumerate(captions):
            csv_data.append({
                "platform": platform,
                "caption_number": i + 1,
                "caption_text": caption,
                "character_count": len(caption),
                "hashtags": extract_hashtags_from_text(caption),
                "optimal_posting_time": get_optimal_time(platform)
            })
    
    return csv_data

def prepare_asset_inventory_csv(
    images: List[Dict[str, Any]],
    ugc_scripts: List[Dict[str, Any]],
    email_assets: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """Prepare asset inventory for CSV export"""
    
    csv_data = []
    
    # Add images
    for image in images:
        csv_data.append({
            "asset_type": "Image",
            "asset_name": image.get("file_name", ""),
            "description": image.get("description", ""),
            "dimensions": image.get("dimensions", ""),
            "usage": image.get("usage", ""),
            "status": "ready" if image.get("url") else "pending"
        })
    
    # Add UGC scripts
    for script in ugc_scripts:
        csv_data.append({
            "asset_type": "UGC Script",
            "asset_name": script.get("title", ""),
            "description": script.get("purpose", ""),
            "duration": script.get("duration", ""),
            "usage": f"{script.get('type', '')} video content",
            "status": "ready"
        })
    
    # Add email assets
    for asset in email_assets:
        csv_data.append({
            "asset_type": "Email Asset",
            "asset_name": asset.get("file_name", ""),
            "description": asset.get("description", ""),
            "dimensions": asset.get("dimensions", ""),
            "usage": asset.get("usage", ""),
            "status": "ready" if asset.get("url") else "pending"
        })
    
    return csv_data

def extract_hashtags_from_text(text: str) -> str:
    """Extract hashtags from text and return as comma-separated string"""
    
    hashtags = []
    words = text.split()
    
    for word in words:
        if word.startswith('#'):
            hashtags.append(word)
    
    return ", ".join(hashtags)

def get_optimal_time(platform: str) -> str:
    """Get optimal posting time for platform"""
    
    optimal_times = {
        "instagram": "11:00 AM - 2:00 PM",
        "facebook": "9:00 AM - 10:00 AM",
        "twitter": "9:00 AM - 10:00 AM",
        "linkedin": "10:00 AM - 11:00 AM",
        "tiktok": "6:00 AM - 10:00 AM"
    }
    
    return optimal_times.get(platform, "10:00 AM - 2:00 PM")

def create_quality_checklist() -> List[Dict[str, str]]:
    """Create quality checklist for generated assets"""
    
    checklist = [
        {
            "category": "Content Quality",
            "items": [
                "All copy is grammatically correct and error-free",
                "Brand tone is consistent across all assets",
                "Key messages are clearly communicated",
                "Call-to-actions are compelling and clear",
                "Content aligns with target audience preferences"
            ]
        },
        {
            "category": "Technical Specifications",
            "items": [
                "Images meet platform dimension requirements",
                "Character counts are within platform limits",
                "Video scripts include proper timing cues",
                "All assets are properly formatted for export",
                "File naming conventions are consistent"
            ]
        },
        {
            "category": "Brand Compliance",
            "items": [
                "Brand colors are accurately represented",
                "Visual style aligns with brand guidelines",
                "Logo usage follows brand standards",
                "Messaging adheres to brand voice",
                "Legal compliance requirements are met"
            ]
        },
        {
            "category": "Platform Optimization",
            "items": [
                "Content is optimized for each platform",
                "Hashtags are relevant and trending",
                "Image formats are platform-appropriate",
                "Video content follows platform best practices",
                "Engagement features are properly utilized"
            ]
        }
    ]
    
    return checklist

def setup_performance_tracking() -> Dict[str, Any]:
    """Setup performance tracking framework"""
    
    tracking = {
        "kpi_metrics": {
            "engagement": ["likes", "comments", "shares", "saves"],
            "reach": ["impressions", "reach", "frequency"],
            "conversion": ["clicks", "conversions", "cost_per_conversion"],
            "brand": ["brand_awareness", "sentiment", "recall"]
        },
        "tracking_setup": {
            "utm_parameters": "Add tracking codes to all links",
            "pixel_implementation": "Ensure tracking pixels are installed",
            "analytics_integration": "Connect to Google Analytics and platform analytics",
            "reporting_schedule": "Weekly performance reviews"
        },
        "optimization_triggers": {
            "low_engagement": "Refresh content if engagement drops below 2%",
            "high_cost": "Optimize if cost per click exceeds target by 50%",
            "poor_conversion": "Review and test new variants if conversion rate drops",
            "audience_fatigue": "Rotate creative assets every 2 weeks"
        },
        "success_benchmarks": {
            "social_engagement": "Aim for 3-5% engagement rate",
            "email_open_rate": "Target 25-30% open rate",
            "click_through_rate": "Target 2-3% CTR for ads",
            "conversion_rate": "Target 2-5% conversion rate"
        }
    }
    
    return tracking
