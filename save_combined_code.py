import os, sys, glob

output_file = os.path.expanduser('~/combined_code.txt')
filenames = ['run', 'utils']
script_name = 'save_combined_code.py'

def remove_imports(lines):
    i = 0
    for line in lines:
        if line.startswith('import') or line.startswith('from'):
            i += 1
        else:
            break
    return lines[i:]

def main():
    all_flag = '--all' in sys.argv[1:]
    src_dir = input("Path to folder containing .py files: ").strip()
    if not os.path.isdir(src_dir):
        print(f"Invalid directory: {src_dir}")
        return
    if all_flag:
        candidates = [f for f in glob.glob(os.path.join(src_dir, '*.py')) if os.path.basename(f) != script_name]
    else:
        candidates = [os.path.join(src_dir, f if f.endswith('.py') else f + '.py') for f in filenames]
    to_process = [f for f in candidates if os.path.basename(f) != script_name]
    with open(output_file, 'w') as outfile:
        for fname in to_process:
            try:
                with open(fname, 'r') as infile:
                    lines = infile.readlines()
                lines = remove_imports(lines)
                content = ''.join(lines).strip('\n')
                outfile.write(f"{os.path.basename(fname)}\n```\n{content}\n```\n\n")
            except FileNotFoundError:
                print(f"Warning: {fname} not found, skipping...")
    print(f"Combined code written to {output_file}")

if __name__=='__main__':
    main()

