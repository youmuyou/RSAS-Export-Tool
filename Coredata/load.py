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
                                content.write(html.unescape(list_details).replace('\xa0', ' '))
#                                 content.write(html.unescape(list_details))
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
