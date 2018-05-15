# RSAS-Export-Tool
Python 绿盟远程安全评估系统(RSAS)漏洞跟踪表导出工具


### 2018年5月14日
- [ ] 代码注释、思路在这看：https://webing.io/article/computer-python-rsas-tool.html
- [ ] 这是失败的代码，两千个漏洞导出花时14分，看下边效果图。去掉获取CVE漏洞编号、漏洞描述功能，可以缩短三分之二的时间。
- [ ] 多线程队列啥的，只会单个for，多个for暂时搞不来，有弄了的可以分享我一份。谢谢,邮箱：纸条<webing.io@qq.com>

### 使用方法：
安装模块：pip install openpyxl
```python
python3 vulnerable.py  /mnt/c/Users/Administrator/Desktop/扫描报告
python3 主程序 原始报告目录路径，支持多个报告
```
#### 文件结构：
```python
├── Coredata           文件夹
│   ├── database.mdb   程序运行生成的核心文件
│   └── load.py        数据提取程序
└── vulnerable.py      漏洞导出主程序
```

#### 须知：
- [x] 当一个漏洞存在两个或者两个以上CVE编号，则只取第一个CVE漏洞编号
- [x] 当一个漏洞不存在CVE编号时，则替换为 '该漏洞暂无CVE漏洞编号。'
- [x] 当一个漏洞整改建议为空时（个别低危漏洞），导出留空

### 单个压缩包导出效果图：
![](http://p68yfqejc.bkt.clouddn.com/rsas.png)
### 多个压缩包导出效果图，2507个漏洞，花时10分钟绝望了：
![](http://p68yfqejc.bkt.clouddn.com/rsrs.png)
