# Figurebed
个人图床，存储一些图片，合理利用公共免费资源，坚决抵制薅羊毛

### 一、本地需支持python以及git，请自行研究下载
### 二、使用方式

#### Step1 首先点个Star，然后Fork到自己仓库
`Star!!!Star!!!Star!!!`
#### Step2 克隆代码到本地
`git clone <你的仓库地址>`
#### Step3 修改generate_index_html.py文件，在这里定义GitHub用户名和仓库名称
```python
GITHUB_USERNAME = 'yixiu001' #GitHub用户名
GITHUB_REPOSITORY = 'Figurebed' #仓库名称
```
#### Step4 当前目录下可以自定义一个或多个目录来储存图片
#### Step5 执行start.sh生成index.html文件并上传到github


### 三、访问
可使用`https://<GitHub用户名>.github.io/<仓库名>/index.html`来访问