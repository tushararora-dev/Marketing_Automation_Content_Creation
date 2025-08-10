import requests
import json
import time
from typing import Dict, Any, Optional
from config.settings import load_config, get_huggingface_headers
from io import BytesIO
from PIL import Image

# Load configuration
config = load_config()
import replicate


# Initialize Replicate client once (you can move this outside the function if you want)
replicate_client = replicate.Client(api_token=config["replicate_api_key"])




#----- Used for Hugging face---
def generate_image(
    prompt: str,
    style: str = "professional, high quality",
    dimensions: str = "1072x1072"
) -> Dict[str, Any]:
    """
    Generate image using HuggingFace Inference API
    
    Args:
        prompt: Text prompt for image generation
        style: Style guidance for the image
        dimensions: Image dimensions (width x height)
    
    Returns:
        Dictionary with image URL and metadata
    """
    
    # Enhance prompt with style and quality modifiers
    enhanced_prompt = f"{prompt}, {style}, high resolution, detailed"
    
    # Parse dimensions
    # width, height = parse_dimensions(dimensions)
    width = 1072
    height = 1072
    
    # Prepare API request
    api_url = f"{config['huggingface_api_url']}/{config['huggingface_image_model']}"
    headers = get_huggingface_headers(config["huggingface_api_key"])
    
    payload = {
        "inputs": enhanced_prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": config.get("num_inference_steps", 20),
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy"
        }
    }
    
    # Make API request with retries
    for attempt in range(config["max_retries"]):
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # HuggingFace returns image data directly
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                # Save image temporarily and return info
                timestamp = str(int(time.time()))
                filename = f"generated_image_{timestamp}.png"
                
                # In a real implementation, you'd save to cloud storage
                # For now, return metadata
                return {
                    "image_obj": image,
                    # "url": f"[GENERATED_IMAGE_{timestamp}]",
                    "filename": filename,
                    "prompt": enhanced_prompt,
                    "dimensions": f"{width}x{height}",
                    "size_bytes": len(image_data),
                    "format": "PNG",
                    "generated_at": timestamp,
                    "model": config['huggingface_image_model']
                }
                
            elif response.status_code == 503:  # Model loading
                wait_time = 10 + (attempt * 5)
                time.sleep(wait_time)
                continue
            elif response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            if attempt == config["max_retries"] - 1:
                raise Exception(f"Failed to generate image after {config['max_retries']} attempts: {str(e)}")
            
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    
    raise Exception("Failed to generate image")







def generate_multiple_images(
    prompts: list,
    style: str = "professional, high quality",
    dimensions: str = "1024x1024"
) -> list:
    """
    Generate multiple images from a list of prompts
    
    Args:
        prompts: List of text prompts
        style: Style guidance for all images
        dimensions: Image dimensions
    
    Returns:
        List of image results
    """
    
    results = []
    
    for i, prompt in enumerate(prompts):
        try:
            # Add small delay between requests to avoid rate limits
            if i > 0:
                time.sleep(2)
            
            result = generate_image(prompt, style, dimensions)
            results.append(result)
            
        except Exception as e:
            # Add error result
            results.append({
                "error": str(e),
                "prompt": prompt,
                "status": "failed"
            })
    
    return results

def generate_campaign_images(
    prompt: str,
    image_type: str,
    brand_colors: list = None
) -> Dict[str, Any]:
    """
    Generate images specifically for marketing campaigns
    
    Args:
        prompt: Base prompt for image generation
        image_type: Type of image (email_header, product_showcase, etc.)
        brand_colors: List of brand colors to incorporate
    
    Returns:
        Generated image with campaign-specific metadata
    """
    
    # Enhance prompt based on image type
    type_enhancements = {
        "email_header": "professional email header, clean layout, business style",
        "product_showcase": "product photography, clean background, commercial quality",
        "social_proof": "testimonial design, trustworthy, clean typography",
        "trust_badges": "security badges, professional icons, trust symbols",
        "cta_button": "button design, clickable appearance, modern UI",
        "ad_creative": "advertising creative, eye-catching, persuasive design",
        "hero_image": "hero banner, lifestyle imagery, aspirational",
        "social_post": "social media post, engaging, trendy design"
    }
    
    enhancement = type_enhancements.get(image_type, "professional, high quality")
    
    # Add brand colors if provided
    if brand_colors:
        color_text = f"using brand colors {', '.join(brand_colors)}"
        enhanced_prompt = f"{prompt}, {enhancement}, {color_text}"
    else:
        enhanced_prompt = f"{prompt}, {enhancement}"
    
    # Get appropriate dimensions for image type
    dimensions = get_image_type_dimensions(image_type)
    
    # Generate image
    result = generate_image(enhanced_prompt, enhancement, dimensions)
    
    # Add campaign-specific metadata
    result.update({
        "image_type": image_type,
        "brand_colors": brand_colors or [],
        "campaign_ready": True,
        "usage_rights": "Generated for campaign use"
    })
    
    return result

def get_image_type_dimensions(image_type: str) -> str:
    """Get appropriate dimensions for different image types"""
    
    dimensions_map = {
        "email_header": "600x200",
        "product_showcase": "800x600", 
        "social_proof": "600x400",
        "trust_badges": "800x100",
        "cta_button": "300x60",
        "ad_creative": "1200x628",
        "hero_image": "1920x1080",
        "social_post": "1080x1080",
        "email_hero": "600x400",
        "email_footer": "600x150"
    }
    
    return dimensions_map.get(image_type, "1024x1024")

def parse_dimensions(dimensions_str: str) -> tuple:
    """Parse dimensions string into width and height integers"""
    
    try:
        width_str, height_str = dimensions_str.split('x')
        width = int(width_str.strip())
        height = int(height_str.strip())
        return width, height
    except (ValueError, AttributeError):
        # Default dimensions if parsing fails
        return 1024, 1024

def optimize_prompt_for_image_generation(prompt: str, image_type: str) -> str:
    """Optimize prompt for better image generation results"""
    
    # Add quality modifiers
    quality_modifiers = [
        "high resolution",
        "professional quality", 
        "detailed",
        "sharp focus",
        "well lit"
    ]
    
    # Add style modifiers based on image type
    if image_type in ["email_header", "trust_badges"]:
        style_modifiers = ["clean", "minimal", "business professional"]
    elif image_type in ["social_post", "ad_creative"]:
        style_modifiers = ["eye-catching", "modern", "engaging"]
    elif image_type == "product_showcase":
        style_modifiers = ["product photography", "commercial", "clean background"]
    else:
        style_modifiers = ["professional", "modern"]
    
    # Combine prompt with modifiers
    optimized = f"{prompt}, {', '.join(style_modifiers)}, {', '.join(quality_modifiers)}"
    
    return optimized

def validate_image_generation_params(prompt: str, dimensions: str) -> bool:
    """Validate image generation parameters"""
    
    if not prompt or len(prompt.strip()) < 5:
        return False
    
    try:
        width, height = parse_dimensions(dimensions)
        # Check reasonable dimension limits
        if width < 64 or width > 2048 or height < 64 or height > 2048:
            return False
    except:
        return False
    
    return True

def get_image_generation_tips() -> Dict[str, list]:
    """Get tips for better image generation"""
    
    return {
        "prompt_writing": [
            "Be specific about style, mood, and composition",
            "Include quality modifiers like 'high resolution', 'professional'",
            "Specify lighting conditions (natural light, studio lighting, etc.)",
            "Mention the intended use case (email header, social post, etc.)",
            "Include brand-relevant descriptors"
        ],
        "style_guidance": [
            "Use 'clean and minimal' for business applications",
            "Use 'eye-catching and modern' for social media",
            "Use 'professional photography' for product shots",
            "Use 'lifestyle imagery' for aspirational content",
            "Use 'flat design' for icons and simple graphics"
        ],
        "technical_tips": [
            "Square dimensions (1:1) work best for social media",
            "Horizontal dimensions (16:9) work best for headers",
            "Vertical dimensions (9:16) work best for stories",
            "Lower resolution for web use, higher for print",
            "Consider file size for email deliverability"
        ]
    }

def estimate_generation_time(dimensions: str, complexity: str = "medium") -> int:
    """Estimate image generation time in seconds"""
    
    width, height = parse_dimensions(dimensions)
    total_pixels = width * height
    
    # Base time calculation
    base_time = 10  # seconds
    
    # Adjust for image size
    if total_pixels > 1000000:  # > 1MP
        base_time += 15
    elif total_pixels > 500000:  # > 0.5MP
        base_time += 10
    elif total_pixels > 250000:  # > 0.25MP
        base_time += 5
    
    # Adjust for complexity
    complexity_multipliers = {
        "simple": 0.7,
        "medium": 1.0,
        "complex": 1.5,
        "very_complex": 2.0
    }
    
    multiplier = complexity_multipliers.get(complexity, 1.0)
    
    return int(base_time * multiplier)

def create_image_variations(
    base_prompt: str,
    image_type: str,
    num_variations: int = 3
) -> list:
    """Create multiple variations of an image with different styles"""
    
    style_variations = [
        "bright and vibrant",
        "minimal and clean", 
        "dark and moody",
        "colorful and energetic",
        "elegant and sophisticated"
    ]
    
    variations = []
    
    for i in range(min(num_variations, len(style_variations))):
        style = style_variations[i]
        
        try:
            variation_prompt = f"{base_prompt}, {style} style"
            result = generate_campaign_images(
                prompt=variation_prompt,
                image_type=image_type
            )
            
            result["variation_style"] = style
            result["variation_number"] = i + 1
            variations.append(result)
            
        except Exception as e:
            variations.append({
                "error": str(e),
                "variation_style": style,
                "variation_number": i + 1,
                "status": "failed"
            })
    
    return variations

def check_huggingface_model_status() -> Dict[str, Any]:
    """Check if the HuggingFace model is loaded and ready"""
    
    api_url = f"{config['huggingface_api_url']}/{config['huggingface_image_model']}"
    headers = get_huggingface_headers(config["huggingface_api_key"])
    
    try:
        # Send a simple test request
        test_payload = {
            "inputs": "test image",
            "parameters": {"width": 512, "height": 512}
        }
        
        response = requests.post(
            api_url,
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {"status": "ready", "message": "Model is loaded and ready"}
        elif response.status_code == 503:
            return {"status": "loading", "message": "Model is loading, please wait"}
        else:
            return {"status": "error", "message": f"Status code: {response.status_code}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}
