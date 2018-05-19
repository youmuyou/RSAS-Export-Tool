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
- [x] 当一个漏洞不存在CVE编号时，则替换为 '漏洞暂无CVE编号。'。
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
上边提到的漏洞报告目录，目录下都有哪些文件？
就是你从漏扫直接导出来的报告，通常为zip压缩包，反正不支持其他的，如图：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_zip.png)

### 导出效果
本次测试共导出17个原始扫描报告，如图。
#### Linux：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_linux_test.png)

#### Windows：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_windows_test.png)

#### 导出数据效果图：
![](http://p4nyd2zat.bkt.clouddn.com/rsas_gif.gif)


### 代码
#### load.py
```python
import os
import re
import sys
import html
import shutil
import zipfile
import time

class File_re(object):
    def __init__(self):
        super(File_re, self).__init__()
        self.file_re = '.*?.zip'
        self.uzip_re = '.*?.html'
        self.title_re = '<th width="120">任务名称</th>.*?<td>(.*?)</td>'
        self.vul_list_re = '(<table id="vuln_list" class="report_table">.*?</table>)'
        self.vul_detail_re = '(<div id="vul_detail">.*?</div>)'
        self.vul_details_re = '(<tr class="solution.*?">.*?<td>.*?<table class="report_table plumb".*?>.*?</table>.*?</td>.*?</tr>)'
        self.host_re = '(<td valign="top" style="width:50%;">.*?<table class="report_table plumb">.*?<tbody>.*?<th width="120">IP地址</th>.*?</tbody>.*?</table></td>)'


def load_date():
    folder_name = str(sys.argv[1])
    dirList = os.listdir(folder_name)
    for name in dirList:
        all_file_name = re.findall(File_re().file_re,name)
        for file_name in all_file_name:
            uzip = zipfile.ZipFile(folder_name+'/'+file_name)
            for uzip_content in uzip.namelist():
                all_uzip_content = re.findall(File_re().uzip_re,uzip_content)
                for all_uzip in all_uzip_content:
                    htmlcont = uzip.open(all_uzip).read().decode('utf8')

                    title = re.findall(File_re().title_re,htmlcont,re.S|re.M)
                    for title_content in title:
                        with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                            content.write('<python>title<python>')
                            content.write(html.unescape(title_content))
                            content.write('<python>title</python>\n')

                        with open('./Coredata/database.mdb','a') as content:
                            content.write('./Coredata/temp/'+html.unescape(title_content)+'.mdb\n')


                    host = re.findall(File_re().host_re,htmlcont,re.S|re.M)
                    for host_content in host:
                        with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                            content.write('<python>host<python>\n')
                            content.write(html.unescape(host_content))
                            content.write('\n<python>host</python>\n')

                    vul_list = re.findall(File_re().vul_list_re,htmlcont,re.S|re.M)
                    for list_content in vul_list:
                        with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                            content.write('<python>vul_list<python>\n')
                            content.write(html.unescape(list_content))
                            content.write('\n<python>vul_list</python>\n')

                    vul_detail = re.findall(File_re().vul_detail_re,htmlcont,re.S|re.M)
                    for detail_content in vul_detail:
                        with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                            content.write('<python>vul_detail<python>\n')

                        vul_details = re.findall(File_re().vul_details_re,detail_content,re.S|re.M)
                        for list_details in vul_details:
                            with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                                content.write('<python>vul_details<python>\n')
                                content.write(html.unescape(list_details))
                                content.write('\n<python>vul_details</python>\n')


                        with open('./Coredata/temp/%s.mdb'%title_content, 'a') as content:
                            content.write('\n<python>vul_detail</python>\n')

            print('提取 %s'%file_name+' 完成！')


def start_date():
    try:
        shutil.rmtree('./Coredata/temp')
        time.sleep(0.1)
        os.mkdir('./Coredata/temp')
    except Exception as e:
        os.mkdir('./Coredata/temp')
    with open('./Coredata/database.mdb', 'w') as content:
        content.write('')


def end_date():
    shutil.rmtree('./Coredata/temp')
    os.remove('./Coredata/database.mdb')
```

#### vulnerable.py

```python
import os
import re
import sys
import html
import time
import zipfile
import datetime
import openpyxl
import Coredata.load


class Vul_re(object):
    def __init__(self):
        super(Vul_re, self).__init__()
        self.vul_list_re = '<python>host<python>.*?<td valign="top".*?<th width="120">IP地址</th>.*?<td>(.*?)</td>.*?</td>.*?<python>host</python>.*?<python>vul_list<python>(.*?)<python>vul_list</python>'
        self.vul_detail_re = '<python>vul_detail<python>(.*?)<python>vul_detail</python>'
        self.vul_details_re = '<python>vul_details<python>(.*?)<python>vul_details</python>'

        self.danger_re = '<span class="level_danger_(.*?)".*?(table_\d_\d+).*?>(.*?)</span>'
        self.title_re = '<python>title<python>(.*?)<python>title</python>'
        self.other_re = '<td class="vul_port">(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>.*?<ul>(.*?)</ul>'

class Vul_content(object):
    def __init__(self,vul_re):
        super(Vul_content, self).__init__()
        self.vul_list_content = re.findall(vul_re.vul_list_re,htmlcont,re.S|re.M)
        self.vul_detail_content = re.findall(vul_re.vul_detail_re,htmlcont,re.S|re.M)


class Solve_re(object):
    def __init__(self, danger):
        super(Solve_re, self).__init__()
        self.solve_re = '<tr class="solution.*?%s.*?<th width="100">解决办法</th>.*?<td>(.*?)</td>' % danger
        self.describe_re = '<tr class="solution.*?%s.*?<th width="100">详细描述</th>.*?<td>(.*?)</td>' % danger
        self.cve_re = '<tr class="solution.*?%s.*?<th width="100">CVE编号</th>.*?<td><a target=.*?>(.*?)</a>.*?</td>' % danger

class Other(object):
    def __init__(self, vul_re, all_vuln_list):
        super(Other, self).__init__()
        self.all_other = re.findall(vul_re.other_re,all_vuln_list,re.S|re.M)

class Danger(object):
    def __init__(self, vul_re, other):
        super(Danger, self).__init__()
        self.danger_coneent = re.findall(vul_re.danger_re,other,re.S|re.M)

class Solve(object):
    def __init__(self, solve, all_vul_detail):
        super(Solve, self).__init__()
        self.solve_plumb = re.findall(solve.solve_re,all_vul_detail,re.S|re.M)
        self.describe_plumb = re.findall(solve.describe_re,all_vul_detail,re.S|re.M)
        self.cve_plumb = re.findall(solve.cve_re,all_vul_detail,re.S|re.M)

def main():
    folder_name = str(sys.argv[1])
    print('\n数据提取完成，正在生成漏洞跟踪表...')
    wb = openpyxl.Workbook()
    ws = wb.active

    vul_re = Vul_re()

    with open('./Coredata/database.mdb') as content:
        for zip_content in content:
            zip_cont = zip_content.strip('\n\r')
            content = open(zip_cont,'r')
            global htmlcont
            htmlcont = content.read()
            content.close()
            sheet_name =  re.findall(vul_re.title_re,htmlcont,re.S|re.M)
            print('正在导出 %s'%sheet_name[0])
            ws = wb.create_sheet(sheet_name[0],0)
            ws['A1'] = '序号'
            ws['B1'] = '主机名'
            ws['C1'] = 'IP地址'
            ws['D1'] = '漏洞名称'
            ws['E1'] = '风险分类'
            ws['F1'] = '风险等级'
            ws['G1'] = '整改建议'
            ws['H1'] = '漏洞描述'
            ws['I1'] = '漏洞CVE编号'
            ws['J1'] = '漏洞对应端口'
            ws['K1'] = '漏洞对应协议'
            ws['L1'] = '漏洞对应服务'

            vul_content = Vul_content(vul_re)
            x = 0

            for all_vul_detail in vul_content.vul_detail_content:
                vul_details_content = re.findall(vul_re.vul_details_re,all_vul_detail,re.S|re.M)

            for all_vul_list in vul_content.vul_list_content:
                for other in Other(vul_re,all_vul_list[1]).all_other:
                    for danger in Danger(vul_re,other[3]).danger_coneent:
                        x += 1
                        for all_vul_details in vul_details_content:
                            vul_detail = Solve(Solve_re(danger[1]),all_vul_details)
                            for solve,describe in zip(vul_detail.solve_plumb,vul_detail.describe_plumb):
                                cve = vul_detail.cve_plumb
                                if cve:
                                    pass
                                else:
                                    cve = ['漏洞暂无CVE编号。']
                        ws.append([x,'',all_vul_list[0],danger[2],'漏洞',danger[0].replace('low','低').replace('middle','中').replace('high','高'),html.unescape(re.sub('<br/>','',solve)).replace(' ','').strip('\n'),html.unescape(re.sub('<br/>','',describe)).replace(' ','').strip('\n'),cve[0],other[0],other[1],other[2]])
    wb.save(folder_name+'/漏洞跟踪表.xlsx')
    print('\n漏洞跟踪表导出完成，保存在 %s 目录下。'%folder_name)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    Coredata.load.start_date()
    Coredata.load.load_date()
    main()
    Coredata.load.end_date()
    endtime = datetime.datetime.now()
    print ('导出花时：%s秒...'%(endtime - starttime).seconds)
```


---
---
---
