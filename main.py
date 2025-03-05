import os
import tarfile
import tempfile
from re import VERBOSE
from typing import Optional

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.gemini import Gemini
from llama_index.llms.groq import Groq  # Using Groq for Llama 3.3 access
from pkginfo import UnpackedSDist

from pkg_inspector import PackageInspector
from prompts import SYSTEM_PROMPT

initial_prompt = """ 
You are an expert security analyst tasked with determining if a Python package is malware. You have the following tools at your disposal:
- **INSPECT_METADATA**: RETRIEVES METADATA LIKE NAME, AUTHOR, EMAIL, URL, AND DESCRIPTION.
- **INSPECT_SETUP_PY**: RETRIEVES THE CONTENT OF SETUP.PY, WHICH MAY CONTAIN INSTALLATION SCRIPTS.
- **INSPECT_INIT_PY**: RETRIEVES THE CONTENT OF __INIT__.PY, THE PACKAGE'S INITIALIZATION CODE.
- **INSPECT_PROJECT_STRUCTURE**: RETRIEVES THE PACKAGE'S DIRECTORY AND FILE STRUCTURE.

YOUR TASK IS TO SYSTEMATICALLY ANALYZE THE PACKAGE BY USING THESE TOOLS TO GATHER EVIDENCE. LOOK FOR SPECIFIC SIGNS OF MALWARE, INCLUDING BUT NOT LIMITED TO:

- **SUSPICIOUS METADATA**: UNUSUAL AUTHOR EMAILS (E.G., RANDOM STRINGS), MALICIOUS URLS (E.G., KNOWN BAD DOMAINS), OR DECEPTIVE DESCRIPTIONS.
- **MALICIOUS SETUP.PY**: CODE EXECUTING SYSTEM COMMANDS (E.G., OS.SYSTEM, SUBPROCESS), DOWNLOADING EXTERNAL SCRIPTS, OR INSTALLING UNEXPECTED DEPENDENCIES.
- **MALICIOUS __INIT__.PY**: OBFUSCATED CODE (E.G., BASE64 ENCODED), NETWORK REQUESTS, OR UNAUTHORIZED FILE OPERATIONS.
- **UNUSUAL STRUCTURE**: HIDDEN FILES (E.G., DOTFILES LIKE .MALWARE.PY), UNEXPECTED EXECUTABLES, OR ATYPICAL DIRECTORY LAYOUTS.

PROCEED STEP-BY-STEP:
1. USE THE TOOLS TO COLLECT INFORMATION.
2. ANALYZE THE OUTPUT FOR RED FLAGS.
3. DECIDE IF FURTHER INSPECTION IS NEEDED OR IF YOU CAN CONCLUDE.

WHEN YOU HAVE SUFFICIENT EVIDENCE, PROVIDE YOUR FINAL ANSWER IN THIS FORMAT: 'FINAL ANSWER: MALWARE' OR 'FINAL ANSWER: NOT MALWARE'. IF UNCERTAIN, EXPLAIN WHY AND CONCLUDE WITH 'FINAL ANSWER: NOT MALWARE' UNLESS CLEAR EVIDENCE EXISTS.

Begin by inspecting the metadata. """


def detect_malware(pkg_folder: str) -> str:
    """
    Detects if a Python package tarfile is malware using a ReActAgent.
    
    Args:
        tarfile_path (str): Path to the package tarfile.
    
    Returns:
        str: 'malware', 'not malware', or an error message.
    """
    # Ensure tarfile exists
    # Initialize inspector with extracted package path
    inspector = PackageInspector(pkg_folder)

    # Define tools
    tools = [
        FunctionTool.from_defaults(
            fn=inspector.inspect_metadata,
            name="inspect_metadata",
            description="Extracts and returns the package metadata (e.g., name, author, URL)."
        ),
        FunctionTool.from_defaults(
            fn=inspector.inspect_setup_py,
            name="inspect_setup_py",
            description="Returns the content of setup.py if present."
        ),
        FunctionTool.from_defaults(
            fn=inspector.inspect_init_py,
            name="inspect_init_py",
            description="Returns the content of __init__.py from the package directory."
        ),
        FunctionTool.from_defaults(
            fn=inspector.inspect_project_structure,
            name="inspect_project_structure",
            description="Returns the directory structure of the package."
        ),
    ]

    llm = Gemini(
        model="models/gemini-1.5-flash",
        api_key=os.environ["GOOGLE_API_KEY"],  # uses GOOGLE_API_KEY env var by default
    )


    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=10, # Prevent infinite loops,
        VERBOSE=True,
    )

    # Run the agent
    try:
        response = agent.chat(SYSTEM_PROMPT)
        response_str = str(response)  # Convert response to string
    except Exception as e:
        return f"Error during agent execution: {str(e)}"

    # Parse the final answer
    if "Final Answer:" in response_str:
        answer = response_str.split("Final Answer:")[1].strip()
        if answer in ["malware", "not malware"]:
            return answer
        return f"Invalid final answer received: {answer}"
    return "Could not determine if the package is malware; no clear final answer provided."
def main():

    top_level_folder = "<your pkg>"
    result = detect_malware(top_level_folder)
    print(f"Analysis result: {result}")

if __name__ == "__main__":
    main()

