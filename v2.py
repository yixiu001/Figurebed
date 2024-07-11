import os
import json

# 在这里定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

def generate_index_html(root_dir):
    base_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/"
    json_dir = os.path.join(root_dir, 'json')

    # 创建json目录
    os.makedirs(json_dir, exist_ok=True)

    # 获取所有图片文件，并根据目录分类
    image_files = {}
    for root, _, files in os.walk(root_dir):
        if not root.startswith('./.git'):
            rel_dir = os.path.relpath(root, root_dir)
            for file in files:
                if file.lower().endswith(('.png','.svg','ico','.webp', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    if rel_dir not in image_files:
                        image_files[rel_dir] = []
                    image_files[rel_dir].append(os.path.join(root, file))

    # 生成JSON文件
    json_data = {}
    for category, files in image_files.items():
        json_data[category] = []
        for file in files:
            file_path = os.path.relpath(file, root_dir)
            https_url = base_url + file_path
            cdn_url_complete = cdn_url + file_path
            json_data[category].append({
                "file": file_path,
                "https_url": https_url,
                "cdn_url": cdn_url_complete
            })

    with open(os.path.join(json_dir, 'images.json'), 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    # 定义生成 HTML 内容的函数
    def generate_html_content(image_files):
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>一休github简易图床系统</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                    color: #333;
                }
                .container {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    max-width: 1200px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .category-nav {
                    flex: 0 0 250px;
                    margin-right: 20px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    box-shadow: 0 0 5px rgba(0,0,0,0.1);
                }
                .category-nav h2 {
                    font-size: 1.5rem;
                    margin-bottom: 10px;
                    cursor: pointer;
                }
                .category-list {
                    list-style-type: none;
                    padding: 0;
                }
                .category-list li {
                    margin-bottom: 10px;
                }
                .category-list a {
                    text-decoration: none;
                    color: #333;
                    display: block;
                    padding: 8px 16px;
                    border-radius: 4px;
                    transition: background-color 0.3s ease;
                }
                .category-list a:hover {
                    background-color: #e9ecef;
                }
                .gallery {
                    flex: 1;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: flex-start;
                }
                .gallery-item {
                    position: relative;
                    width: calc(33.33% - 20px);
                    margin-bottom: 20px;
                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                    background-color: #fff;
                    overflow: hidden;
                }
                .gallery-item img {
                    width: 100%;
                    height: auto;
                    display: block;
                    transition: filter 0.3s ease;
                }
                .gallery-item:hover img {
                    filter: blur(4px);
                }
                .link-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(255, 255, 255, 0.8);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    text-align: center;
                }
                .gallery-item:hover .link-overlay {
                    opacity: 1;
                }
                .link-overlay a {
                    margin: 5px;
                    color: #007bff;
                    text-decoration: none;
                }
                .link-overlay a:hover {
                    text-decoration: underline;
                }
                footer {
                    text-align: center;
                    padding: 20px 0;
                    background-color: #333;
                    color: white;
                    margin-top: 20px;
                }
            </style>
            <script>
                function copyToClipboard(text) {
                    navigator.clipboard.writeText(text).then(function() {
                        alert('复制成功: ' + text);
                    }, function(err) {
                        alert('复制失败: ' + err);
                    });
                }
                function toggleCategory(categoryId) {
                    const categoryNav = document.getElementById(categoryId);
                    categoryNav.classList.toggle('open');
                }
            </script>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>一休github简易图床系统</h1>
                </div>
            </header>
            <div class="container">
                <nav class="category-nav">
                    <h2>分类</h2>
                    <ul class="category-list">
        '''

        # 生成导航链接
        for category in image_files:
            html_content += f'<li><a href="javascript:void(0);" onclick="toggleCategory(\'{category}\')">{category}</a></li>'

        html_content += '''
                    </ul>
                    <a href="json/images.json" download>导出所有图片信息</a>
                </nav>
                <div class="gallery">
        '''

        # 生成每个分类的图片展示
        for category, files in image_files.items():
            html_content += f'<div id="{category}" class="gallery"><h2>{category} <a href="json/images_{category}.json" download>导出该分类图片信息</a></h2>'

            category_json_data = []

            for file in files:
                file_path = os.path.relpath(file, root_dir)
                https_url = base_url + file_path
                cdn_url_complete = cdn_url + file_path
                category_json_data.append({
                    "file": file_path,
                    "https_url": https_url,
                    "cdn_url": cdn_url_complete
                })
                html_content += f'''
                <div class="gallery-item">
                    <img src="{https_url}" alt="{os.path.basename(file)}">
                    <div class="link-overlay">
                        <a href="{https_url}" target="_blank" onclick="copyToClipboard('{https_url}'); return false;">HTTPS 访问地址</a>
                        <a href="{cdn_url_complete}" target="_blank" onclick="copyToClipboard('{cdn_url_complete}'); return false;">jsdelivr CDN 加速地址</a>
                    </div>
                </div>
                '''

            # 确保目录存在
            category_json_file_path = os.path.join(json_dir, f'images_{category}.json')
            os.makedirs(os.path.dirname(category_json_file_path), exist_ok=True)
            with open(category_json_file_path, 'w', encoding='utf-8') as category_json_file:
                json.dump(category_json_data, category_json_file, ensure_ascii=False, indent=4)

            html_content += '</div>'

        html_content += '''
                </div>
            </div>
            <footer>
                &copy; 2024 一休github简易图床系统
            </footer>
        </body>
        </html>
        '''
        return html_content

    if image_files:
        html_content = generate_html_content(image_files)
        with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    else:
        print(f"No image files found in {root_dir}")

if __name__ == "__main__":
    generate_index_html('.')
