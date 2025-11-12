"""
Copywriter Agent: Generates ad copy, slogans, and social media captions.
"""
from typing import Dict, Any, Optional
import json
from .base_agent import BaseAgent


class CopywriterAgent(BaseAgent):
    """Specialist agent for creating marketing copy and content."""
    
    def execute_task(self, task_description: str, brand_info: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate marketing copy based on the task description.
        
        Args:
            task_description: What copy is needed (e.g., "Create Instagram captions")
            brand_info: Additional brand information
        
        Returns:
            Dictionary with generated copy content
        """
        # Get context about the campaign
        context = self._get_context_summary()
        brief = self.context_manager.context.get("brief", "")
        
        system_prompt = """You are an expert marketing copywriter with years of experience creating 
        compelling ad copy, slogans, and social media content. Your writing is creative, engaging, 
        and aligned with brand voice. You understand target audiences and craft messages that resonate."""
        
        user_prompt = f"""Based on the following campaign brief and context, create marketing copy:

Campaign Brief: {brief}

Context from team: {context}

Task: {task_description}
{f"Additional brand information: {brand_info}" if brand_info else ""}

Please generate:
1. A core brand slogan/tagline (1-2 lines)
2. 3 Instagram captions (different tones: inspirational, informative, call-to-action)
3. 2 Facebook ad copy variations (short and long form)
4. 1 Twitter/X post
5. 1 LinkedIn post

Format your response as JSON with this structure:
{{
    "slogan": "your slogan here",
    "instagram_captions": [
        {{"tone": "inspirational", "caption": "..."}},
        {{"tone": "informative", "caption": "..."}},
        {{"tone": "call-to-action", "caption": "..."}}
    ],
    "facebook_ads": [
        {{"type": "short", "copy": "..."}},
        {{"type": "long", "copy": "..."}}
    ],
    "twitter_post": "...",
    "linkedin_post": "..."
}}"""
        
        response = self._call_llm(system_prompt, user_prompt, temperature=0.8)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response if it's wrapped in markdown
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            copy_content = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: create structured output from text
            copy_content = {
                "slogan": "Generated from response",
                "raw_response": response,
                "instagram_captions": [],
                "facebook_ads": [],
                "twitter_post": "",
                "linkedin_post": ""
            }
        
        # Store in context
        output = {
            "task": task_description,
            "content": copy_content,
            "agent": "copywriter"
        }
        self.context_manager.add_copywriter_output(output)
        
        return output

