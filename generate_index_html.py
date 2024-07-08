import os
import json

# 在这里定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

TEMPLATE_DIR = '.theme'

def read_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_index_html(root_dir):
    base_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/"

    html_template = read_template(os.path.join(TEMPLATE_DIR, 'template.html.temp'))
    js_template = read_template(os.path.join(TEMPLATE_DIR, 'script.js.temp'))

    file_structure = {}

    def generate_file_structure(directory):
        structure = {}
        for entry in sorted(os.listdir(directory)):
            if entry.startswith('.'):
                continue
            path = os.path.join(directory, entry)
            rel_path = os.path.relpath(path, root_dir).replace("\\", "/")
            if os.path.isdir(path):
                structure[entry] = generate_file_structure(path)
            elif entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                https_url = base_url + rel_path
                cdn_url_complete = cdn_url + rel_path
                structure[entry] = {
                    'https_url': https_url,
                    'cdn_url': cdn_url_complete
                }
        return structure

    file_structure = generate_file_structure(root_dir)

    with open(os.path.join(root_dir, 'files.json'), 'w', encoding='utf-8') as f:
        json.dump(file_structure, f, ensure_ascii=False, indent=2)

    html_content = html_template
    html_content = html_content.replace('<!-- GITHUB_USERNAME -->', GITHUB_USERNAME)
    html_content = html_content.replace('<!-- GITHUB_REPOSITORY -->', GITHUB_REPOSITORY)

    with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open(os.path.join(root_dir, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(js_template)

if __name__ == "__main__":
    generate_index_html('.')
