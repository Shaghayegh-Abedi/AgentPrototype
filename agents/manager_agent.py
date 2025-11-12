"""
Manager Agent: Orchestrates the marketing team using LangGraph.
Breaks down briefs, assigns tasks, and integrates outputs.
"""
from typing import Dict, Any, List, Optional, TypedDict, Annotated
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from memory.context_manager import ContextManager
from .copywriter_agent import CopywriterAgent
from .data_analyst_agent import DataAnalystAgent
from .outreach_agent import OutreachAgent
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


class AgentState(TypedDict):
    """State structure for the LangGraph workflow."""
    brief: str
    manager_plan: Optional[Dict[str, Any]]
    copywriter_output: Optional[Dict[str, Any]]
    data_analyst_output: Optional[Dict[str, Any]]
    outreach_output: Optional[Dict[str, Any]]
    evaluation: Optional[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]]
    revision_count: int
    max_revisions: int


class ManagerAgent:
    """Manager agent that orchestrates the marketing team."""
    
    def __init__(self, context_manager: ContextManager, data_file: str = "data/marketing_data.csv"):
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
        
        self.model = "gpt-4o-mini"
        
        # Initialize specialist agents
        self.copywriter = CopywriterAgent(context_manager)
        self.data_analyst = DataAnalystAgent(context_manager, data_file=data_file)
        self.outreach = OutreachAgent(context_manager)
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
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
    
    def create_plan(self, brief: str) -> Dict[str, Any]:
        """
        Break down the brief into a structured plan with subtasks.
        
        Args:
            brief: The campaign brief
        
        Returns:
            Dictionary with task breakdown and assignments
        """
        system_prompt = """You are an experienced marketing manager leading a team of specialists:
- Copywriter: Creates ad copy, slogans, social media content
- Data Analyst: Analyzes data to suggest audiences and channels
- Outreach Agent: Drafts emails and influencer pitches

Your job is to break down campaign briefs into specific, actionable tasks for each specialist.
Be strategic and ensure tasks align with the campaign goals."""
        
        user_prompt = f"""Analyze this campaign brief and create a detailed execution plan:

Brief: {brief}

Create a plan that includes:
1. Overall campaign strategy (2-3 sentences)
2. Specific tasks for the Copywriter agent
3. Specific tasks for the Data Analyst agent
4. Specific tasks for the Outreach agent
5. Expected deliverables

Format your response as JSON:
{{
    "strategy": "...",
    "copywriter_tasks": ["task 1", "task 2"],
    "data_analyst_tasks": ["task 1", "task 2"],
    "outreach_tasks": ["task 1", "task 2"],
    "deliverables": ["deliverable 1", "deliverable 2"]
}}"""
        
        response = self._call_llm(system_prompt, user_prompt, temperature=0.6)
        
        # Parse JSON response
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(response)
        except json.JSONDecodeError:
            # Fallback plan
            plan = {
                "strategy": "Execute a multi-channel marketing campaign",
                "copywriter_tasks": [
                    "Create brand slogan and tagline",
                    "Generate social media captions for Instagram, Facebook, Twitter, LinkedIn"
                ],
                "data_analyst_tasks": [
                    "Identify target audience segments",
                    "Recommend best marketing channels"
                ],
                "outreach_tasks": [
                    "Draft influencer collaboration pitches",
                    "Create outreach email templates"
                ],
                "deliverables": [
                    "Complete content library",
                    "Audience targeting strategy",
                    "Outreach templates"
                ],
                "raw_response": response
            }
        
        return plan
    
    def evaluate_outputs(self, state: AgentState) -> Dict[str, Any]:
        """
        Evaluate the quality of agent outputs and provide feedback.
        This enables self-improvement loops.
        
        Args:
            state: Current workflow state
        
        Returns:
            Evaluation with feedback and revision requests
        """
        brief = state.get("brief", "")
        plan = state.get("manager_plan", {})
        copywriter_output = state.get("copywriter_output")
        data_analyst_output = state.get("data_analyst_output")
        outreach_output = state.get("outreach_output")
        
        system_prompt = """You are a quality control manager reviewing marketing campaign outputs.
        You evaluate work against the original brief and plan, checking for:
        - Alignment with campaign goals
        - Quality and creativity
        - Completeness
        - Brand consistency
        
        Provide constructive feedback and identify what needs revision."""
        
        user_prompt = f"""Review the campaign outputs against the brief and plan:

Brief: {brief}

Plan: {json.dumps(plan, indent=2)}

Copywriter Output: {json.dumps(copywriter_output, indent=2) if copywriter_output else "Not available"}

Data Analyst Output: {json.dumps(data_analyst_output, indent=2) if data_analyst_output else "Not available"}

Outreach Output: {json.dumps(outreach_output, indent=2) if outreach_output else "Not available"}

Evaluate each output and determine:
1. Overall quality score (1-10)
2. What's working well
3. What needs improvement
4. Specific revision requests (if any)

Format as JSON:
{{
    "overall_score": 8,
    "strengths": ["..."],
    "improvements_needed": ["..."],
    "revision_requests": [
        {{
            "agent": "copywriter/data_analyst/outreach",
            "issue": "...",
            "request": "..."
        }}
    ],
    "ready_for_final": true/false
}}"""
        
        response = self._call_llm(system_prompt, user_prompt, temperature=0.5)
        
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(response)
        except json.JSONDecodeError:
            evaluation = {
                "overall_score": 7,
                "strengths": ["Outputs generated"],
                "improvements_needed": [],
                "revision_requests": [],
                "ready_for_final": True,
                "raw_response": response
            }
        
        return evaluation
    
    def integrate_outputs(self, state: AgentState) -> Dict[str, Any]:
        """
        Integrate all agent outputs into a final campaign plan.
        
        Args:
            state: Current workflow state
        
        Returns:
            Final integrated campaign output
        """
        brief = state.get("brief", "")
        plan = state.get("manager_plan", {})
        copywriter_output = state.get("copywriter_output", {})
        data_analyst_output = state.get("data_analyst_output", {})
        outreach_output = state.get("outreach_output", {})
        
        # Extract key information from each agent
        copywriter_content = copywriter_output.get("content", {}) if copywriter_output else {}
        analyst_analysis = data_analyst_output.get("analysis", {}) if data_analyst_output else {}
        outreach_content = outreach_output.get("content", {}) if outreach_output else {}
        
        # Build integrated output
        final_output = {
            "campaign_brief": brief,
            "strategy": plan.get("strategy", ""),
            "target_audience": analyst_analysis.get("target_audiences", [{}])[0].get("segment_name", "General audience") if analyst_analysis.get("target_audiences") else "General audience",
            "core_message": copywriter_content.get("slogan", ""),
            "recommended_channels": [ch.get("channel", "") for ch in analyst_analysis.get("recommended_channels", [])],
            "content_examples": {
                "slogan": copywriter_content.get("slogan", ""),
                "instagram_captions": copywriter_content.get("instagram_captions", []),
                "facebook_ads": copywriter_content.get("facebook_ads", []),
                "twitter_post": copywriter_content.get("twitter_post", ""),
                "linkedin_post": copywriter_content.get("linkedin_post", "")
            },
            "outreach_templates": {
                "cold_email": outreach_content.get("cold_outreach_email", {}),
                "influencer_pitch": outreach_content.get("influencer_pitch", {}),
                "media_pitch": outreach_content.get("media_pitch", {})
            },
            "kpis": analyst_analysis.get("suggested_kpis", []),
            "timing_recommendations": analyst_analysis.get("timing_recommendations", "")
        }
        
        return final_output
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for agent orchestration."""
        
        # Define workflow nodes
        def plan_node(state: AgentState) -> Dict[str, Any]:
            """Node: Manager creates the plan."""
            print("📋 Manager: Creating campaign plan...")
            plan = self.create_plan(state["brief"])
            self.context_manager.set_manager_plan(plan)
            return {"manager_plan": plan}
        
        def copywriter_node(state: AgentState) -> Dict[str, Any]:
            """Node: Copywriter executes tasks."""
            print("✍️  Copywriter: Generating marketing copy...")
            plan = state.get("manager_plan", {})
            tasks = plan.get("copywriter_tasks", ["Create marketing copy"])
            task_description = " | ".join(tasks)
            
            output = self.copywriter.execute_task(task_description)
            return {"copywriter_output": output}
        
        def data_analyst_node(state: AgentState) -> Dict[str, Any]:
            """Node: Data Analyst executes tasks."""
            print("📊 Data Analyst: Analyzing data and suggesting strategies...")
            plan = state.get("manager_plan", {})
            tasks = plan.get("data_analyst_tasks", ["Analyze audience and channels"])
            task_description = " | ".join(tasks)
            
            output = self.data_analyst.execute_task(task_description)
            return {"data_analyst_output": output}
        
        def outreach_node(state: AgentState) -> Dict[str, Any]:
            """Node: Outreach Agent executes tasks."""
            print("📧 Outreach: Creating outreach templates...")
            plan = state.get("manager_plan", {})
            tasks = plan.get("outreach_tasks", ["Create outreach content"])
            task_description = " | ".join(tasks)
            
            output = self.outreach.execute_task(task_description)
            return {"outreach_output": output}
        
        def evaluation_node(state: AgentState) -> Dict[str, Any]:
            """Node: Manager evaluates outputs."""
            print("🔍 Manager: Evaluating outputs...")
            evaluation = self.evaluate_outputs(state)
            
            # Store revision if needed
            revision_requests = evaluation.get("revision_requests", [])
            if revision_requests:
                for req in revision_requests:
                    self.context_manager.add_revision(
                        req.get("agent", "unknown"),
                        req.get("request", ""),
                        {}
                    )
            
            return {"evaluation": evaluation, "revision_count": state.get("revision_count", 0) + 1}
        
        def integration_node(state: AgentState) -> Dict[str, Any]:
            """Node: Manager integrates all outputs."""
            print("🔗 Manager: Integrating all outputs...")
            final_output = self.integrate_outputs(state)
            self.context_manager.set_final_output(final_output)
            return {"final_output": final_output}
        
        def should_revise(state: AgentState) -> str:
            """Conditional: Determine if revisions are needed."""
            evaluation = state.get("evaluation", {})
            revision_count = state.get("revision_count", 0)
            max_revisions = state.get("max_revisions", 1)
            
            # Always finalize if we've hit max revisions
            if revision_count >= max_revisions:
                return "finalize"
            
            # Check if there are API errors in outputs - if so, don't revise
            copywriter_output = state.get("copywriter_output", {})
            if copywriter_output and "Error:" in str(copywriter_output.get("content", {}).get("raw_response", "")):
                # API errors detected, just finalize
                return "finalize"
            
            ready = evaluation.get("ready_for_final", True)
            has_requests = len(evaluation.get("revision_requests", [])) > 0
            
            # Only revise if we have requests AND haven't hit max revisions AND outputs are ready
            if has_requests and revision_count < max_revisions and ready:
                return "revise"
            
            return "finalize"
        
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("plan", plan_node)
        workflow.add_node("copywriter", copywriter_node)
        workflow.add_node("data_analyst", data_analyst_node)
        workflow.add_node("outreach", outreach_node)
        workflow.add_node("evaluate", evaluation_node)
        workflow.add_node("integrate", integration_node)
        
        # Define edges - use a join pattern for parallel execution
        workflow.set_entry_point("plan")
        
        # All agents start from plan (parallel execution)
        workflow.add_edge("plan", "copywriter")
        workflow.add_edge("plan", "data_analyst")
        workflow.add_edge("plan", "outreach")
        
        # All agents converge to evaluate (LangGraph will wait for all)
        # We use a simple approach: all agents go to evaluate
        # LangGraph handles this by executing evaluate once all inputs are ready
        workflow.add_edge("copywriter", "evaluate")
        workflow.add_edge("data_analyst", "evaluate")
        workflow.add_edge("outreach", "evaluate")
        
        # Conditional: revise or finalize
        # If revise, go back to plan so all agents re-run
        workflow.add_conditional_edges(
            "evaluate",
            should_revise,
            {
                "revise": "plan",  # Go back to plan to re-run all agents
                "finalize": "integrate"
            }
        )
        
        workflow.add_edge("integrate", END)
        
        return workflow.compile()
    
    def execute_campaign(self, brief: str, max_revisions: int = 1) -> Dict[str, Any]:
        """
        Execute the full campaign workflow.
        
        Args:
            brief: Campaign brief
            max_revisions: Maximum number of revision cycles
        
        Returns:
            Final integrated campaign output
        """
        # Set brief in context
        self.context_manager.set_brief(brief)
        
        # Initialize state
        initial_state: AgentState = {
            "brief": brief,
            "manager_plan": None,
            "copywriter_output": None,
            "data_analyst_output": None,
            "outreach_output": None,
            "evaluation": None,
            "final_output": None,
            "revision_count": 0,
            "max_revisions": max_revisions
        }
        
        # Run the workflow
        print(f"\n🚀 Starting campaign execution for: {brief}\n")
        final_state = self.workflow.invoke(initial_state)
        
        return final_state.get("final_output", {})

