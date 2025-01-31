import json
import logging
from code_reader import read_code_from_directories
from extract_knowledge import extract_knowledge
from json_generator import save_analysis_to_json
from llm_interface import generate_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(directories, output_file, batch_size=5):
    
    code_snippets = read_code_from_directories(directories)

    logging.info(f"Read {len(code_snippets)} code snippets from directories")

    analysis = extract_knowledge(code_snippets, batch_size=batch_size)

    save_analysis_to_json(analysis, output_file)

if __name__ == "__main__":
    directories = ["codebase1"]
    output_file = "data.json"

    main(directories, output_file, batch_size=5)
    
    while True:
        question = input("Ask follow-up question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        try:
            with open('data.json') as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Error reading data.json: {e}")
            continue
        
        prompt = (
            "You have the following code analysis data:\n\n"
            f"{json.dumps(data, indent=4)}\n\n"
            f"Based on this information, please answer the following question:\n"
            f"{question}"
        )

        try:
            response = generate_response(prompt)
            print(f"Follow-up Response: {response}")
        except Exception as e:
            logging.error(f"Error generating follow-up response: {e}")