"""Test script to verify all imports work correctly."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing imports...")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path[0]}")
print()

try:
    print("1. Testing streamlit import...")
    import streamlit as st
    print("   [OK] Streamlit imported successfully")
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    sys.exit(1)

try:
    print("2. Testing dotenv import...")
    from dotenv import load_dotenv
    print("   [OK] dotenv imported successfully")
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    sys.exit(1)

try:
    print("3. Testing ContextManager import...")
    from memory.context_manager import ContextManager
    print("   [OK] ContextManager imported successfully")
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Testing ManagerAgent import...")
    from agents.manager_agent import ManagerAgent
    print("   [OK] ManagerAgent imported successfully")
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("[SUCCESS] All imports successful! The app should work.")

