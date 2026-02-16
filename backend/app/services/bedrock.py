"""
Amazon Bedrock service for interacting with Nova models
"""
import boto3
import json
from typing import Dict, Any, Optional
from app.config import settings

class BedrockService:
    """Service for interacting with Amazon Bedrock Nova models"""
    
    def __init__(self):
        """Initialize Bedrock client"""
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.aws_region
        )
        
    async def invoke_nova_pro(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Invoke Amazon Nova Pro model for complex reasoning
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Model response
        """
        messages = [{"role": "user", "content": prompt}]
        
        body = {
            "messages": messages,
            "max_tokens": settings.max_tokens,
            "temperature": settings.temperature,
            "top_p": 0.9,
        }
        
        if system_prompt:
            body["system"] = [{"text": system_prompt}]
        
        try:
            response = self.client.invoke_model(
                modelId=settings.nova_pro_model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body
        except Exception as e:
            print(f"Error invoking Nova Pro: {str(e)}")
            raise
    
    async def invoke_nova_lite(self, prompt: str) -> Dict[str, Any]:
        """
        Invoke Amazon Nova Lite model for quick analysis
        
        Args:
            prompt: User prompt
            
        Returns:
            Model response
        """
        messages = [{"role": "user", "content": prompt}]
        
        body = {
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.5,
        }
        
        try:
            response = self.client.invoke_model(
                modelId=settings.nova_lite_model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body
        except Exception as e:
            print(f"Error invoking Nova Lite: {str(e)}")
            raise
    
    def extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """Extract text content from Nova response"""
        try:
            if 'output' in response and 'message' in response['output']:
                content = response['output']['message'].get('content', [])
                if content and len(content) > 0:
                    return content[0].get('text', '')
            return ""
        except Exception as e:
            print(f"Error extracting text from response: {str(e)}")
            return ""

# Global instance
bedrock_service = BedrockService()
