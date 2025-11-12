# AutoMarketing Agent 🚀

A professional AI-powered multi-agent marketing campaign generator built with Streamlit. This application uses specialized AI agents to create comprehensive marketing campaigns, including content, strategies, and outreach templates.

## Features

- **Multi-Agent System**: Collaborative AI agents working together to create marketing campaigns
  - **Manager Agent**: Orchestrates the entire campaign workflow
  - **Copywriter Agent**: Generates creative content (slogans, captions, ads)
  - **Data Analyst Agent**: Analyzes marketing data and provides insights
  - **Outreach Agent**: Creates email templates and pitch materials

- **Professional Web Interface**: Modern Streamlit UI with:
  - Campaign creation and management
  - Real-time progress tracking
  - Results visualization
  - Export capabilities (JSON)

- **Context Management**: Persistent memory system that stores campaign context and history

- **Data-Driven Insights**: Leverages marketing data to inform campaign strategies

## Requirements

- Python 3.8 or higher
- OpenAI API key (or OpenRouter API key)
- All dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with your API key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   
   # Optional: Custom login credentials (defaults: admin/admin123)
   # APP_USERNAME=admin
   # APP_PASSWORD=admin123
   ```
   
   **Note**: You can use either:
   - Standard OpenAI API key (starts with `sk-`)
   - OpenRouter API key (starts with `sk-or-v1-`)

## Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser, typically at `http://localhost:8501`.

### Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

You can customize these by setting `APP_USERNAME` and `APP_PASSWORD` in your `.env` file.

## Usage

### Creating a Campaign

1. **Login** to the application using the default credentials
2. Navigate to the **"Create Campaign"** tab
3. Enter your campaign brief describing:
   - Campaign goals
   - Target audience
   - Key messages
   - Product/service details
4. Configure settings in the sidebar:
   - Max revisions (1-5)
   - Data file path (default: `data/marketing_data.csv`)
   - Context file path (default: `campaign_context.json`)
5. Click **"Run Campaign"** and wait for the AI agents to generate your marketing plan

### Viewing Results

After campaign execution, navigate to the **"View Results"** tab to see:
- Campaign overview and strategy
- Target audience analysis
- Recommended channels
- Content examples (slogans, Instagram captions, Facebook ads, Twitter posts, LinkedIn posts)
- Outreach templates (cold emails, influencer pitches, media pitches)
- Suggested KPIs

### Progress Log

Check the **"Progress Log"** tab to view detailed execution logs and agent activities.

## Project Structure

```
AgentPrototype/
├── app.py                      # Main Streamlit application
├── automark.py                 # CLI version of the application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── campaign_context.json       # Campaign context storage (auto-generated)
├── agents/                     # AI agent modules
│   ├── base_agent.py          # Base class for all agents
│   ├── manager_agent.py       # Manager/orchestrator agent
│   ├── copywriter_agent.py    # Content generation agent
│   ├── data_analyst_agent.py  # Data analysis agent
│   ├── outreach_agent.py      # Outreach template agent
│   ├── agent_communication.py # Inter-agent communication
│   └── specialized_prompts.py # Agent-specific prompts
├── memory/                     # Memory and context management
│   ├── context_manager.py    # Context persistence
│   └── vector_memory.py       # Vector-based memory system
└── data/                       # Marketing data
    └── marketing_data.csv     # Sample marketing dataset
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI or OpenRouter API key
- `APP_USERNAME` (optional): Custom login username (default: `admin`)
- `APP_PASSWORD` (optional): Custom login password (default: `admin123`)

### Campaign Settings

Configure in the Streamlit sidebar:
- **Max Revisions**: Number of revision cycles (1-5)
- **Data File**: Path to marketing dataset CSV
- **Context File**: Path to campaign context JSON file

## Dependencies

- `openai>=1.12.0` - OpenAI API client
- `langgraph>=0.0.40` - Workflow orchestration
- `langchain>=0.1.0` - LLM framework
- `langchain-openai>=0.0.5` - LangChain OpenAI integration
- `pandas>=2.0.0` - Data analysis
- `python-dotenv>=1.0.0` - Environment variable management
- `streamlit>=1.28.0` - Web interface
- `moviepy>=1.0.3` - Media processing
- `pillow>=10.0.0` - Image processing
- `numpy>=1.24.0` - Numerical computing

## Features in Detail

### Multi-Agent Workflow

The application uses a sophisticated agent-based architecture:
1. **Manager Agent** receives the campaign brief and creates an execution plan
2. **Data Analyst Agent** analyzes marketing data to inform strategy
3. **Copywriter Agent** generates creative content across multiple channels
4. **Outreach Agent** creates professional outreach templates
5. All agents collaborate through the **Context Manager** for shared memory

### Context Management

Campaign context is automatically saved to `campaign_context.json`, allowing:
- Campaign history tracking
- Context persistence across sessions
- Results recovery

### Export Options

- Download campaign results as JSON
- View raw JSON data
- Access campaign history

## Troubleshooting

### API Key Issues

If you see "API Key Not Configured":
- Ensure `.env` file exists in the project root
- Verify `OPENAI_API_KEY` is set correctly
- Check that the API key is valid and has sufficient credits

### Import Errors

If you encounter import errors:
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.8 or higher
- Check that you're running from the project root directory

### Campaign Execution Errors

- Check the **Progress Log** tab for detailed error messages
- Ensure `data/marketing_data.csv` exists
- Verify API key has sufficient quota/credits

## License

This project is provided as-is for demonstration and development purposes.

## Support

For issues or questions, please check:
- The Progress Log tab for execution details
- Error messages in the Streamlit interface
- Campaign context file for saved data

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**

