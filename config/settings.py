import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config() -> Dict[str, Any]:
    """Load configuration settings from environment variables with defaults"""
    
    config = {
        # API Keys (required: override defaults in .env file)
        "groq_api_key": os.getenv("GROQ_API_KEY", ""),
        "huggingface_api_key": os.getenv("HUGGINGFACE_API_KEY", ""),
        
        # Model Configuration
        "groq_model": "llama3-8b-8192",
        "huggingface_image_model": "stabilityai/stable-diffusion-3-medium-diffusers",
        
        # API Endpoints
        "groq_api_url": "https://api.groq.com/openai/v1/chat/completions",
        "huggingface_api_url": "https://api-inference.huggingface.co/models",
        
        # LLM Generation Settings
        "max_tokens": 2048,
        "temperature": 0.7,
        "max_retries": 3,
        
        # File Storage Paths
        "export_dir": "export",
        "memory_dir": "memory",
        
        # Image Generation
        "image_width": 1024,
        "image_height": 1024,
        "num_inference_steps": 20,
        
        # Generation Limits
        "max_emails": 10,
        "max_sms": 5,
        "max_ad_variants": 5,
        "max_social_captions": 3,
    }

    return config

def get_groq_headers(api_key: str) -> Dict[str, str]:
    """Get headers for Groq API requests"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def get_huggingface_headers(api_key: str) -> Dict[str, str]:
    """Get headers for HuggingFace API requests"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
