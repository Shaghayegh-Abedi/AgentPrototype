"""
Data Analyst Agent: Analyzes marketing data to suggest audience segments and channels.
"""
from typing import Dict, Any, Optional
import pandas as pd
import json
import os
from pathlib import Path
from .base_agent import BaseAgent


class DataAnalystAgent(BaseAgent):
    """Specialist agent for analyzing marketing data and suggesting strategies."""
    
    def __init__(self, context_manager, data_file: str = "data/marketing_data.csv", **kwargs):
        super().__init__(context_manager, **kwargs)
        self.data_file = Path(data_file)
        self.dataset = None
        self._load_dataset()
    
    def _load_dataset(self):
        """Load the marketing dataset."""
        if self.data_file.exists():
            try:
                self.dataset = pd.read_csv(self.data_file)
            except Exception as e:
                print(f"Warning: Could not load dataset: {e}")
                self.dataset = None
        else:
            print(f"Warning: Dataset file not found at {self.data_file}")
            self.dataset = None
    
    def _get_dataset_summary(self) -> str:
        """Get a summary of the dataset for the LLM."""
        if self.dataset is None or self.dataset.empty:
            return "No dataset available. Using general marketing knowledge."
        
        summary = f"Dataset shape: {self.dataset.shape}\n"
        summary += f"Columns: {', '.join(self.dataset.columns.tolist())}\n"
        
        # Get some sample statistics
        if len(self.dataset) > 0:
            summary += f"\nSample data (first 5 rows):\n{self.dataset.head().to_string()}\n"
            
            # Try to get some basic stats for numeric columns
            numeric_cols = self.dataset.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                summary += f"\nBasic statistics:\n{self.dataset[numeric_cols].describe().to_string()}"
        
        return summary
    
    def execute_task(self, task_description: str, **kwargs) -> Dict[str, Any]:
        """
        Analyze data and suggest audience segments and channels.
        
        Args:
            task_description: What analysis is needed
        
        Returns:
            Dictionary with audience segments and channel recommendations
        """
        context = self._get_context_summary()
        brief = self.context_manager.context.get("brief", "")
        dataset_summary = self._get_dataset_summary()
        
        system_prompt = """You are an expert marketing data analyst. You analyze marketing datasets, 
        identify patterns, and provide data-driven recommendations for audience targeting and channel selection. 
        You base your recommendations on actual data insights when available, and use marketing best practices 
        when data is limited."""
        
        user_prompt = f"""Based on the following campaign brief, context, and dataset, provide data-driven recommendations:

Campaign Brief: {brief}

Context from team: {context}

Dataset Information:
{dataset_summary}

Task: {task_description}

Please provide:
1. Target audience segments (with demographics, psychographics, and data-backed reasoning)
2. Recommended marketing channels (prioritized with rationale)
3. Optimal timing/frequency suggestions
4. Key performance indicators (KPIs) to track

Format your response as JSON with this structure:
{{
    "target_audiences": [
        {{
            "segment_name": "...",
            "demographics": "...",
            "psychographics": "...",
            "size_estimate": "...",
            "data_evidence": "..."
        }}
    ],
    "recommended_channels": [
        {{
            "channel": "...",
            "priority": "high/medium/low",
            "rationale": "...",
            "expected_reach": "..."
        }}
    ],
    "timing_recommendations": "...",
    "suggested_kpis": ["...", "..."]
}}"""
        
        response = self._call_llm(system_prompt, user_prompt, temperature=0.6)
        
        # Try to parse JSON response
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(response)
        except json.JSONDecodeError:
            # Fallback
            analysis = {
                "target_audiences": [],
                "recommended_channels": [],
                "timing_recommendations": "Based on general best practices",
                "suggested_kpis": ["reach", "engagement", "conversions"],
                "raw_response": response
            }
        
        # Store in context
        output = {
            "task": task_description,
            "analysis": analysis,
            "agent": "data_analyst"
        }
        self.context_manager.add_data_analyst_output(output)
        
        return output

