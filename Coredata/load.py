import os
import sys
import re
import zipfile
import html
import time

class File_re(object):
    def __init__(self):
        super(File_re, self).__init__()
        self.file_re = '.*?.zip'
        self.uzip_re = '.*?.html'
        self.title_re = '<th width="120">任务名称</th>.*?<td>(.*?)</td>'
        #正则，用于获取2.1 漏洞概况所有内容
        self.vul_list_re = '(<table id="vuln_list" class="report_table">.*?</table>)'
        #正则，用于获取2.2 漏洞详情所有内容
        self.vul_detail_re = '(<div id="vul_detail">.*?</div>)'
        #正则，用于获取2.2 漏洞详情所有内容,并分开内容
        self.vul_details_re = '(<tr class="solution.*?">.*?<td>.*?<table class="report_table plumb".*?>.*?</table>.*?</td>.*?</tr>)'
        #正则，用于获取IP地址、主机名、操作系统
        self.host_re = '(<td valign="top" style="width:50%;">.*?<table class="report_table plumb">.*?<tbody>.*?<th width="120">IP地址</th>.*?</tbody>.*?</table></td>)'


def load_date():
    clean_date()
    #获取实参目录
    folder_name = str(sys.argv[1])
    #获取目录下的所有文件
    dirList = os.listdir(folder_name)
    for name in dirList:
        #查找zip压缩包(.*?.zip)
        all_file_name = re.findall(File_re().file_re,name)
        for file_name in all_file_name:
            #打开压缩包文件
            uzip = zipfile.ZipFile(folder_name+'/'+file_name)
            #迭代所有文件名
            for uzip_content in uzip.namelist():
                #只获取正则内的文件名（.*?.html）
                all_uzip_content = re.findall(File_re().uzip_re,uzip_content)
                for all_uzip in all_uzip_content:
                    #打开这些文件，按照以下正则分别获取内容，写入文件（辅助作用）
                    htmlcont = uzip.open(all_uzip).read().decode('utf8')

                    title = re.findall(File_re().title_re,htmlcont,re.S|re.M)
                    for title_content in title:
                        with open('./Coredata/database.mdb', 'a') as content:
                            content.write('<python>python<python>\n')
                            content.write('<python>title<python>')
                            content.write(html.unescape(title_content))
                            content.write('<python>title</python>\n')

                    host = re.findall(File_re().host_re,htmlcont,re.S|re.M)
                    for host_content in host:
                        with open('./Coredata/database.mdb', 'a') as content:
                            content.write('<python>host<python>\n')
                            content.write(html.unescape(host_content))
                            content.write('\n<python>host</python>\n')

                    vul_list = re.findall(File_re().vul_list_re,htmlcont,re.S|re.M)
                    for list_content in vul_list:
                        with open('./Coredata/database.mdb', 'a') as content:
                            content.write('<python>vul_list<python>\n')
                            content.write(html.unescape(list_content))
                            content.write('\n<python>vul_list</python>\n')

                    vul_detail = re.findall(File_re().vul_detail_re,htmlcont,re.S|re.M)
                    for detail_content in vul_detail:
                        with open('./Coredata/database.mdb', 'a') as content:
                            content.write('<python>vul_detail<python>\n')

                        vul_details = re.findall(File_re().vul_details_re,detail_content,re.S|re.M)
                        for list_details in vul_details:
                            with open('./Coredata/database.mdb', 'a') as content:
                                content.write('<python>vul_details<python>\n')
                                content.write(html.unescape(list_details))
                                content.write('\n<python>vul_details</python>\n')


                        with open('./Coredata/database.mdb', 'a') as content:
                            content.write('\n<python>vul_detail</python>\n')

            with open('./Coredata/database.mdb', 'a') as content:
                content.write('<python>python</python>\n')

            print('提取 %s'%file_name+' 完成！')


def clean_date():
    with open('./Coredata/database.mdb', 'w') as content:
        #清空文件里的数据
        content.write('')
        print('\n删除缓存成功！')
