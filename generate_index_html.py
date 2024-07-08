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

def generate_html(file_structure):
    def generate_directory_html(data, path=''):
        html = ''
        for key in data:
            if isinstance(data[key], dict) and 'https_url' not in data[key]:
                subdir_html = generate_directory_html(data[key], f"{path}/{key}".strip('/'))
                html += f'<div class="folder"><button class="collapsible" data-path="{path}/{key}">{key}</button><div class="content-section">{subdir_html}</div></div>'
            elif isinstance(data[key], dict):
                html += f'<div class="image-entry" data-path="{path}"><img src="{data[key]["https_url"]}" alt="{key}" /><span class="link" onclick="copyToClipboard(\'{data[key]["https_url"]}\')">{data[key]["https_url"]}</span><span class="link" onclick="copyToClipboard(\'{data[key]["cdn_url"]}\')">{data[key]["cdn_url"]}</span></div>'
        return html

    directory_html = generate_directory_html(file_structure)

    html_content = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一休github简易图床系统</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="sidebar">
        <h1>目录</h1>
        <div id="directory">
            {directory_html}
        </div>
    </div>
    <div class="content">
        <h1>图片信息</h1>
        <div id="image-info"></div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const coll = document.getElementsByClassName("collapsible");
            for (let i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    const content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                    showImages(this.getAttribute("data-path"));
                });
            }

            function showImages(directory) {
                const images = document.querySelectorAll('.image-entry');
                images.forEach(image => {
                    if (image.getAttribute('data-path').startsWith(directory)) {
                        image.style.display = 'block';
                    } else {
                        image.style.display = 'none';
                    }
                });
            }

            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('链接已复制: ' + text);
                }, function(err) {
                    console.error('复制失败: ', err);
                });
            }

            showImages(Object.keys({file_structure})[0]); // 默认显示第一个目录的图片
        });
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    root_dir = '.'
    generate_files_json(root_dir)
    file_structure = generate_file_structure(root_dir, root_dir)
    generate_html(file_structure)
