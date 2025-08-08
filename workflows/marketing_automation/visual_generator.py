from typing import Dict, Any, List
from tools.image_gen import generate_campaign_images
from tools.llm_manager import get_llm_response

def generate_visuals(
    brand_analysis: Dict[str, Any],
    campaign_plan: Dict[str, Any],
    emails: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate visual assets for marketing campaign
    
    Args:
        brand_analysis: Brand analysis data
        campaign_plan: Campaign plan with strategy
        emails: Generated email content for context
    
    Returns:
        List of visual assets with metadata
    """
    
    visuals = []
    
    # Generate email header images
    email_headers = generate_email_headers(brand_analysis, emails)
    visuals.extend(email_headers)
    
    # Generate product showcase images
    product_images = generate_product_visuals(brand_analysis, campaign_plan)
    visuals.extend(product_images)
    
    # Generate social proof visuals
    social_proof_images = generate_social_proof_visuals(brand_analysis)
    visuals.extend(social_proof_images)
    
    # Generate CTA button designs
    cta_designs = generate_cta_visuals(brand_analysis, emails)
    visuals.extend(cta_designs)
    
    return visuals

def generate_email_headers(brand_analysis: Dict[str, Any], emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate header images for each email"""
    
    headers = []
    brand_name = brand_analysis.get("brand_name", "Brand")
    brand_colors = brand_analysis.get("colors", ["#007bff", "#ffffff"])
    
    for i, email in enumerate(emails):
        # Create prompt for email header
        header_prompt = f"""
        Create a professional email header image for {brand_name}.
        Email purpose: {email.get('purpose', 'Marketing')}
        Email focus: {email.get('focus', 'Engagement')}
        Brand colors: {', '.join(brand_colors)}
        Style: Clean, modern, professional
        Include: Brand name, relevant imagery for {email.get('focus', 'product')}
        Dimensions: 600x200 pixels
        """
        
        # Generate image
        try:
            image_result = generate_campaign_images(
                prompt=header_prompt,
                image_type="email_header",
                brand_colors=brand_colors
            )
            
            header = {
                "type": "email_header",
                "email_sequence": i + 1,
                "purpose": email.get("purpose", "Marketing"),
                "prompt": header_prompt,
                "image_url": image_result.get("url", ""),
                "dimensions": "600x200",
                "file_name": f"email_header_{i+1}.png",
                "brand_compliant": True
            }
            
            headers.append(header)
            
        except Exception as e:
            # Create placeholder visual description
            header = {
                "type": "email_header",
                "email_sequence": i + 1,
                "purpose": email.get("purpose", "Marketing"),
                "description": f"Professional header for {brand_name} - {email.get('focus', 'marketing')} theme",
                "dimensions": "600x200",
                "file_name": f"email_header_{i+1}.png",
                "error": str(e)
            }
            headers.append(header)
    
    return headers

def generate_product_visuals(brand_analysis: Dict[str, Any], campaign_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate product showcase visuals"""
    
    visuals = []
    brand_name = brand_analysis.get("brand_name", "Brand")
    products = brand_analysis.get("products", ["Main Product"])
    brand_colors = brand_analysis.get("colors", ["#007bff", "#ffffff"])
    
    # Generate main product showcase
    product_prompt = f"""
    Create a professional product showcase image for {brand_name}.
    Products: {', '.join(products[:3])}
    Brand colors: {', '.join(brand_colors)}
    Style: Clean, modern, e-commerce style
    Background: Minimal, white or light gradient
    Layout: Product-focused with clean typography
    Include: Product name, key benefit
    Dimensions: 800x600 pixels
    """
    
    try:
        image_result = generate_campaign_images(
            prompt=product_prompt,
            image_type="product_showcase",
            brand_colors=brand_colors
        )
        
        visual = {
            "type": "product_showcase",
            "products": products[:3],
            "prompt": product_prompt,
            "image_url": image_result.get("url", ""),
            "dimensions": "800x600",
            "file_name": "product_showcase.png",
            "usage": ["email_body", "social_media", "web"]
        }
        
        visuals.append(visual)
        
    except Exception as e:
        visual = {
            "type": "product_showcase",
            "products": products[:3],
            "description": f"Professional product showcase featuring {brand_name} products",
            "dimensions": "800x600",
            "file_name": "product_showcase.png",
            "error": str(e)
        }
        visuals.append(visual)
    
    return visuals

def generate_social_proof_visuals(brand_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate social proof and testimonial visuals"""
    
    visuals = []
    brand_name = brand_analysis.get("brand_name", "Brand")
    brand_colors = brand_analysis.get("colors", ["#007bff", "#ffffff"])
    
    # Generate customer testimonial visual
    testimonial_prompt = f"""
    Create a customer testimonial graphic for {brand_name}.
    Style: Clean, trustworthy, professional
    Include: 5-star rating, customer quote placeholder, customer avatar placeholder
    Brand colors: {', '.join(brand_colors)}
    Background: Light, gradient or solid color
    Typography: Modern, readable
    Dimensions: 600x400 pixels
    Layout: Centered, balanced composition
    """
    
    try:
        image_result = generate_campaign_images(
            prompt=testimonial_prompt,
            image_type="social_proof",
            brand_colors=brand_colors
        )
        
        visual = {
            "type": "social_proof",
            "subtype": "testimonial",
            "prompt": testimonial_prompt,
            "image_url": image_result.get("url", ""),
            "dimensions": "600x400",
            "file_name": "customer_testimonial.png",
            "usage": ["email_footer", "social_media"]
        }
        
        visuals.append(visual)
        
    except Exception as e:
        visual = {
            "type": "social_proof",
            "subtype": "testimonial",
            "description": "Customer testimonial graphic with 5-star rating and quote",
            "dimensions": "600x400",
            "file_name": "customer_testimonial.png",
            "error": str(e)
        }
        visuals.append(visual)
    
    # Generate trust badges visual
    trust_badges_prompt = f"""
    Create a trust badges strip for {brand_name}.
    Include: Security badges, payment methods, satisfaction guarantee
    Style: Professional, trustworthy, clean
    Brand colors: {', '.join(brand_colors)}
    Layout: Horizontal strip, evenly spaced
    Dimensions: 800x100 pixels
    Elements: SSL certificate, money-back guarantee, secure payment icons
    """
    
    try:
        image_result = generate_campaign_images(
            prompt=trust_badges_prompt,
            image_type="trust_badges",
            brand_colors=brand_colors
        )
        
        visual = {
            "type": "trust_badges",
            "prompt": trust_badges_prompt,
            "image_url": image_result.get("url", ""),
            "dimensions": "800x100",
            "file_name": "trust_badges.png",
            "usage": ["email_footer", "checkout_page"]
        }
        
        visuals.append(visual)
        
    except Exception as e:
        visual = {
            "type": "trust_badges",
            "description": "Trust badges strip with security and guarantee icons",
            "dimensions": "800x100",
            "file_name": "trust_badges.png",
            "error": str(e)
        }
        visuals.append(visual)
    
    return visuals

def generate_cta_visuals(brand_analysis: Dict[str, Any], emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate call-to-action button designs"""
    
    visuals = []
    brand_colors = brand_analysis.get("colors", ["#007bff", "#ffffff"])
    
    # Extract unique CTAs from emails
    ctas = []
    for email in emails:
        cta = email.get("cta", {})
        if cta and cta.get("text"):
            ctas.append(cta["text"])
    
    # Remove duplicates
    unique_ctas = list(set(ctas))
    
    for i, cta_text in enumerate(unique_ctas[:3]):  # Limit to 3 CTA designs
        cta_prompt = f"""
        Create a call-to-action button design.
        Button text: "{cta_text}"
        Style: Modern, clickable, professional
        Colors: Primary color {brand_colors[0]}, with good contrast
        Shape: Rounded corners, subtle shadow
        Typography: Bold, readable
        Dimensions: 300x60 pixels
        Include: Hover state suggestion
        """
        
        try:
            image_result = generate_campaign_images(
                prompt=cta_prompt,
                image_type="cta_button",
                brand_colors=brand_colors
            )
            
            visual = {
                "type": "cta_button",
                "button_text": cta_text,
                "prompt": cta_prompt,
                "image_url": image_result.get("url", ""),
                "dimensions": "300x60",
                "file_name": f"cta_button_{i+1}.png",
                "usage": ["email_body", "landing_page"]
            }
            
            visuals.append(visual)
            
        except Exception as e:
            visual = {
                "type": "cta_button",
                "button_text": cta_text,
                "description": f"Professional CTA button with text '{cta_text}'",
                "dimensions": "300x60",
                "file_name": f"cta_button_{i+1}.png",
                "error": str(e)
            }
            visuals.append(visual)
    
    return visuals

def create_visual_style_guide(brand_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Create a visual style guide for consistent branding"""
    
    style_guide = {
        "brand_name": brand_analysis.get("brand_name", "Brand"),
        "primary_colors": brand_analysis.get("colors", ["#007bff"]),
        "secondary_colors": ["#6c757d", "#f8f9fa"],
        "fonts": {
            "primary": "Arial, sans-serif",
            "secondary": "Georgia, serif",
            "headings": "Helvetica, Arial, sans-serif"
        },
        "logo_usage": {
            "min_size": "100px width",
            "clear_space": "Equal to logo height",
            "backgrounds": ["white", "light gray"]
        },
        "image_style": {
            "photography": "Clean, professional, well-lit",
            "illustrations": "Modern, minimal, branded colors",
            "icons": "Line style, consistent weight"
        },
        "layout_principles": {
            "spacing": "Consistent 16px grid",
            "alignment": "Left-aligned text, centered CTAs",
            "hierarchy": "Clear typography scale"
        }
    }
    
    return style_guide

def generate_responsive_variants(visual: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate responsive variants of visuals"""
    
    variants = [visual]
    
    # Generate mobile variant
    if visual["type"] == "email_header":
        mobile_variant = visual.copy()
        mobile_variant["dimensions"] = "320x120"
        mobile_variant["file_name"] = visual["file_name"].replace(".png", "_mobile.png")
        mobile_variant["device"] = "mobile"
        variants.append(mobile_variant)
    
    # Generate tablet variant
    if visual["type"] == "product_showcase":
        tablet_variant = visual.copy()
        tablet_variant["dimensions"] = "600x450"
        tablet_variant["file_name"] = visual["file_name"].replace(".png", "_tablet.png")
        tablet_variant["device"] = "tablet"
        variants.append(tablet_variant)
    
    return variants

def optimize_images_for_email(visuals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimize images for email delivery"""
    
    optimized_visuals = []
    
    for visual in visuals:
        optimized = visual.copy()
        
        # Add email optimization metadata
        optimized["email_optimized"] = True
        optimized["file_size_limit"] = "100KB"
        optimized["format"] = "PNG or JPG"
        optimized["compression"] = "Medium quality, web optimized"
        
        # Add alt text for accessibility
        optimized["alt_text"] = generate_alt_text(visual)
        
        optimized_visuals.append(optimized)
    
    return optimized_visuals

def generate_alt_text(visual: Dict[str, Any]) -> str:
    """Generate descriptive alt text for images"""
    
    visual_type = visual.get("type", "image")
    
    alt_texts = {
        "email_header": f"Header image for {visual.get('purpose', 'marketing')} email",
        "product_showcase": f"Product showcase featuring {visual.get('products', ['products'])}",
        "social_proof": "Customer testimonial with 5-star rating",
        "trust_badges": "Security and trust badges",
        "cta_button": f"Call to action button: {visual.get('button_text', 'Click here')}"
    }
    
    return alt_texts.get(visual_type, "Marketing image")
