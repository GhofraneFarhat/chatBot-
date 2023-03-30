import jsonlines

with open('dataensi_prepared (2).jsonl', 'r', encoding='utf-8') as f:
    reader = jsonlines.Reader(f)
    for obj in reader:
        print(obj)
