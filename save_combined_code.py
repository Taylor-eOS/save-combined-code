import os, sys, glob, json

filenames = ['main_script', 'feature_utils', 'embed', 'utils']
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

def save_settings(path, settings):
    with open(path, 'w') as f:
        json.dump(settings, f)

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

def get_candidates(src_dir, all_flag):
    if all_flag:
        return [f for f in glob.glob(os.path.join(src_dir, '*.py')) if os.path.basename(f) != script_name]
    return [os.path.join(src_dir, f if f.endswith('.py') else f + '.py') for f in filenames]

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
    all_flag = '--all' in sys.argv[1:]
    candidates = get_candidates(src_dir, all_flag)
    to_process = [f for f in candidates if os.path.basename(f) != script_name]
    combine_files(to_process, output_file)
    print(f"Combined code written to {output_file}")

if __name__=='__main__':
    main()
