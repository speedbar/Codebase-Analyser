import os
import logging

def read_code_from_directories(directories):
   
    code_snippets = []
    excluded_dirs = {'node_modules', '.git', '__pycache__'} 
    
    for directory in directories:
        if not os.path.isdir(directory):
            logging.warning(f"Directory {directory} does not exist.")
            continue
        
        for root, dirs, files in os.walk(directory):
         
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file.endswith(('.py', '.java', '.js', '.html', '.css', '.scss', '.ts', '.tsx')):  # Add other extensions if needed
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        code_snippets.append({
                            "file": file_path,
                            "code": code
                        })
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {e}")

    return code_snippets
