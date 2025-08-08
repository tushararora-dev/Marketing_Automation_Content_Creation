import requests
import json
import time
from typing import Dict, Any, Optional
from config.settings import load_config, get_groq_headers

# Load configuration
config = load_config()

def get_llm_response(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: str = None,
    max_tokens: int = None,
    temperature: float = None
) -> str:
    """
    Get response from Groq LLM API using Llama3-8B-8192 model
    
    Args:
        prompt: User prompt/question
        system_message: System context message
        model: Model to use (defaults to config)
        max_tokens: Max tokens to generate
        temperature: Temperature for generation
    
    Returns:
        Generated text response
    """
    
    # Use config defaults if not specified
    if model is None:
        model = config["groq_model"]
    if max_tokens is None:
        max_tokens = config["max_tokens"]
    if temperature is None:
        temperature = config["temperature"]
    
    # Prepare request payload
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 1,
        "stream": False
    }
    
    # Get headers
    headers = get_groq_headers(config["groq_api_key"])
    
    # Make API request with retries
    for attempt in range(config["max_retries"]):
        try:
            response = requests.post(
                config["groq_api_url"],
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract generated text
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    content = response_data["choices"][0]["message"]["content"]
                    return content.strip()
                else:
                    raise Exception("No choices in response")
                    
            elif response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            if attempt == config["max_retries"] - 1:
                raise Exception(f"Failed to get LLM response after {config['max_retries']} attempts: {str(e)}")
            
            # Wait before retry
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    
    raise Exception("Failed to get LLM response")

def get_llm_response_with_context(
    prompt: str,
    context: Dict[str, Any],
    system_message: str = "You are a helpful assistant."
) -> str:
    """
    Get LLM response with additional context information
    
    Args:
        prompt: User prompt/question
        context: Additional context information
        system_message: System context message
    
    Returns:
        Generated text response
    """
    
    # Build enhanced prompt with context
    context_str = format_context_for_prompt(context)
    enhanced_prompt = f"{context_str}\n\n{prompt}"
    
    return get_llm_response(enhanced_prompt, system_message)

def format_context_for_prompt(context: Dict[str, Any]) -> str:
    """Format context dictionary for inclusion in prompt"""
    
    context_lines = ["Context Information:"]
    
    for key, value in context.items():
        if isinstance(value, (str, int, float)):
            context_lines.append(f"- {key.replace('_', ' ').title()}: {value}")
        elif isinstance(value, list):
            if value:  # Only add if list is not empty
                context_lines.append(f"- {key.replace('_', ' ').title()}: {', '.join(map(str, value))}")
        elif isinstance(value, dict):
            context_lines.append(f"- {key.replace('_', ' ').title()}:")
            for sub_key, sub_value in value.items():
                context_lines.append(f"  - {sub_key.replace('_', ' ').title()}: {sub_value}")
    
    return '\n'.join(context_lines)

def validate_llm_response(response: str, expected_elements: list = None) -> bool:
    """
    Validate LLM response contains expected elements
    
    Args:
        response: LLM response text
        expected_elements: List of elements that should be present
    
    Returns:
        True if response is valid, False otherwise
    """
    
    if not response or len(response.strip()) < 10:
        return False
    
    if expected_elements:
        response_lower = response.lower()
        for element in expected_elements:
            if element.lower() not in response_lower:
                return False
    
    return True

def clean_llm_response(response: str) -> str:
    """
    Clean and format LLM response
    
    Args:
        response: Raw LLM response
    
    Returns:
        Cleaned response text
    """
    
    # Remove extra whitespace
    cleaned = response.strip()
    
    # Remove common artifacts
    artifacts = [
        "Here is", "Here's", "I'll help you", "I can help", 
        "Let me", "I'll create", "I'll generate"
    ]
    
    for artifact in artifacts:
        if cleaned.startswith(artifact):
            # Find the end of the sentence and remove it
            first_sentence_end = cleaned.find('.', len(artifact))
            if first_sentence_end != -1:
                cleaned = cleaned[first_sentence_end + 1:].strip()
    
    # Normalize line breaks
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n') if line.strip())
    
    return cleaned

def generate_with_fallback(
    primary_prompt: str,
    fallback_prompt: str,
    system_message: str = "You are a helpful assistant."
) -> str:
    """
    Generate response with fallback prompt if primary fails
    
    Args:
        primary_prompt: Primary prompt to try first
        fallback_prompt: Fallback prompt if primary fails
        system_message: System message
    
    Returns:
        Generated response
    """
    
    try:
        # Try primary prompt
        response = get_llm_response(primary_prompt, system_message)
        
        # Validate response
        if validate_llm_response(response):
            return response
        else:
            raise Exception("Invalid primary response")
            
    except Exception:
        # Fall back to simpler prompt
        try:
            return get_llm_response(fallback_prompt, system_message)
        except Exception as e:
            # Return generic response as last resort
            return generate_generic_response(fallback_prompt)

def generate_generic_response(prompt: str) -> str:
    """Generate a generic response when all else fails"""
    
    if "email" in prompt.lower():
        return """
        Subject: Important Update
        
        Hello,
        
        We hope this message finds you well. We wanted to reach out with some important information about our latest offering.
        
        Thank you for your continued support.
        
        Best regards,
        The Team
        """
    elif "ad" in prompt.lower() or "copy" in prompt.lower():
        return """
        Headline: Discover Something Amazing
        
        Transform your experience with our innovative solution. Join thousands of satisfied customers who have already made the switch.
        
        CTA: Learn More Today
        """
    elif "social" in prompt.lower():
        return "Exciting news coming your way! Stay tuned for something special. #innovation #exciting #update"
    else:
        return "Thank you for your interest. We're here to help you achieve your goals with our quality solutions."

def batch_llm_requests(
    requests_data: list,
    system_message: str = "You are a helpful assistant.",
    batch_size: int = 5,
    delay_between_batches: float = 1.0
) -> list:
    """
    Process multiple LLM requests in batches with rate limiting
    
    Args:
        requests_data: List of prompt strings or dicts with prompt info
        system_message: System message for all requests
        batch_size: Number of requests per batch
        delay_between_batches: Delay in seconds between batches
    
    Returns:
        List of responses
    """
    
    responses = []
    
    # Process requests in batches
    for i in range(0, len(requests_data), batch_size):
        batch = requests_data[i:i + batch_size]
        batch_responses = []
        
        for request_data in batch:
            try:
                if isinstance(request_data, str):
                    prompt = request_data
                elif isinstance(request_data, dict):
                    prompt = request_data.get("prompt", "")
                    system_msg = request_data.get("system_message", system_message)
                else:
                    continue
                
                response = get_llm_response(prompt, system_msg)
                batch_responses.append(response)
                
            except Exception as e:
                batch_responses.append(f"Error: {str(e)}")
        
        responses.extend(batch_responses)
        
        # Delay between batches to avoid rate limits
        if i + batch_size < len(requests_data):
            time.sleep(delay_between_batches)
    
    return responses

def optimize_prompt_for_model(prompt: str, model_type: str = "llama3") -> str:
    """
    Optimize prompt for specific model characteristics
    
    Args:
        prompt: Original prompt
        model_type: Type of model being used
    
    Returns:
        Optimized prompt
    """
    
    if model_type.lower() == "llama3":
        # Llama3 optimizations
        optimized = prompt
        
        # Add clear structure indicators
        if not prompt.startswith(("Create", "Generate", "Write", "Develop")):
            optimized = f"Create the following: {prompt}"
        
        # Add output format hints
        if "format" not in prompt.lower():
            optimized += "\n\nProvide a clear, well-structured response."
        
        return optimized
    
    return prompt

def get_model_info() -> Dict[str, Any]:
    """Get information about the current model configuration"""
    
    return {
        "model": config["groq_model"],
        "api_endpoint": config["groq_api_url"],
        "max_tokens": config["max_tokens"],
        "temperature": config["temperature"],
        "max_retries": config["max_retries"]
    }

def test_llm_connection() -> bool:
    """Test connection to LLM API"""
    
    try:
        response = get_llm_response(
            "Hello, please respond with 'Connection successful'",
            "You are a test assistant.",
            max_tokens=50
        )
        
        return "successful" in response.lower()
        
    except Exception:
        return False

def estimate_token_count(text: str) -> int:
    """
    Rough estimation of token count for text
    
    Args:
        text: Input text
    
    Returns:
        Estimated token count
    """
    
    # Rough estimation: ~4 characters per token on average
    return len(text) // 4

def chunk_text_for_model(text: str, max_tokens: int = None) -> list:
    """
    Chunk text to fit within model token limits
    
    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
    
    Returns:
        List of text chunks
    """
    
    if max_tokens is None:
        max_tokens = config["max_tokens"] // 2  # Leave room for response
    
    # Estimate max characters per chunk
    max_chars = max_tokens * 4
    
    chunks = []
    sentences = text.split('.')
    current_chunk = ""
    
    for sentence in sentences:
        sentence_with_period = sentence.strip() + '.'
        
        if len(current_chunk + sentence_with_period) <= max_chars:
            current_chunk += sentence_with_period + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence_with_period + " "
    
    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
