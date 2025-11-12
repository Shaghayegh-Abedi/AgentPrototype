#!/usr/bin/env python3
"""
AutoMark: A Mini Multi-Agent Marketing Team

Main entry point for the marketing campaign automation system.
Usage: python automark.py --brief "Your campaign brief here"
"""
import argparse
import json
import sys
import io
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Load .env from project root
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from memory.context_manager import ContextManager
from agents.manager_agent import ManagerAgent


def format_output(final_output: Dict[str, Any]) -> str:
    """
    Format the final output in a readable way.
    
    Args:
        final_output: The integrated campaign output
    
    Returns:
        Formatted string representation
    """
    output_lines = []
    output_lines.append("\n" + "="*70)
    output_lines.append("🎯 CAMPAIGN PLAN GENERATED")
    output_lines.append("="*70 + "\n")
    
    # Core Information
    if final_output.get("campaign_brief"):
        output_lines.append(f"📋 Brief: {final_output['campaign_brief']}\n")
    
    if final_output.get("strategy"):
        output_lines.append(f"💡 Strategy: {final_output['strategy']}\n")
    
    if final_output.get("target_audience"):
        output_lines.append(f"🎯 Target Audience: {final_output['target_audience']}\n")
    
    if final_output.get("core_message"):
        output_lines.append(f"💬 Core Message: {final_output['core_message']}\n")
    
    # Recommended Channels
    if final_output.get("recommended_channels"):
        output_lines.append("📡 Recommended Channels:")
        for channel in final_output['recommended_channels']:
            if channel:
                output_lines.append(f"   • {channel}")
        output_lines.append("")
    
    # Content Examples
    content = final_output.get("content_examples", {})
    if content:
        output_lines.append("📝 Content Examples:")
        output_lines.append("-" * 70)
        
        if content.get("slogan"):
            output_lines.append(f"\n🏷️  Slogan: {content['slogan']}\n")
        
        if content.get("instagram_captions"):
            output_lines.append("📸 Instagram Captions:")
            for i, caption in enumerate(content['instagram_captions'], 1):
                if isinstance(caption, dict):
                    tone = caption.get("tone", "")
                    text = caption.get("caption", "")
                    output_lines.append(f"   {i}. [{tone}] {text}")
                else:
                    output_lines.append(f"   {i}. {caption}")
            output_lines.append("")
        
        if content.get("facebook_ads"):
            output_lines.append("📘 Facebook Ads:")
            for i, ad in enumerate(content['facebook_ads'], 1):
                if isinstance(ad, dict):
                    ad_type = ad.get("type", "")
                    copy = ad.get("copy", "")
                    output_lines.append(f"   {i}. [{ad_type}] {copy}")
                else:
                    output_lines.append(f"   {i}. {ad}")
            output_lines.append("")
        
        if content.get("twitter_post"):
            output_lines.append(f"🐦 Twitter/X Post: {content['twitter_post']}\n")
        
        if content.get("linkedin_post"):
            output_lines.append(f"💼 LinkedIn Post: {content['linkedin_post']}\n")
    
    # Outreach Templates
    outreach = final_output.get("outreach_templates", {})
    if outreach:
        output_lines.append("📧 Outreach Templates:")
        output_lines.append("-" * 70)
        
        if outreach.get("cold_email"):
            email = outreach["cold_email"]
            if isinstance(email, dict):
                output_lines.append(f"\n📨 Cold Outreach Email:")
                if email.get("subject"):
                    output_lines.append(f"   Subject: {email['subject']}")
                if email.get("body"):
                    output_lines.append(f"   Body: {email['body']}")
                output_lines.append("")
        
        if outreach.get("influencer_pitch"):
            pitch = outreach["influencer_pitch"]
            if isinstance(pitch, dict):
                output_lines.append(f"🌟 Influencer Pitch:")
                if pitch.get("subject"):
                    output_lines.append(f"   Subject: {pitch['subject']}")
                if pitch.get("body"):
                    output_lines.append(f"   Body: {pitch['body']}")
                output_lines.append("")
    
    # KPIs
    if final_output.get("kpis"):
        output_lines.append("📊 Suggested KPIs:")
        for kpi in final_output['kpis']:
            if kpi:
                output_lines.append(f"   • {kpi}")
        output_lines.append("")
    
    # Timing Recommendations
    if final_output.get("timing_recommendations"):
        output_lines.append(f"⏰ Timing: {final_output['timing_recommendations']}\n")
    
    output_lines.append("="*70)
    output_lines.append("✅ Campaign plan complete! Check campaign_context.json for full details.")
    output_lines.append("="*70 + "\n")
    
    return "\n".join(output_lines)


def output_json(final_output: Dict[str, Any], output_file: str = None):
    """
    Output the final result as JSON (matching the requested format).
    
    Args:
        final_output: The integrated campaign output
        output_file: Optional file path to save JSON
    """
    # Format to match the requested structure
    json_output = {
        "target_audience": final_output.get("target_audience", "General audience"),
        "core_message": final_output.get("core_message", ""),
        "content_examples": []
    }
    
    # Add content examples
    content = final_output.get("content_examples", {})
    if content.get("slogan"):
        json_output["content_examples"].append(f"Slogan: {content['slogan']}")
    
    if content.get("instagram_captions"):
        for caption in content['instagram_captions']:
            if isinstance(caption, dict):
                json_output["content_examples"].append(f"Instagram: {caption.get('caption', '')}")
            else:
                json_output["content_examples"].append(f"Instagram: {caption}")
    
    if content.get("facebook_ads"):
        for ad in content['facebook_ads']:
            if isinstance(ad, dict):
                json_output["content_examples"].append(f"Facebook: {ad.get('copy', '')}")
            else:
                json_output["content_examples"].append(f"Facebook: {ad}")
    
    if content.get("twitter_post"):
        json_output["content_examples"].append(f"Twitter: {content['twitter_post']}")
    
    if content.get("linkedin_post"):
        json_output["content_examples"].append(f"LinkedIn: {content['linkedin_post']}")
    
    # Add email drafts
    outreach = final_output.get("outreach_templates", {})
    if outreach.get("cold_email"):
        email = outreach["cold_email"]
        if isinstance(email, dict) and email.get("body"):
            json_output["content_examples"].append(f"Email draft: {email['body'][:100]}...")
    
    json_str = json.dumps(json_output, indent=2, ensure_ascii=False)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"\n💾 JSON output saved to: {output_file}")
    else:
        print("\n" + "="*70)
        print("📄 JSON OUTPUT:")
        print("="*70)
        print(json_str)
        print("="*70)


def main():
    """Main entry point for AutoMark."""
    parser = argparse.ArgumentParser(
        description="AutoMark: A Mini Multi-Agent Marketing Team",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python automark.py --brief "Promote eco-friendly water bottle"
  python automark.py --brief "Launch new fitness app" --revisions 2
  python automark.py --brief "Promote eco-friendly water bottle" --json-output campaign.json
        """
    )
    
    parser.add_argument(
        "--brief",
        type=str,
        required=True,
        help="Campaign brief describing what to promote"
    )
    
    parser.add_argument(
        "--revisions",
        type=int,
        default=1,
        help="Maximum number of revision cycles (default: 1)"
    )
    
    parser.add_argument(
        "--data-file",
        type=str,
        default="data/marketing_data.csv",
        help="Path to marketing dataset CSV (default: data/marketing_data.csv)"
    )
    
    parser.add_argument(
        "--context-file",
        type=str,
        default="campaign_context.json",
        help="Path to context file (default: campaign_context.json)"
    )
    
    parser.add_argument(
        "--json-output",
        type=str,
        default=None,
        help="Save JSON output to file (optional)"
    )
    
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output only JSON format (no human-readable output)"
    )
    
    args = parser.parse_args()
    
    # Validate data file exists
    data_file_path = Path(args.data_file)
    if not data_file_path.exists():
        print(f"⚠️  Warning: Data file not found at {args.data_file}")
        print("   Continuing without dataset (agent will use general knowledge)...")
    
    try:
        # Initialize context manager
        context_manager = ContextManager(context_file=args.context_file)
        
        # Initialize manager agent
        manager = ManagerAgent(
            context_manager=context_manager,
            data_file=args.data_file
        )
        
        # Execute campaign
        final_output = manager.execute_campaign(
            brief=args.brief,
            max_revisions=args.revisions
        )
        
        # Output results
        if not args.json_only:
            print(format_output(final_output))
        
        output_json(final_output, args.json_output)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Campaign execution interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

