import os, sys, glob, json

filenames = ['main_script', 'feature_utils', 'utils', 'model', 'gui_core', 'embed']
script_name = 'save_combined_code.py'

def remove_imports(lines):
    i = 0
    for line in lines:
        if line.startswith('import') or line.startswith('from'):
            i += 1
        else:
            break
    return lines[i:]

def load_settings(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {}

def save_settings(path, new_settings):
    settings = load_settings(path)
    settings.update(new_settings)
    with open(path, 'w') as f:
        json.dump(settings, f, indent=2)

def get_src_dir(settings_file):
    settings = load_settings(settings_file)
    last_path = settings.get('last_src_dir', '')
    prompt = f"Path to folder containing .py files [{last_path}]: " if last_path else "Path to folder containing .py files: "
    src_dir = input(prompt).strip() or last_path
    if not os.path.isdir(src_dir):
        print(f"Invalid directory: {src_dir}")
        return None, settings
    settings['last_src_dir'] = src_dir
    save_settings(settings_file, settings)
    return src_dir, settings

def get_candidates(src_dir):
    return [f for f in glob.glob(os.path.join(src_dir, '*.py')) if os.path.basename(f) != script_name]

def prompt_selection(candidates):
    for i, f in enumerate(candidates, 1):
        print(f"{i}. {os.path.basename(f)}")
    choices = input("Files to include (comma separated): ").split(',')
    selected = []
    for c in choices:
        c = c.strip()
        if c.isdigit() and 1 <= int(c) <= len(candidates):
            selected.append(candidates[int(c) - 1])
        else:
            name = c if c.endswith('.py') else c + '.py'
            for f in candidates:
                if os.path.basename(f) == name:
                    selected.append(f)
                    break
    return selected

def combine_files(file_list, output_path):
    with open(output_path, 'w') as outfile:
        for fname in file_list:
            try:
                with open(fname, 'r') as infile:
                    lines = infile.readlines()
                lines = remove_imports(lines)
                content = ''.join(lines).strip('\n')
                outfile.write(f"{os.path.basename(fname)}\n```\n{content}\n```\n\n")
            except FileNotFoundError:
                print(f"Warning: {fname} not found, skipping...")

def main():
    settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
    src_dir, _ = get_src_dir(settings_file)
    if not src_dir: return
    output_file = os.path.join(src_dir, 'combined_code.txt')
    candidates = get_candidates(src_dir)
    to_process = prompt_selection(candidates) if len(sys.argv) > 1 and sys.argv[1] == '-c' else candidates
    combine_files(to_process, output_file)
    print(f"Combined code written to {output_file}")

if __name__=='__main__':
    main()

