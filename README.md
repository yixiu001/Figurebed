# Figurebed
个人图床，存储一些图片

## Staticaly CDN加速
直接访问Github仓库的资源是非常慢的！因此我们要用一些免费的CDN进行加速，Staticaly CDN是目前免费CDN中比较好用的啦，他的应用规则如下：
```shell
# 格式 其中 user是用户名  repo是仓库名  version代表版本(tag或者分支 默认为main)  flie是文件路径
https://cdn.staticaly.com/gh/user/repo@version/file

# 比如我的示例仓库就是加速地址就是这个大家可以参考参考
https://cdn.staticaly.com/gh/fomalhaut1998/pic_bed@main/img/p2.webp
```
