import json
import logging

def save_analysis_to_json(analysis, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=4)
        logging.info(f"Analysis saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving analysis to {output_file}: {e}")
