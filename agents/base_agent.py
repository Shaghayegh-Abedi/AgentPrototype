"""
Base class for all specialist agents.
Provides common functionality for LLM interactions and context management.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

from memory.context_manager import ContextManager
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


class BaseAgent(ABC):
    """Base class for all specialist agents."""
    
    def __init__(self, context_manager: ContextManager, model: str = "gpt-4o-mini"):
        self.context_manager = context_manager
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment. Please set it in .env file.")
        
        # Check if this is an OpenRouter key (starts with sk-or-v1)
        if api_key.startswith("sk-or-v1"):
            # Use OpenRouter endpoint
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            # Use standard OpenAI endpoint
            self.client = OpenAI(api_key=api_key)
        
        self.model = model
        self.name = self.__class__.__name__
    
    def _call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """Make a call to OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _get_context_summary(self) -> str:
        """Get relevant context for the agent."""
        return self.context_manager.get_context_summary()
    
    @abstractmethod
    def execute_task(self, task_description: str, **kwargs) -> Dict[str, Any]:
        """Execute the agent's specific task. Must be implemented by subclasses."""
        pass

