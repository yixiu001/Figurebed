import os
import json

# 定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

def generate_file_structure(directory, root_dir):
    structure = {}
    for entry in sorted(os.listdir(directory)):
        if entry.startswith('.'):
            continue
        path = os.path.join(directory, entry)
        rel_path = os.path.relpath(path, root_dir).replace("\\", "/")
        if os.path.isdir(path):
            structure[entry] = generate_file_structure(path, root_dir)
        elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            https_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/{rel_path}"
            cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/{rel_path}"
            structure[entry] = {
                'https_url': https_url,
                'cdn_url': cdn_url
            }
    return structure

def generate_files_json(root_dir):
    file_structure = generate_file_structure(root_dir, root_dir)
    with open(os.path.join(root_dir, 'files.json'), 'w', encoding='utf-8') as f:
        json.dump(file_structure, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_files_json('.')
