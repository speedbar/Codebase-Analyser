from llm_interface import generate_response
import logging
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_knowledge(code_snippets, batch_size=5):

    knowledge_list = []
    total_snippets = len(code_snippets)
    batches = math.ceil(total_snippets / batch_size)

    logging.info(f"Total code snippets: {total_snippets}. Processing in {batches} batches.")

    for batch_num in range(batches):
        batch_snippets = code_snippets[batch_num * batch_size:(batch_num + 1) * batch_size]
        
        for snippet in batch_snippets:
            file_path = snippet["file"]
            code = snippet["code"]

            prompt = (
                f"File: {file_path}\n"
                f"Code:\n{code}\n\n"
                "Please provide the following details in a structured format:\n"
                "- 1. High-level description of what the code aims to achieve\n"
                "- 2. Method names, signatures, and descriptions\n"
                "- 3. Code complexity and ways to improve\n"
                "- 4. Errors or problems in the code\n"
                "Provide me the response in the same numbered format given above\n"
            )

            try:
                response = generate_response(prompt)
                knowledge_list.append({
                    "Batch": batch_num + 1,
                    "File": file_path,
                    "High level Description": response.split("**1. ")[1].split("**2. ")[0].strip(),
                    "Method Names, Signatures, and Descriptions": response.split("**2. ")[1].split("**3. ")[0].strip(),
                    "Code Complexity and Ways to Improve:": response.split("**3. ")[1].split("**4. ")[0].strip(),
                    "Errors or Problems": response.split("**4. ")[1].strip()
                })

                logging.info(f"Processed file: {file_path} in batch {batch_num + 1}")

            except Exception as e:
                logging.error(f"Error processing file {file_path} in batch {batch_num + 1}: {e}")

    return knowledge_list
