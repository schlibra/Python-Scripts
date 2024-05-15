# vilipix_download
Vilipix插画网图片下载脚本，根据搜索关键词一键下载所有图片
## 安装依赖
```shell
pip install -r packages.txt
```
## 修改配置
配置文件为`config.ini`，配置文件将会影响整个程序的运行，下面是配置项：

| 配置项名称 | 说明 | 示例              |
| --- | --- |-----------------|
| keyword | 搜索关键词 | miku            |
| output | 输出路径 | D:\img_download |
| skip_page | 跳过的页数 | 0               |
| user_agent | 模拟浏览器的UA | Mozilla/5.0……   |
## 运行程序
```shell
python vilipix_download.py
```
## 注意事项
该程序暂不支持版本3.12及以上的Python