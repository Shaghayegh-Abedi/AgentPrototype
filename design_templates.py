"""
Alternative design templates for the GitHub Pages repository showcase.
You can swap these into generate_repos_page.py to change the look.
"""

# Template 1: Dark Mode
DARK_MODE_CSS = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #c9d1d9;
            background: #0d1117;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #161b22;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            overflow: hidden;
            border: 1px solid #30363d;
        }
        
        header {
            background: linear-gradient(135deg, #1f6feb 0%, #8957e5 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        
        .content {
            padding: 40px;
            background: #0d1117;
        }
        
        .content h2 {
            color: #c9d1d9;
            margin-bottom: 20px;
        }
        
        .repos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .repo-card {
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            background: #161b22;
            transition: all 0.3s;
        }
        
        .repo-card:hover {
            border-color: #1f6feb;
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(31, 111, 235, 0.2);
        }
        
        .repo-name {
            color: #58a6ff;
        }
        
        .repo-description {
            color: #8b949e;
        }
        
        .repo-meta {
            color: #8b949e;
        }
"""

# Template 2: Glassmorphism
GLASSMORPHISM_CSS = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        header {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            color: white;
            padding: 50px;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .content {
            padding: 40px;
            background: rgba(255, 255, 255, 0.05);
        }
        
        .content h2 {
            color: white;
            margin-bottom: 20px;
        }
        
        .repos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .repo-card {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
        }
        
        .repo-card:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .repo-name {
            color: white;
        }
        
        .repo-description {
            color: rgba(255, 255, 255, 0.9);
        }
        
        .repo-meta {
            color: rgba(255, 255, 255, 0.8);
        }
"""

# Template 3: Minimalist
MINIMALIST_CSS = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.8;
            color: #2d3748;
            background: #f7fafc;
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 0;
            box-shadow: none;
            overflow: hidden;
        }
        
        header {
            background: white;
            color: #1a202c;
            padding: 60px 40px;
            text-align: center;
            border-bottom: 1px solid #e2e8f0;
        }
        
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 300;
            letter-spacing: -1px;
        }
        
        header p {
            color: #718096;
            font-size: 1.1em;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-top: 40px;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: 200;
            color: #1a202c;
        }
        
        .stat-label {
            color: #718096;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .content {
            padding: 60px 40px;
        }
        
        .content h2 {
            color: #1a202c;
            margin-bottom: 40px;
            font-weight: 300;
            font-size: 1.8em;
        }
        
        .repos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
        }
        
        .repo-card {
            border: none;
            border-bottom: 2px solid #e2e8f0;
            border-radius: 0;
            padding: 30px 0;
            background: white;
            transition: all 0.2s;
        }
        
        .repo-card:hover {
            transform: none;
            box-shadow: none;
            border-bottom-color: #1a202c;
        }
        
        .repo-name {
            color: #1a202c;
            font-size: 1.3em;
            font-weight: 400;
        }
        
        .repo-description {
            color: #4a5568;
            margin: 15px 0;
        }
        
        .repo-meta {
            color: #a0aec0;
        }
"""

# Template 4: Colorful Gradient
COLORFUL_GRADIENT_CSS = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            padding: 20px;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }
        
        .repos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            padding: 40px;
        }
        
        .repo-card {
            border: 2px solid #e1e4e8;
            border-radius: 15px;
            padding: 25px;
            background: white;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .repo-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .repo-card:hover::before {
            left: 100%;
        }
        
        .repo-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .repo-name {
            color: #0366d6;
            font-weight: 600;
        }
"""

# How to use these templates:
# 1. Open generate_repos_page.py
# 2. Find the <style> section in the generate_html() function
# 3. Replace the CSS with one of these templates
# 4. Run the script again to generate new HTML









