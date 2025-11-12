"""
JSON-based context manager for agent collaboration.
Stores intermediate results so agents can read each other's work.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class ContextManager:
    """Manages shared context between agents using JSON storage."""
    
    def __init__(self, context_file: str = "campaign_context.json"):
        self.context_file = Path(context_file)
        self.context: Dict[str, Any] = self._load_context()
    
    def _load_context(self) -> Dict[str, Any]:
        """Load existing context from JSON file."""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._init_context()
        return self._init_context()
    
    def _init_context(self) -> Dict[str, Any]:
        """Initialize empty context structure."""
        return {
            "campaign_id": None,
            "brief": None,
            "created_at": None,
            "updated_at": None,
            "manager_plan": None,
            "copywriter_outputs": [],
            "data_analyst_outputs": [],
            "outreach_outputs": [],
            "revisions": [],
            "final_output": None
        }
    
    def save_context(self):
        """Persist context to JSON file."""
        self.context["updated_at"] = datetime.now().isoformat()
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
    
    def set_brief(self, brief: str):
        """Store the initial campaign brief."""
        self.context["brief"] = brief
        self.context["created_at"] = datetime.now().isoformat()
        self.context["campaign_id"] = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.save_context()
    
    def set_manager_plan(self, plan: Dict[str, Any]):
        """Store the manager's task breakdown and plan."""
        self.context["manager_plan"] = plan
        self.save_context()
    
    def add_copywriter_output(self, output: Dict[str, Any]):
        """Add copywriter agent output."""
        output["timestamp"] = datetime.now().isoformat()
        self.context["copywriter_outputs"].append(output)
        self.save_context()
    
    def add_data_analyst_output(self, output: Dict[str, Any]):
        """Add data analyst agent output."""
        output["timestamp"] = datetime.now().isoformat()
        self.context["data_analyst_outputs"].append(output)
        self.save_context()
    
    def add_outreach_output(self, output: Dict[str, Any]):
        """Add outreach agent output."""
        output["timestamp"] = datetime.now().isoformat()
        self.context["outreach_outputs"].append(output)
        self.save_context()
    
    def add_revision(self, agent: str, feedback: str, revised_output: Dict[str, Any]):
        """Record a revision request and response."""
        revision = {
            "agent": agent,
            "feedback": feedback,
            "revised_output": revised_output,
            "timestamp": datetime.now().isoformat()
        }
        self.context["revisions"].append(revision)
        self.save_context()
    
    def set_final_output(self, output: Dict[str, Any]):
        """Store the final integrated campaign output."""
        self.context["final_output"] = output
        self.save_context()
    
    def get_context_summary(self) -> str:
        """Get a human-readable summary of current context."""
        summary = []
        if self.context["brief"]:
            summary.append(f"Brief: {self.context['brief']}")
        if self.context["manager_plan"]:
            summary.append(f"Plan: {json.dumps(self.context['manager_plan'], indent=2)}")
        if self.context["copywriter_outputs"]:
            summary.append(f"Copywriter outputs: {len(self.context['copywriter_outputs'])} items")
        if self.context["data_analyst_outputs"]:
            summary.append(f"Data analyst outputs: {len(self.context['data_analyst_outputs'])} items")
        if self.context["outreach_outputs"]:
            summary.append(f"Outreach outputs: {len(self.context['outreach_outputs'])} items")
        return "\n".join(summary)
    
    def clear_context(self):
        """Clear all context (useful for new campaigns)."""
        self.context = self._init_context()
        self.save_context()

