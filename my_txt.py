import json


def extract_text_blocks(full_path):
    with open(full_path, 'r') as f:
        json_data = json.load(f)

    text_blocks = []
    for page in json_data["pages"]:
        for block in page["blocks"]:
            text = ""
            for line in block["lines"]:
                for word in line["words"]:
                    text += word["value"] + " "
            text_blocks.append(text.strip())
    return text_blocks