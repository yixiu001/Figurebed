#!/bin/zsh

python generate_index_html.py

git add . && git commit -m '博客图片上传' && git push