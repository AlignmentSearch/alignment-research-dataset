import json

def print_jsonl(filename: str, num_lines: int = 1, text_lim: int = None, encoding: str = 'utf-8'):
    if text_lim is None:
        text_lim = 1e6
    with open(filename, 'r', encoding=encoding) as file:
        for i, line in enumerate(file, 1):
            entry = json.loads(line)
            entry["text"] = entry["text"][:text_lim]
            print(entry)
            if i == num_lines:
                break
        

if __name__ == '__main__':
    print_jsonl('data/alignment_newsletter.jsonl', num_lines=1)