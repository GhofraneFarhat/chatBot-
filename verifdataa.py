import os

filename = "data.jsonl"

if not os.path.exists(filename):
    with open(data, 'w') as f:
        f.write('')
