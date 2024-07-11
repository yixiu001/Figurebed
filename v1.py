import os

# 在这里定义GitHub用户名和仓库名称
GITHUB_USERNAME = 'yixiu001'
GITHUB_REPOSITORY = 'Figurebed'

def generate_index_html(root_dir):
    base_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/raw/main/"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}@main/"

    # 定义生成 HTML 内容的函数
    def generate_html_content(files):
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
                .container {
                    margin: 20px auto;
                    padding: 20px;
                    max-width: 1000px;
                    background-color: white;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .gallery {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: center;
                }
                .gallery-item {
                    flex: 1 1 200px;
                    max-width: 200px;
                    text-align: center;
                }
                .gallery-item img {
                    max-width: 100%;
                    height: auto;
                }
                .gallery-item a {
                    display: block;
                    margin-top: 10px;
                    color: #007bff;
                    text-decoration: none;
                    word-wrap: break-word;
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
        </head>
        <body>
            <header>
                <h1>一休github简易图床系统</h1>
            </header>
            <div class="container">
                <div class="gallery">
        '''

        for file in files:
            file_path = os.path.relpath(file, root_dir)
            https_url = base_url + file_path
            cdn_url_complete = cdn_url + file_path
            html_content += f'''
            <div class="gallery-item">
                <img src="{https_url}" alt="{os.path.basename(file)}">
                <a href="{https_url}" target="_blank">HTTPS 访问地址</a>
                <a href="{cdn_url_complete}" target="_blank">jsdelivr CDN 加速地址</a>
            </div>
            '''

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

    # 获取所有图片文件
    image_files = [os.path.join(root, file) for root, _, files in os.walk(root_dir) for file in files if file.lower().endswith(('.png','.svg','ico','.webp', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

    if image_files:
        html_content = generate_html_content(image_files)
        with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    else:
        print(f"No image files found in {root_dir}")

if __name__ == "__main__":
    generate_index_html('.')
