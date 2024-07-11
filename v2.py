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
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f0f0f0;
                }
                header {
                    background-color: #333;
                    color: white;
                    padding: 10px 0;
                    text-align: center;
                }
                header h1 {
                    margin: 0;
                }
                #category-nav {
                    position: fixed;
                    left: 0;
                    top: 0;
                    width: 200px;
                    height: 100%;
                    background-color: #444;
                    color: white;
                    padding: 20px;
                    box-shadow: 2px 0 5px rgba(0,0,0,0.5);
                    overflow-y: auto;
                    transition: transform 0.3s ease;
                    transform: translateX(-100%);
                }
                #category-nav.open {
                    transform: translateX(0);
                }
                #category-nav a {
                    display: block;
                    color: white;
                    text-decoration: none;
                    margin-bottom: 10px;
                }
                #category-nav a:hover {
                    text-decoration: underline;
                }
                #category-toggle {
                    position: fixed;
                    left: 0;
                    top: 0;
                    background-color: #444;
                    color: white;
                    padding: 10px;
                    cursor: pointer;
                }
                .container {
                    margin-left: 220px;
                    padding: 20px;
                }
                .gallery {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: center;
                }
                .gallery-item {
                    position: relative;
                    width: 200px;
                    height: 200px;
                    text-align: center;
                    overflow: hidden;
                    border: 1px solid #ddd;
                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                    background-color: #fff;
                }
                .gallery-item img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: all 0.3s ease;
                }
                .gallery-item:hover img {
                    filter: blur(4px);
                }
                .gallery-item .link-overlay {
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
                    position: fixed;
                    width: 100%;
                    bottom: 0;
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
                function toggleCategoryNav() {
                    document.getElementById('category-nav').classList.toggle('open');
                }
            </script>
        </head>
        <body>
            <header>
                <h1>一休github简易图床系统</h1>
            </header>
            <div id="category-toggle" onclick="toggleCategoryNav()">分类</div>
            <nav id="category-nav">
        '''

        # 生成导航链接
        for category in image_files:
            html_content += f'<a href="#{category}" onclick="toggleCategoryNav()">{category}</a>'
        html_content += '<a href="json/images.json" download>导出所有图片信息</a>'

        html_content += '''
            </nav>
            <div class="container">
        '''

        # 生成每个分类的图片展示
        for category, files in image_files.items():
            html_content += f'<h2 id="{category}">{category} <a href="json/images_{category}.json" download>导出该分类图片信息</a></h2><div class="gallery">'

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
            <footer>
                &copy; <a href="https://github.com/yixiu001/Figurebed" >2024 a一休github简易图床系统</a>
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
