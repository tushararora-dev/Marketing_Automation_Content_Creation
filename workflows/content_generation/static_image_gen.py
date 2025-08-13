from typing import Dict, Any, List
from tools.image_gen import generate_image, generate_multiple_images
from tools.llm_manager import get_llm_response

def generate_static_images(
    content_strategy: Dict[str, Any],
    brand_colors: str = "",
    include_product_visuals: bool = False
) -> List[Dict[str, Any]]:
    """
    Generate static images for marketing campaigns
    
    Args:
        content_strategy: Content strategy and requirements
        brand_colors: Brand color scheme
        include_product_visuals: Whether to include product-specific visuals
    
    Returns:
        List of generated images with metadata
    """
    
    images = []
    
    # Generate different types of static images
    image_types = [
        {"type": "hero_image", "description": "Main campaign hero image"},
        {"type": "social_post", "description": "Social media post image"},
        {"type": "ad_creative", "description": "Advertising creative"}
    ]
    
    if include_product_visuals:
        image_types.append({"type": "product_showcase", "description": "Product showcase image"})
    
    for image_type in image_types:
        try:
            image = generate_single_static_image(
                content_strategy=content_strategy,
                image_type=image_type["type"],  
                brand_colors=brand_colors,
                description=image_type["description"]
            )
            images.append(image)
        except Exception as e:
            # Create error placeholder
            images.append({
                "type": image_type["type"],
                "description": image_type["description"],
                "error": str(e),
                "status": "failed"
            })
    
    return images

def generate_single_static_image(
    content_strategy: Dict[str, Any],
    image_type: str,
    brand_colors: str,
    description: str
) -> Dict[str, Any]:
    """Generate a single static image"""
    
    # Create image generation prompt
    image_prompt = create_image_prompt(
        content_strategy=content_strategy,
        image_type=image_type,
        brand_colors=brand_colors,
        description=description
    )
    
    # Generate image using the image generation tool
    image_result = generate_image(
        prompt=image_prompt,
        style=get_image_style(image_type),
        dimensions=get_image_dimensions(image_type)
    )
    
    # Structure the image data
    image = {
        "type": image_type,
        "description": description,
        "prompt": image_prompt,
        "image_obj": image_result.get("image_obj"),  # get image object, not URL
        # "url": image_result.get("url", ""),
        "dimensions": get_image_dimensions(image_type),
        "style": get_image_style(image_type),
        "brand_colors": brand_colors,
        "usage_rights": "Generated for campaign use",
        "alt_text": generate_alt_text(image_type, content_strategy),
        "file_name": f"{image_type}_{generate_timestamp()}.png",
        "variations": generate_image_variations(image_type, image_prompt),
        "optimization": get_optimization_settings(image_type)
    }
    return image

def create_image_prompt(
    content_strategy: Dict[str, Any],
    image_type: str,
    brand_colors: str,
    description: str
) -> str:
    """Create a detailed prompt for image generation"""
    
    product_description = content_strategy.get("product_description", "product")
    target_audience = content_strategy.get("target_audience", "general audience")
    brand_tone = content_strategy.get("brand_tone", "professional")
    content_pillars = content_strategy.get("content_pillars", [])
    
    # base_prompt = f"""
    # Create a high-quality {image_type} image for marketing campaign.
    
    # Product/Service: {product_description}
    # Target Audience: {target_audience}
    # Brand Tone: {brand_tone}
    # Content Focus: {', '.join(content_pillars[:3])}
    # """

    # base_prompt = f"""
    # Create a high-quality {image_type} image.
    
    # Product/Service: {product_description}
    # """

    base_prompt = f"""
    High-quality {image_type}, showcasing: {product_description}, modern professional style, vibrant colors, clear composition, email/social/ad optimized, PNG, no background, visually engaging.
    """

    
    # if brand_colors:
    #     base_prompt += f"\nBrand Colors: {brand_colors}"
    
    # # Add type-specific requirements
    # type_requirements = get_type_specific_requirements(image_type, product_description)
    # base_prompt += f"\n\n{type_requirements}"
    
    # # Add style and quality requirements
    # base_prompt += """
    
    # Style Requirements:
    # - High resolution, professional quality
    # - Clean, modern design
    # - Strong visual hierarchy
    # - Platform-optimized composition
    # - Engaging and eye-catching
    # - Brand-consistent aesthetics
    # """
    
    return base_prompt

def get_type_specific_requirements(image_type: str, product_description: str) -> str:
    """Get specific requirements for different image types"""
    
    requirements = {
        "hero_image": f"""
        Create a compelling hero image featuring {product_description}.
        Include:
        - Central product/service focus
        - Lifestyle context showing usage
        - Space for text overlay
        - Professional lighting and composition
        - Aspirational mood and feeling
        """,
        
        "social_post": f"""
        Create an engaging social media post image for {product_description}.
        Include:
        - Square or vertical format suitable for social platforms
        - Bold, attention-grabbing visuals
        - Clear product/service representation
        - Social-friendly composition with space for captions
        - Trendy, shareable aesthetic
        """,
        
        "ad_creative": f"""
        Create a persuasive advertising creative for {product_description}.
        Include:
        - Clear value proposition visualization
        - Problem/solution representation
        - Trust-building elements
        - Call-to-action friendly layout
        - Conversion-optimized design
        """,
        
        "product_showcase": f"""
        Create a product showcase image for {product_description}.
        Include:
        - Clean, white or branded background
        - Multiple product angles or features
        - Professional product photography style
        - Detail highlighting
        - E-commerce ready composition
        """
    }
    
    return requirements.get(image_type, f"Create a professional image showcasing {product_description}")

def get_image_style(image_type: str) -> str:
    """Get style guidance for different image types"""
    
    styles = {
        "hero_image": "cinematic, professional photography, lifestyle",
        "social_post": "trendy, colorful, social media optimized",
        "ad_creative": "persuasive, clean, conversion-focused",
        "product_showcase": "clean, minimalist, product photography"
    }
    
    return styles.get(image_type, "professional, modern, clean")

def get_image_dimensions(image_type: str) -> str:
    """Get optimal dimensions for different image types"""
    
    dimensions = {
        "hero_image": "1920x1080",
        "social_post": "1080x1080",
        "ad_creative": "1200x628",
        "product_showcase": "1000x1000"
    }
    return dimensions.get(image_type, "1080x1080")

def generate_alt_text(image_type: str, content_strategy: Dict[str, Any]) -> str:
    """Generate descriptive alt text for accessibility"""
    
    product = content_strategy.get("product_description", "product")
    
    alt_texts = {
        "hero_image": f"Hero image showcasing {product} in lifestyle setting",
        "social_post": f"Social media image featuring {product} for engagement",
        "ad_creative": f"Advertisement creative highlighting {product} benefits",
        "product_showcase": f"Product showcase displaying {product} features"
    }
    
    return alt_texts.get(image_type, f"Marketing image for {product}")

def generate_timestamp() -> str:
    """Generate timestamp for file naming"""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_image_variations(image_type: str, base_prompt: str) -> List[Dict[str, str]]:
    """Generate variations of the base image"""
    
    variations = []
    
    # Create different style variations
    style_variations = {
        "bright": base_prompt + " Bright, high contrast, vibrant colors",
        "minimal": base_prompt + " Minimal, clean, lots of white space",
        "dark": base_prompt + " Dark theme, moody lighting, premium feel"
    }
    
    for style_name, prompt in style_variations.items():
        variations.append({
            "style": style_name,
            "prompt": prompt,
            "description": f"{style_name.title()} version of {image_type}"
        })
    
    return variations

def get_optimization_settings(image_type: str) -> Dict[str, Any]:
    """Get optimization settings for different platforms"""
    
    optimization = {
        "web_quality": 85,
        "mobile_optimized": True,
        "formats": ["PNG", "JPG", "WebP"],
        "compression": "lossless for graphics, lossy for photos",
        "responsive_breakpoints": ["320px", "768px", "1024px", "1920px"]
    }
    
    # Platform-specific optimizations
    if image_type == "social_post":
        optimization["social_platforms"] = {
            "instagram": {"size": "1080x1080", "format": "JPG"},
            "facebook": {"size": "1200x630", "format": "JPG"},
            "twitter": {"size": "1024x512", "format": "JPG"},
            "linkedin": {"size": "1200x627", "format": "PNG"}
        }
    elif image_type == "ad_creative":
        optimization["ad_platforms"] = {
            "facebook_ads": {"size": "1200x628", "text_limit": "20%"},
            "google_ads": {"size": "728x90", "format": "JPG"},
            "display": {"sizes": ["300x250", "728x90", "160x600"]}
        }
    
    return optimization

def generate_email_assets(
    content_strategy: Dict[str, Any],
    brand_colors: str = ""
) -> List[Dict[str, Any]]:
    """Generate email-specific creative assets"""
    
    email_assets = []
    
    # Email header
    header_asset = generate_email_header(content_strategy, brand_colors)
    email_assets.append(header_asset)
    
    # Email hero image
    hero_asset = generate_email_hero(content_strategy, brand_colors)
    email_assets.append(hero_asset)
    
    # Email footer elements
    footer_asset = generate_email_footer(content_strategy, brand_colors)
    email_assets.append(footer_asset)
    
    # CTA buttons
    cta_assets = generate_email_cta_buttons(content_strategy, brand_colors)
    email_assets.extend(cta_assets)
    
    return email_assets

def generate_email_header(content_strategy: Dict[str, Any], brand_colors: str) -> Dict[str, Any]:
    """Generate email header image"""
    
    header_prompt = f"""
    Professional email header, size 600x200px, brand colors {brand_colors}, includes brand elements and product hint: {content_strategy.get('product_description', 'product')}, clean modern style, email-optimized, background with brand colors or subtle gradient, PNG, no background.
    """

    
    try:
        header_result = generate_image(
            prompt=header_prompt,
            style="email header, professional",
            dimensions="600x200"
        )
        
        return {
            "type": "email_header",
            "description": "Professional email header with brand elements",
            "image_obj": header_result.get("image_obj"),
            "dimensions": "600x200",
            "file_name": f"email_header_{generate_timestamp()}.png",
            "usage": "Email campaigns, newsletters"
        }
    except Exception as e:
        return {
            "type": "email_header",
            "description": "Professional email header with brand elements",
            "error": str(e),
            "dimensions": "600x200"
        }

def generate_email_hero(content_strategy: Dict[str, Any], brand_colors: str) -> Dict[str, Any]:
    """Generate email hero section image"""
    
    hero_prompt = f"""
    Email hero section, size 600x400px, brand colors {brand_colors}, product showcase: {content_strategy.get('product_description', 'product')}, engaging modern style, email-optimized, includes value proposition visual and space for CTA, centered clean layout, PNG, no background.
    """
    
    try:
        hero_result = generate_image(
            prompt=hero_prompt,
            style="email hero, engaging, professional",
            dimensions="600x400"
        )
        
        return {
            "type": "email_hero",
            "description": "Engaging hero image for email body",
            "image_obj": hero_result.get("image_obj"),
            "dimensions": "600x400",
            "file_name": f"email_hero_{generate_timestamp()}.png",
            "usage": "Email body, main content section"
        }
    except Exception as e:
        return {
            "type": "email_hero",
            "description": "Engaging hero image for email body",
            "error": str(e),
            "dimensions": "600x400"
        }

def generate_email_footer(content_strategy: Dict[str, Any], brand_colors: str) -> Dict[str, Any]:
    """Generate email footer elements"""
    
    footer_prompt = f"""
    Email footer, size 600x150px, brand colors {brand_colors}, minimal professional style, includes social media icons and space for contact info, clean organized layout, trust-building design, PNG, no background.
    """

    
    try:
        footer_result = generate_image(
            prompt=footer_prompt,
            style="email footer, professional, minimal",
            dimensions="600x150"
        )
        
        return {
            "type": "email_footer",
            "description": "Professional email footer with social elements",
            "image_obj": footer_result.get("image_obj"),
            "dimensions": "600x150",
            "file_name": f"email_footer_{generate_timestamp()}.png",
            "usage": "Email footer, contact information section"
        }
    except Exception as e:
        return {
            "type": "email_footer",
            "description": "Professional email footer with social elements",
            "error": str(e),
            "dimensions": "600x150"
        }

def generate_email_cta_buttons(content_strategy: Dict[str, Any], brand_colors: str) -> List[Dict[str, Any]]:
    """Generate CTA button designs for emails"""
    
    cta_buttons = []
    
    # Primary CTA button
    primary_cta_prompt = f"""
    Bold clickable CTA button for email, text "Get Started", size 200x50px, brand colors {brand_colors}, white text, rounded corners, strong contrast, subtle shadow, clean professional style, PNG, no background.
    """
    
    try:
        primary_result = generate_image(
            prompt=primary_cta_prompt,
            style="CTA button, professional, clickable",
            dimensions="200x50"
        )
        
        cta_buttons.append({
            "type": "primary_cta_button",
            "description": "Primary call-to-action button",
            "image_obj": primary_result.get("image_obj"),
            "dimensions": "200x50",
            "file_name": f"primary_cta_{generate_timestamp()}.png",
            "usage": "Main email CTA, primary actions"
        })
    except Exception as e:
        cta_buttons.append({
            "type": "primary_cta_button",
            "description": "Primary call-to-action button",
            "error": str(e),
            "dimensions": "200x50"
        })
    
    # Secondary CTA button
    secondary_cta_prompt = f"""
    Subtle secondary CTA button for email, text "Learn More" or "View Details", size 180x40px, outline style using brand colors {brand_colors}, white or dark text, rounded corners, clean professional look, less prominent than primary, PNG, no background.
    """

    
    try:
        secondary_result = generate_image(
            prompt=secondary_cta_prompt,
            style="secondary CTA, subtle, professional",
            dimensions="180x40"
        )
        
        cta_buttons.append({
            "type": "secondary_cta_button",
            "description": "Secondary call-to-action button",
            "image_obj": primary_result.get("image_obj"),
            "dimensions": "180x40",
            "file_name": f"secondary_cta_{generate_timestamp()}.png",
            "usage": "Secondary email CTA, supporting actions"
        })
    except Exception as e:
        cta_buttons.append({
            "type": "secondary_cta_button",
            "description": "Secondary call-to-action button",
            "error": str(e),
            "dimensions": "180x40"
        })
    
    return cta_buttons

def create_image_templates(content_strategy: Dict[str, Any]) -> Dict[str, Any]:
    """Create reusable image templates"""
    
    templates = {
        "social_media_template": {
            "dimensions": ["1080x1080", "1080x1350", "1200x628"],
            "elements": ["logo_space", "text_area", "product_space", "cta_area"],
            "style_guide": "Brand consistent, social optimized"
        },
        "email_template": {
            "dimensions": ["600x400", "600x300", "600x600"],
            "elements": ["header", "hero_section", "content_blocks", "footer"],
            "style_guide": "Email compliant, professional"
        },
        "ad_creative_template": {
            "dimensions": ["1200x628", "300x250", "728x90"],
            "elements": ["headline_space", "value_prop", "product_image", "cta_button"],
            "style_guide": "Conversion focused, platform compliant"
        }
    }
    
    return templates

