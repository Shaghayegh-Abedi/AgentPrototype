"""
Outreach Agent: Drafts outreach emails and influencer pitches.
"""
from typing import Dict, Any, Optional
import json
from .base_agent import BaseAgent


class OutreachAgent(BaseAgent):
    """Specialist agent for creating outreach communications."""
    
    def execute_task(self, task_description: str, recipient_type: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate outreach emails or influencer pitches.
        
        Args:
            task_description: What outreach is needed
            recipient_type: Type of recipient (e.g., "influencer", "partner", "media")
        
        Returns:
            Dictionary with outreach content
        """
        context = self._get_context_summary()
        brief = self.context_manager.context.get("brief", "")
        
        # Get copywriter outputs if available for consistent messaging
        copywriter_outputs = self.context_manager.context.get("copywriter_outputs", [])
        brand_message = ""
        if copywriter_outputs:
            latest_copy = copywriter_outputs[-1].get("content", {})
            brand_message = latest_copy.get("slogan", "")
        
        system_prompt = """You are an expert in outreach and relationship building. You craft personalized, 
        compelling emails and pitches that get responses. Your writing is professional yet warm, 
        value-focused, and respectful of the recipient's time."""
        
        user_prompt = f"""Based on the following campaign brief and context, create outreach content:

Campaign Brief: {brief}

Brand Message: {brand_message}

Context from team: {context}

Task: {task_description}
{f"Recipient type: {recipient_type}" if recipient_type else ""}

Please generate:
1. A cold outreach email (professional, concise, value-focused)
2. An influencer collaboration pitch (engaging, partnership-focused)
3. A media/press pitch (newsworthy angle)
4. A follow-up email template (for non-responses)

Format your response as JSON with this structure:
{{
    "cold_outreach_email": {{
        "subject": "...",
        "body": "...",
        "call_to_action": "..."
    }},
    "influencer_pitch": {{
        "subject": "...",
        "body": "...",
        "value_proposition": "..."
    }},
    "media_pitch": {{
        "subject": "...",
        "body": "...",
        "news_angle": "..."
    }},
    "follow_up_template": {{
        "subject": "...",
        "body": "..."
    }}
}}"""
        
        response = self._call_llm(system_prompt, user_prompt, temperature=0.7)
        
        # Try to parse JSON response
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            outreach_content = json.loads(response)
        except json.JSONDecodeError:
            outreach_content = {
                "cold_outreach_email": {"subject": "", "body": "", "call_to_action": ""},
                "influencer_pitch": {"subject": "", "body": "", "value_proposition": ""},
                "media_pitch": {"subject": "", "body": "", "news_angle": ""},
                "follow_up_template": {"subject": "", "body": ""},
                "raw_response": response
            }
        
        # Store in context
        output = {
            "task": task_description,
            "content": outreach_content,
            "agent": "outreach"
        }
        self.context_manager.add_outreach_output(output)
        
        return output

