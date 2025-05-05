import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

input_dir = 'unzipped_hojin'
output_dir = 'hojinjoho_ndjson'

os.makedirs(output_dir, exist_ok=True)


def escape_control_and_quotes(val):
    """
    Escape raw newlines, carriage returns, tabs, backslashes, and quotes inside any string.
    """
    if not isinstance(val, str):
        return val
    return (
        val
        .replace('\\', '\\\\')
        .replace('\n', '\\n')
        .replace('\r', '\\r')
        .replace('\t', '\\t')
        .replace('"', '\\"')
    )


def recurse_escape(obj):
    """
    Recursively walk dicts & lists, escaping all string leaves.
    """
    if isinstance(obj, dict):
        return {k: recurse_escape(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recurse_escape(v) for v in obj]
    else:
        return escape_control_and_quotes(obj)


def convert_file(input_path, output_path):
    """
    Convert a single JSON file containing an array of objects
    to NDJSON with escaped control characters.
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    with open(output_path, 'w', encoding='utf-8', newline='\n') as outfile:
        for record in data:
            safe = recurse_escape(record)
            line = json.dumps(
                safe,
                ensure_ascii=False,
                separators=(',', ':')
            )
            outfile.write(line + '\n')

    print(f"[✔] Converted {len(data)} records: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")


def main():
    for fname in os.listdir(input_dir):
        if fname.lower().endswith('.json'):
            inp_path = os.path.join(input_dir, fname)
            out_name = os.path.splitext(fname)[0] + '.ndjson'
            out_path = os.path.join(output_dir, out_name)
            try:
                convert_file(inp_path, out_path)
            except Exception as e:
                print(f"[!] Failed to convert {fname}: {e}")


if __name__ == '__main__':
    main()
