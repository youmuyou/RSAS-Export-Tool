### 说明
- [ ] 去掉获取主机名和操作系统
- [ ] 去掉获取漏洞描述功能
- [x] 不弄了

### 功能
支持导出数据：
IP地址、漏洞名称、风险分类、风险等级、整改建议、漏洞CVE编号、漏洞对应端口、漏洞对应协议、漏洞对应服务

实现思路、去掉的功能、代码注释可以到这看：https://webing.io/article/computer-python-rsas-tool.html

无多线程，有大佬加上的恳请分享我一份，谢谢！邮箱：纸条 webing.io@qq.com


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

### 使用说明
```python
python3   vulnerable.py   /mnt/c/Users/Administrator/Desktop/扫描报告
python3   主程序              原始报告存放目录
```
运行环境Python3以上，原始报告目录如：把原始报告放在 C:\扫描报告 目录下就这么执行：python3 vulnerable.py C:\扫描报告

扫描报告目录下可以放任意多个扫描报告
如：
![](http://p68yfqejc.bkt.clouddn.com/sapmoap.png)

导出如图,上边为单个，下边为多个：
![](http://p4nyd2zat.bkt.clouddn.com/xiaoguotu.png)
