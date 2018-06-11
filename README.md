### 添加功能
新增Windows版本。

#### 工具介绍
绿盟远程安全评估系统漏洞跟踪表导出工具，只支持6.0的RSAS，用于导出各种乱七八糟的数据。

工具涉及：目录获取文件、ZIP文件读取、正则表达式、Excel表格处理、文件读写

GitHub：https://github.com/webingio/RSAS-Export-Tool

这是测试的原始报告：http://p68yfqejc.bkt.clouddn.com/192.168.1.2.zip

实现思路、去掉的功能、代码注释可以到这看（我的博客笔记）：https://webing.io/article/computer-python-rsas-tool.html

#### 测试环境
#### Windows：
```python
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18)
[MSC v.1900 64 bit (AMD64)] on win32
```
#### Linux：
```python
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
[GCC 5.4.0 20160609] on linux
```
注意：不支持Python2

#### 文件结构
```python
├── Coredata          --一个文件夹
│   └── load.py       --数据提取程序
└── vulnerable.py     --漏洞导出程序
```

#### 功能
- [x] 支持导出的数据：IP地址、漏洞名称、风险等级、整改建议、漏洞描述、漏洞CVE编号、漏洞对应端口、漏洞对应协议、漏洞对应服务等，其他数据考虑以后是否添加。
- [x] 支持导出不同端口的同一个漏洞，也就是一个端口对应一个漏洞，保证漏洞的完整性。
- [ ] 不支持多线程，速度还行，看下边的效果图，队列并发只是个鸡肋。

#### 须知
- [x] 当一个漏洞存在两个或者两个以上CVE编号，则只取第一个CVE漏洞编号。
- [x] 当一个漏洞不存在CVE编号时，则替换为 '漏洞暂无CVE编号'。
- [x] 当一个漏洞整改建议为空时（个别低危漏洞），导出留空。

#### 使用说明
#### 安装依赖模块：
```python
pip3 install openpyxl
```
#### 运行程序：
linux:
```python
python3 vulnerable.py /mnt/c/Users/Administrator/Desktop/原始扫描报告
```
#### Windows：
```python
vulnerable.py C:\Users\Administrator\Desktop\原始扫描报告
```
#### 命令说明
主程序 漏洞报告目录路径
如，原始报告存放在 C:\Users\Administrator\Desktop\原始扫描报告 目录下，
就这么执行：
```python
vulnerable.py C:\Users\Administrator\Desktop\原始扫描报告
```
Windows下不能执行，可删掉：encoding='utf-8' 恢复正常，分享的代码已经删除。

#### 漏洞报告目录文件


从RSAS这么导出的原始报告才能用这个工具：
报表输出-勾选主机报表

上边提到的漏洞报告目录，目录下都有哪些文件？

就是你从漏扫直接导出来的报告，通常为zip压缩包，反正不支持其他的，如图：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_zip.png)

压缩包里边都有啥？如图：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_zip_content.png)


### 导出效果
本次测试共导出17个原始扫描报告，如图。
#### Linux：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_linux_test.png)

#### Windows：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_windows_test.png)

#### 导出数据效果图：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_gif.gif)


---
---
---
