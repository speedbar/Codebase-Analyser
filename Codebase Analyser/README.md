
# Codebase Analyzer with LLM Integration

## File Structure
- main.py: The entry point of the application. It manages the code reading, knowledge extraction, and JSON output.  It also provides an interactive interface for asking follow-up questions based on the analyzed code.
- llm_interface.py: Handles the interaction with the LLM using the Gemini API to generate responses based on code snippets and follow-up questions.
- json_generator.py: Saves the extracted knowledge into a JSON file.
- extract_knowledge.py: Processes the code snippets in batches, sends them to the LLM, and extracts structured knowledge about the code.
- code_reader.py: Recursively reads code files from specified directories while excluding certain directories (e.g., node_modules, .git).
- config.json: Contains api key.

## Approach
This project reads code from a list of specified directories, analyzes it using the Gemini LLM to extract detailed information, and generates a structured JSON output.


## Best Practices Considered
- Ensured code snippets are read correctly and are not empty.
- Used prompts to accurately request specific details from the LLM.
- Handled large codebases by processing snippets in manageable chunks.
- The code will be able to handle multiple directories.

## Instructions
1. Place the code you want to analyze in directories.
2. Run pip install -r requirements.tx
2. Modify directories names in main.py as per the actual names of directories. Currently given name is "codebase1".
3. Set up your Gemini API key in the config.json file
4. Run the application:python main.py
5. The analysis will be saved in data.json.
6. Ask follow-up questions.
    