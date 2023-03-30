import jsonlines

data = []

with jsonlines.open('dataensi.jsonl') as f:
    for line in f.iter():
        try:
            data.append(line)
        except json.decoder.JSONDecodeError:
            continue

print(data)
