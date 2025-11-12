"""
Streamlit UI for AutoMarketing Agent
A professional web interface for the multi-agent marketing team.
"""
import streamlit as st
import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import traceback

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(dotenv_path=project_root / ".env")

from memory.context_manager import ContextManager
from agents.manager_agent import ManagerAgent

# Page configuration
st.set_page_config(
    page_title="AutoMarketing Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AutoMarketing Agent - AI-Powered Marketing Campaign Generator"
    }
)

# Initialize session state early for authentication check
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Professional CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Cards */
    .campaign-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: #1f2937 !important;
    }
    
    .campaign-card * {
        color: #1f2937 !important;
    }
    
    .campaign-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .info-card {
        background: #f0f9ff;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        overflow: visible;
        min-height: auto;
    }
    
    .info-card * {
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .success-card {
        background: #f0fdf4;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        overflow: visible;
        min-height: auto;
    }
    
    .success-card * {
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .warning-card {
        background: #fffbeb;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        overflow: visible;
        min-height: auto;
    }
    
    .warning-card * {
        color: #1f2937 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-processing {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-error {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: all 0.3s ease;
        color: #1f2937 !important;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea !important;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Content Areas */
    .content-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #1f2937 !important;
    }
    
    .content-section * {
        color: #1f2937 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Text Areas */
    .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        color: #1f2937 !important;
    }
    
    /* Text Area Labels */
    .stTextArea label {
        color: #1f2937 !important;
    }
    
    /* Text Area Container */
    .stTextArea>div>div {
        color: #1f2937 !important;
    }
    
    /* Disabled Text Areas (like in Progress Log) */
    .stTextArea>div>div>textarea:disabled {
        color: #1f2937 !important;
        background-color: #f9fafb !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #1f2937;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 700;
    }
    
    h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.75rem;
    }
    
    h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-size: 1.25rem;
        color: #374151;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 2rem 0;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    
    /* Channel Badges */
    .channel-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        color: #1f2937 !important;
    }
    
    .kpi-card * {
        color: #1f2937 !important;
    }
    
    .kpi-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Login Form Styling */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        padding: 2rem;
    }
    
    .login-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 3rem;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
        max-width: 450px;
        width: 100%;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: #6b7280;
        font-size: 0.95rem;
    }
    
    .login-input {
        margin-bottom: 1.5rem;
    }
    
    .login-button {
        width: 100%;
        margin-top: 1rem;
    }
    
    .error-message {
        background: #fee2e2;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #dc2626;
    }
    
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'campaign_results' not in st.session_state:
        st.session_state.campaign_results = None
    if 'campaign_running' not in st.session_state:
        st.session_state.campaign_running = False
    if 'progress_log' not in st.session_state:
        st.session_state.progress_log = []
    if 'context_manager' not in st.session_state:
        st.session_state.context_manager = None


def check_login():
    """Check if user is authenticated. Returns True if authenticated."""
    import os
    
    # Get credentials from environment variables or use defaults
    default_username = os.getenv("APP_USERNAME", "admin")
    default_password = os.getenv("APP_PASSWORD", "admin123")
    
    if st.session_state.authenticated:
        return True
    
    # Hide sidebar and header on login page using CSS
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden !important;
        }
        footer {
            visibility: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize login error state
    if 'login_error' not in st.session_state:
        st.session_state.login_error = None
    
    # Add some vertical spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login box container
        st.markdown("""
        <div class="login-box">
            <div class="login-header">
                <div class="login-title">🔐 AutoMarketing Agent</div>
                <div class="login-subtitle">Please login to access the application</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show error message if login failed
        if st.session_state.login_error:
            st.error(f"❌ {st.session_state.login_error}")
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_button:
                if username == default_username and password == default_password:
                    st.session_state.authenticated = True
                    st.session_state.login_error = None
                    st.rerun()
                else:
                    st.session_state.login_error = "Invalid username or password. Please try again."
                    st.rerun()
        
        # Footer info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 1rem 0;">
            <p><strong>Default Credentials:</strong></p>
            <p>Username: <code>admin</code> | Password: <code>admin123</code></p>
            <p style="margin-top: 1rem; font-size: 0.8rem;">💡 Configure custom credentials via environment variables:<br>
            <code>APP_USERNAME</code> and <code>APP_PASSWORD</code></p>
        </div>
        """, unsafe_allow_html=True)
    
    return False


def create_metric_card(label: str, value: str, icon: str = ""):
    """Create a professional metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def format_campaign_output(final_output: Dict[str, Any]) -> None:
    """Display campaign output in a professional format."""
    
    # Campaign Header with Metrics
    st.markdown("---")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_metric_card("Status", "Complete", "✅")
    with col2:
        audience = final_output.get("target_audience", "N/A")
        create_metric_card("Audience", audience[:20] + "..." if len(audience) > 20 else audience, "🎯")
    with col3:
        channels = final_output.get("recommended_channels", [])
        create_metric_card("Channels", str(len(channels)), "📡")
    with col4:
        content = final_output.get("content_examples", {})
        content_count = sum([
            len(content.get("instagram_captions", [])),
            len(content.get("facebook_ads", [])),
            len([content.get("slogan")] if content.get("slogan") else []),
            len([content.get("twitter_post")] if content.get("twitter_post") else []),
            len([content.get("linkedin_post")] if content.get("linkedin_post") else [])
        ])
        create_metric_card("Content", str(content_count), "📝")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Campaign Overview
    st.markdown("### 📋 Campaign Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if final_output.get("campaign_brief"):
            st.markdown("#### Campaign Brief")
            st.markdown(f'<div class="info-card">{final_output["campaign_brief"]}</div>', unsafe_allow_html=True)
        
        if final_output.get("target_audience"):
            st.markdown("#### Target Audience")
            st.markdown(f'<div class="success-card">{final_output["target_audience"]}</div>', unsafe_allow_html=True)
    
    with col2:
        if final_output.get("strategy"):
            st.markdown("#### Strategy")
            st.markdown(f'<div class="success-card">{final_output["strategy"]}</div>', unsafe_allow_html=True)
        
        if final_output.get("core_message"):
            st.markdown("#### Core Message")
            st.markdown(f'<div class="info-card" style="font-size: 1.1rem; font-weight: 600; color: #667eea; word-wrap: break-word; overflow-wrap: break-word; white-space: normal; overflow: visible;">{final_output["core_message"]}</div>', unsafe_allow_html=True)
    
    # Recommended Channels
    if final_output.get("recommended_channels"):
        st.markdown("### 📡 Recommended Channels")
        channel_html = '<div style="margin: 1rem 0;">'
        for channel in final_output['recommended_channels']:
            if channel:
                channel_html += f'<span class="channel-badge">{channel}</span>'
        channel_html += '</div>'
        st.markdown(channel_html, unsafe_allow_html=True)
    
    # Timing Recommendations
    if final_output.get("timing_recommendations"):
        st.markdown("### ⏰ Timing Recommendations")
        st.markdown(f'<div class="warning-card">{final_output["timing_recommendations"]}</div>', unsafe_allow_html=True)
    
    # Content Examples
    content = final_output.get("content_examples", {})
    if content:
        st.markdown("---")
        st.markdown("### 📝 Content Examples")
        
        tabs = st.tabs(["🏷️ Slogan", "📸 Instagram", "📘 Facebook", "🐦 Twitter", "💼 LinkedIn"])
        
        with tabs[0]:
            if content.get("slogan"):
                st.markdown(f'<div class="success-card" style="font-size: 1.25rem; font-weight: 600; text-align: center; padding: 2rem;">{content["slogan"]}</div>', unsafe_allow_html=True)
        
        with tabs[1]:
            if content.get("instagram_captions"):
                st.markdown("#### Instagram Captions")
                for i, caption in enumerate(content['instagram_captions'], 1):
                    if isinstance(caption, dict):
                        tone = caption.get("tone", "")
                        text = caption.get("caption", "")
                        st.markdown(f"**Caption {i}** - *{tone}*")
                        st.markdown(f'<div class="info-card">{text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"**Caption {i}**")
                        st.markdown(f'<div class="info-card">{caption}</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            if content.get("facebook_ads"):
                st.markdown("#### Facebook Ads")
                for i, ad in enumerate(content['facebook_ads'], 1):
                    if isinstance(ad, dict):
                        ad_type = ad.get("type", "")
                        copy = ad.get("copy", "")
                        st.markdown(f"**Ad {i}** - *{ad_type}*")
                        st.markdown(f'<div class="info-card">{copy}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"**Ad {i}**")
                        st.markdown(f'<div class="info-card">{ad}</div>', unsafe_allow_html=True)
        
        with tabs[3]:
            if content.get("twitter_post"):
                st.markdown("#### Twitter/X Post")
                st.markdown(f'<div class="info-card" style="padding: 1.5rem; font-size: 1rem; line-height: 1.6;">{content["twitter_post"]}</div>', unsafe_allow_html=True)
        
        with tabs[4]:
            if content.get("linkedin_post"):
                st.markdown("#### LinkedIn Post")
                st.markdown(f'<div class="info-card" style="padding: 1.5rem; font-size: 1rem; line-height: 1.6;">{content["linkedin_post"]}</div>', unsafe_allow_html=True)
    
    # Outreach Templates
    outreach = final_output.get("outreach_templates", {})
    if outreach:
        st.markdown("---")
        st.markdown("### 📧 Outreach Templates")
        
        outreach_tabs = st.tabs(["📨 Cold Email", "🌟 Influencer Pitch", "📰 Media Pitch"])
        
        with outreach_tabs[0]:
            if outreach.get("cold_email"):
                email = outreach["cold_email"]
                if isinstance(email, dict):
                    if email.get("subject"):
                        st.markdown(f"#### Subject Line")
                        st.markdown(f'<div class="success-card" style="font-weight: 600;">{email["subject"]}</div>', unsafe_allow_html=True)
                    if email.get("body"):
                        st.markdown("#### Email Body")
                        st.markdown(f'<div class="info-card" style="white-space: pre-wrap; line-height: 1.8;">{email["body"]}</div>', unsafe_allow_html=True)
        
        with outreach_tabs[1]:
            if outreach.get("influencer_pitch"):
                pitch = outreach["influencer_pitch"]
                if isinstance(pitch, dict):
                    if pitch.get("subject"):
                        st.markdown(f"#### Subject Line")
                        st.markdown(f'<div class="success-card" style="font-weight: 600;">{pitch["subject"]}</div>', unsafe_allow_html=True)
                    if pitch.get("body"):
                        st.markdown("#### Pitch Body")
                        st.markdown(f'<div class="info-card" style="white-space: pre-wrap; line-height: 1.8;">{pitch["body"]}</div>', unsafe_allow_html=True)
        
        with outreach_tabs[2]:
            if outreach.get("media_pitch"):
                media_pitch = outreach["media_pitch"]
                if isinstance(media_pitch, dict):
                    if media_pitch.get("subject"):
                        st.markdown(f"#### Subject Line")
                        st.markdown(f'<div class="success-card" style="font-weight: 600;">{media_pitch["subject"]}</div>', unsafe_allow_html=True)
                    if media_pitch.get("body"):
                        st.markdown("#### Media Pitch Body")
                        st.markdown(f'<div class="info-card" style="white-space: pre-wrap; line-height: 1.8;">{media_pitch["body"]}</div>', unsafe_allow_html=True)
    
    # KPIs
    if final_output.get("kpis"):
        st.markdown("---")
        st.markdown("### 📊 Suggested KPIs")
        kpi_cols = st.columns(min(len(final_output['kpis']), 3))
        for i, kpi in enumerate(final_output['kpis']):
            if kpi:
                with kpi_cols[i % 3]:
                    st.markdown(f'<div class="kpi-card">📈 {kpi}</div>', unsafe_allow_html=True)


def execute_campaign(
    brief: str,
    max_revisions: int = 1,
    data_file: str = "data/marketing_data.csv",
    context_file: str = "campaign_context.json",
    progress_placeholder=None
) -> Optional[Dict[str, Any]]:
    """Execute campaign and return results."""
    try:
        # Initialize context manager
        context_manager = ContextManager(context_file=context_file)
        st.session_state.context_manager = context_manager
        
        # Initialize manager agent
        manager = ManagerAgent(
            context_manager=context_manager,
            data_file=data_file
        )
        
        # Create a custom stdout capture for progress
        old_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Execute campaign
        final_output = manager.execute_campaign(
            brief=brief,
            max_revisions=max_revisions
        )
        
        # Restore stdout and get captured output
        sys.stdout = old_stdout
        output_text = captured_output.getvalue()
        captured_output.close()
        
        # Store progress log
        if output_text:
            st.session_state.progress_log = [line for line in output_text.split('\n') if line.strip()]
        else:
            st.session_state.progress_log = ["Campaign execution completed"]
        
        return final_output
        
    except Exception as e:
        # Restore stdout in case of error
        if 'old_stdout' in locals():
            sys.stdout = old_stdout
        if 'captured_output' in locals():
            captured_output.close()
        
        error_msg = f"Error executing campaign: {str(e)}"
        error_trace = traceback.format_exc()
        
        # Store error in progress log
        st.session_state.progress_log = [error_msg, error_trace]
        
        return None


def main():
    """Main application."""
    initialize_session_state()
    
    # Check authentication
    if not check_login():
        return
    
    # Professional Header
    st.markdown('<h1 class="main-header">AutoMarketing Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Multi-Agent Marketing Campaign Generator</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        # Logout button at the top
        st.markdown("### 👤 User Session")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.campaign_results = None
            st.session_state.campaign_running = False
            st.session_state.progress_log = []
            st.rerun()
        st.markdown("---")
        st.markdown("### ⚙️ Configuration")
        
        # API Key check with professional styling
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ **API Key Not Configured**")
            st.markdown("Please create a `.env` file and add your `OPENAI_API_KEY`")
            st.markdown("---")
        else:
            st.success("✅ **API Key Configured**")
            masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
            st.caption(f"Key: `{masked_key}`")
            st.markdown("---")
        
        # Configuration Section
        st.markdown("#### 🎛️ Campaign Settings")
        max_revisions = st.slider(
            "Max Revisions",
            1, 5, 1,
            help="Maximum number of revision cycles for quality improvement"
        )
        data_file = st.text_input(
            "Data File",
            "data/marketing_data.csv",
            help="Path to marketing dataset CSV"
        )
        context_file = st.text_input(
            "Context File",
            "campaign_context.json",
            help="Path to context file for storing campaign data"
        )
        
        st.markdown("---")
        
        # Campaign history with professional styling
        st.markdown("#### 📚 Campaign History")
        if Path(context_file).exists():
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
                    if context_data.get("brief"):
                        brief_text = context_data.get('brief', 'N/A')[:50]
                        st.info(f"**Last Campaign:**\n{brief_text}...")
                        if context_data.get("created_at"):
                            created = context_data['created_at']
                            try:
                                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                                st.caption(f"Created: {dt.strftime('%Y-%m-%d %H:%M')}")
                            except:
                                st.caption(f"Created: {created}")
                    else:
                        st.caption("No previous campaigns")
            except Exception as e:
                st.caption("No previous campaigns")
        else:
            st.caption("No previous campaigns")
        
        st.markdown("---")
        
        # Clear context button
        if st.button("🗑️ Clear Context", help="Clear all campaign context"):
            try:
                context_manager = ContextManager(context_file=context_file)
                context_manager.clear_context()
                st.success("Context cleared successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing context: {e}")
    
    # Main content area with professional tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Create Campaign", "📊 View Results", "📝 Progress Log"])
    
    with tab1:
        st.markdown("## 🚀 Create New Campaign")
        st.markdown("Enter your campaign brief below and let our AI agents create a comprehensive marketing plan for you.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Campaign brief input with better styling
        brief = st.text_area(
            "Campaign Brief",
            placeholder="Describe your campaign goals, target audience, and key messages...\n\nExample: Promote an eco-friendly water bottle to environmentally conscious millennials aged 25-35, emphasizing sustainability and style.",
            height=180,
            help="Provide a detailed description of what you want to promote and to whom"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Run button with better layout
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            run_button = st.button("🚀 Run Campaign", type="primary", use_container_width=True)
        
        # Execute campaign
        if run_button:
            if not brief.strip():
                st.error("⚠️ Please enter a campaign brief to continue")
            else:
                st.session_state.campaign_running = True
                
                # Professional progress container
                progress_container = st.container()
                with progress_container:
                    st.markdown("### ⏳ Campaign Execution in Progress")
                    st.markdown("Our AI agents are working on your campaign...")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_details = st.empty()
                    
                    # Status updates with professional styling
                    status_text.info("📋 **Starting Campaign Execution**")
                    status_details.caption("Initializing AI agents and preparing campaign plan...")
                    progress_bar.progress(5)
                    
                    try:
                        # Execute campaign with spinner for visual feedback
                        status_text.info("🤖 **AI Agents Working**")
                        status_details.caption("Manager, Copywriter, Data Analyst, and Outreach agents are collaborating...")
                        progress_bar.progress(20)
                        
                        with st.spinner("⏳ Generating your marketing campaign... This may take 30-60 seconds."):
                            result = execute_campaign(
                                brief=brief,
                                max_revisions=max_revisions,
                                data_file=data_file,
                                context_file=context_file,
                                progress_placeholder=status_text
                            )
                        
                        progress_bar.progress(90)
                        
                        if result:
                            st.session_state.campaign_results = result
                            progress_bar.progress(100)
                            status_text.success("✅ **Campaign Completed Successfully!**")
                            status_details.caption("Your marketing campaign has been generated. Check the View Results tab to see the complete plan.")
                            st.balloons()
                            st.session_state.campaign_running = False
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.info("💡 **Tip**: Navigate to the 'View Results' tab to see your complete campaign plan.")
                        else:
                            progress_bar.progress(0)
                            status_text.error("❌ **Campaign Execution Failed**")
                            status_details.caption("Please check the Progress Log tab for detailed error information")
                            st.session_state.campaign_running = False
                    
                    except Exception as e:
                        progress_bar.progress(0)
                        status_text.error(f"❌ **Error**: {str(e)}")
                        status_details.caption("An error occurred during campaign execution. Please check the details below.")
                        st.session_state.campaign_running = False
                        with st.expander("Error Details", expanded=False):
                            st.code(traceback.format_exc())
    
    with tab2:
        st.markdown("## 📊 Campaign Results")
        st.markdown("View your complete marketing campaign plan with all generated content and strategies.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Check if we have results
        if st.session_state.campaign_results:
            format_campaign_output(st.session_state.campaign_results)
            
            # Professional export options
            st.markdown("---")
            st.markdown("### 💾 Export Results")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                # JSON download
                json_str = json.dumps(st.session_state.campaign_results, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_str,
                    file_name=f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                # View raw JSON
                if st.button("📄 View Raw JSON", use_container_width=True):
                    st.json(st.session_state.campaign_results)
            
            with col3:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
        
        else:
            # Check if there's a saved context
            context_file = "campaign_context.json"
            if Path(context_file).exists():
                try:
                    with open(context_file, 'r', encoding='utf-8') as f:
                        context_data = json.load(f)
                        if context_data.get("final_output"):
                            st.info("📂 Loading results from saved context...")
                            format_campaign_output(context_data["final_output"])
                            st.session_state.campaign_results = context_data["final_output"]
                        else:
                            st.info("📭 No campaign results found. Create a new campaign to get started!")
                            st.markdown("""
                            ### Getting Started:
                            1. Go to the **Create Campaign** tab
                            2. Enter your campaign brief
                            3. Click **Run Campaign**
                            4. Wait for the agents to generate your marketing plan
                            5. View results in this tab
                            """)
                except Exception as e:
                    st.error(f"Error loading context: {e}")
            else:
                st.info("📭 No campaign results found. Create a new campaign to get started!")
                st.markdown("""
                ### 🚀 Getting Started:
                1. Navigate to the **Create Campaign** tab
                2. Enter your campaign brief in the text area
                3. Click **Run Campaign** to start generation
                4. Wait for the AI agents to create your marketing plan
                5. View your complete campaign results in this tab
                """)
                
                # Quick example
                with st.expander("💡 See an Example Campaign Brief", expanded=False):
                    st.markdown("""
                    **Example Brief:**
                    ```
                    Promote an eco-friendly water bottle to environmentally 
                    conscious millennials aged 25-35. The product is made from 
                    recycled materials, is BPA-free, and features a sleek design. 
                    Target audience values sustainability and style.
                    ```
                    """)
    
    with tab3:
        st.markdown("## 📝 Progress Log")
        st.markdown("View detailed execution logs and agent activities.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.progress_log:
            # Professional log display
            log_text = "\n".join(st.session_state.progress_log)
            st.text_area(
                "Execution Log",
                log_text,
                height=500,
                disabled=True,
                help="Detailed log of campaign execution"
            )
            
            # Log statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Log Lines", len(st.session_state.progress_log))
            with col2:
                error_count = sum(1 for line in st.session_state.progress_log if "error" in line.lower() or "Error" in line)
                st.metric("Errors", error_count)
            with col3:
                success_count = sum(1 for line in st.session_state.progress_log if "complete" in line.lower() or "success" in line.lower())
                st.metric("Success", success_count)
        else:
            st.info("📋 No progress log available. Run a campaign to see progress updates.")
            
            # Try to load from context if available
            context_file = "campaign_context.json"
            if Path(context_file).exists():
                st.markdown("### 📂 Recent Campaign Context")
                try:
                    with open(context_file, 'r', encoding='utf-8') as f:
                        context_data = json.load(f)
                        with st.expander("View Context Data", expanded=False):
                            st.json(context_data)
                except Exception as e:
                    st.error(f"Error loading context: {e}")


# Streamlit runs the script on each interaction
# Call main() to render the app
main()
