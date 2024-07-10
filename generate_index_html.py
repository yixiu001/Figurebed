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
                    margin: 20px;
                    background-color: #f0f0f0;
                }
                h1 {
                    text-align: center;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                    text-align: left;
                }
                img {
                    max-width: 100px;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <h1>一休github简易图床系统</h1>
            <table>
                <tr>
                    <th>缩略图</th>
                    <th>HTTPS 访问地址</th>
                    <th>jsdelivr CDN 加速地址</th>
                </tr>
        '''

        for file in files:
            file_path = os.path.relpath(file, root_dir)
            https_url = base_url + file_path
            cdn_url_complete = cdn_url + file_path
            html_content += f'''
            <tr>
                <td><img src="{https_url}" alt="{os.path.basename(file)}"></td>
                <td><a href="{https_url}" target="_blank">{https_url}</a></td>
                <td><a href="{cdn_url_complete}" target="_blank">{cdn_url_complete}</a></td>
            </tr>
            '''

        html_content += '''
            </table>
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
