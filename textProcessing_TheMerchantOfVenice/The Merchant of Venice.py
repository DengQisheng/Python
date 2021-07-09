############### Directions ###############

##### 文件夹位置说明 #####

## 项目文件夹 Final Project/
## 数据文件夹 Final Project/The Merchant of Venice/
## 主网页文件夹 Final Project/The Merchant of Venice/data/
## 子网页文件夹（不能直接访问） Final Project/The Merchant of Venice/data/merchant/


##### 文件位置说明 #####

## 源文件 Final Project/Final Project_ The Merchant of Venice.py
## 主网页文件 Final Project/The Merchant of Venice/data/Merchant of Venice_ List of Scenes.html
## 子网页文件（不能直接访问） Final Project/The Merchant of Venice/data/merchant/merchant.[act_no].[scene_no].html
## 输出文件 Final Project/The Merchant of Venice.md


##### 使用说明 #####

## 项目文件夹Final Project包含以下文件：
##
##     数据文件夹 The Merchant of Venice
##     源代码 Final Project_ The Merchant of Venice.py
##     Markdown格式输出结果 The Merchant of Venice.md
##     pdf格式输出结果 The Merchant of Venice.pdf
## 
## 在当前目录下打开源代码文件，在shell中运行模块，即可获得标记的统计结果，Markdown格式输出结果文件会在文件夹中生成


############### Functions ###############

##### 解析剧本路径 #####

def get_scene_path():

    '''获得子网页文件的路径'''

    try:
        ## 读入文件数据
        main_file = open(main_path)
        read_file = main_file.readlines()
        
        ## 寻找子网页文件路径位置
        pattern = re.compile('<a.+?\".+?\">')
        ori_content = [pattern.findall(line) for line in read_file if pattern.findall(line)]

        ## 清洗得到子网页文件路径
        content_string = [element for line in ori_content for element in line]
        content_abbr = [re.sub('(<a.+?")|(">)', '', element) for element in content_string]
        content = [re.sub('\./', main_dir, element) for element in content_abbr]

    except:
        main_file = None
        print('获取scene_path失败！退出程序！')
        sys.exit()
        
    finally:
        ## 操作成功后关闭文件
        if main_file:
            main_file.close()

    return content


def get_whole_path():
    
    '''获得所有网页文件的路径'''

    try:
        ## 合并所有网页文件路径
        whole_path = scene_path[::]
        whole_path.append(main_path)
    
    except:
        print('获取whole_path失败！退出程序！')
        sys.exit()

    return whole_path


##### 获得剧本信息 #####

def get_title():
    
    '''获得标题信息'''

    try:
        ## 读入文件数据
        main_file = open(main_path)
        read_file = main_file.readlines()
        
        ## 寻找剧本标题位置
        pattern = re.compile('<tbody>.+')
        content = [pattern.findall(line) for line in read_file if pattern.findall(line)]

        ## 清洗得到剧本标题
        ori_title = re.sub('<.+?>', '', content[0][0])
        title = ''.join(['\n', '# ', ori_title, '\n'])

    except:
        main_file = None
        print('获取title失败！退出程序！')
        sys.exit()
        
    finally:
        ## 操作成功后关闭文件
        if main_file:
            main_file.close()

    return title


def get_scene_address(act_no, scene_no):
    
    '''获得场景地址'''

    try:
        ## 读入文件数据
        main_file = open(main_path)
        read_file = main_file.readlines()
        
        ## 寻找场景信息位置
        pattern = re.compile('Act.+')
        content = [pattern.findall(line) for line in read_file if pattern.findall(line)]

        ## 清洗得到场景地址
        pattern_no = re.compile('%s\.%s' % (act_no, scene_no))
        pattern_add = re.compile('\">.+?<')
        address_list = [pattern_add.findall(info[0]) for info in content if pattern_no.findall(info[0])]
        address = address_list[0][0].lstrip('\">').rstrip('<')
        
    except:
        main_file = None
        print('获取scene_address失败！退出程序！')
        sys.exit()
        
    finally:
        ## 操作成功后关闭文件
        if main_file:
            main_file.close()

    return address


def get_scene_heading(file_path):
    
    '''获得幕号、场号及场景地址'''

    try:
        ## 寻找子网页文件路径的场景信息
        pattern = re.compile('\d+\.')
        info = pattern.findall(file_path)
        
        ## 分离幕号、场号与场景地址
        act_no = info[0].rstrip('.')
        scene_no = info[1].rstrip('.')
        scene_address = get_scene_address(act_no, scene_no)

        ## 清洗得到场景标题
        act = ''.join(['\n## ACT ', act_no, '\n']) if scene_no == '1' else ''
        scene = ''.join(['\n### SCENE ', scene_no, '. ', scene_address, '\n'])
        heading = ''.join([act, scene])

    except:
        print('获取scene_heading失败！退出程序！')
        sys.exit()

    return heading


def get_scene_content(file_path):
    
    '''获得剧本内容'''
    
    try:
        ## 读入文件数据
        sub_file = open(file_path)
        read_file = sub_file.readlines()
    
        ## 寻找子网页文件路径的剧本内容
        pattern = re.compile('<[aA] NAME=speech\d+?><b>.+?</b></[aA]>|<[aA] NAME=\d+?>.+?</[aA]><br>|<i>.+?</i>')
        ori_lines = [pattern.findall(line) for line in read_file if pattern.findall(line)]
        
        ## 创建内容储存列表
        content_list = list()

        ## 创建内容样式
        pattern_character = re.compile('<[aA] NAME=speech\d+?><[bB]>.+?</[bB]></[aA]>')
        pattern_dialogue = re.compile('<[aA] NAME=\d+?>.+?</[aA]><[bB][rR]>')
        pattern_direction = re.compile('<[iI]>.+?</[iI]>')

        ## 创建标志变量
        new_block = 0    ## 新语句标志
        old_block = 0    ## 旧语句标志

        ## 匹配内容样式
        for line in ori_lines:
            
            ## 人物姓名
            if pattern_character.findall(line[0]):
                ori_content_line = re.sub('<[aA] NAME=speech\d+?><[bB]>|</[bB]></[aA]>', '', line[0])
                content_line = ''.join(['**', ori_content_line.strip(), '**\n'])
                new_block = 1
            
            ## 台词文本
            elif pattern_dialogue.findall(line[0]):
                ori_content_line = re.sub('<[aA] NAME=\d+?>|</[aA]><[bB][rR]>', '', line[0])
                content_line = ''.join([ori_content_line.strip(), '  \n'])
                ## 注意此处换行符前添加了两个空格用于输出pdf文件时换行
                new_block = 2
            
            ## 舞台说明
            elif pattern_direction.findall(line[0]):
                ori_content_line = re.sub('<[iI]>|</[iI]>', '', line[0])
                content_line = ''.join(['*', ori_content_line.strip(), '*\n'])
                new_block = 3
            
            ## 语句块结束位置添加空行
            if old_block != new_block:
                content_line = ''.join(['\n', content_line])
            old_block = new_block
            
            ## 储存剧本内容
            content_list.append(content_line)
        
        ## 清洗得到剧本内容
        content = ''.join(content_list)

    except:
        sub_file = None
        print('获取scene_content失败！退出程序！')
        sys.exit()
        
    finally:
        ## 操作成功后关闭文件
        if sub_file:
            sub_file.close()
    
    return content


##### 输出剧本文件 #####

def write_title():
    
    '''输出剧本标题'''

    try:
        ## 读取主标题
        title = get_title()

        ## 打开待写文件
        md_file = open(md_path, 'w')

        ## 写入主标题
        md_file.write(title)

    except:
        md_file = None
        print('写入title失败！退出程序！')
        sys.exit()

    finally:
        ## 操作成功后关闭文件
        if md_file:
            md_file.close()


def write_scene():
    
    '''输出剧本内容'''

    try:
        ## 打开待写文件
        md_file = open(md_path, 'a')

        ## 写入剧本
        for sub_file in scene_path:

            heading = get_scene_heading(sub_file)    ## 读取标题
            md_file.write(heading)    ## 写入标题

            content = get_scene_content(sub_file)    ## 读取内容
            md_file.write(content)    ## 写入内容

    except:
        md_file = None
        print('写入scene失败！退出程序！')
        sys.exit()

    finally:
        ## 操作成功后关闭文件
        if md_file:
            md_file.close()


def write_script():
    
    '''输出剧本'''

    try:
        ## 输出剧本
        write_title()    ## 输出主标题
        write_scene()    ## 输出剧本内容

        ## 输出文件位置
        print("\n结果1 - Markdown格式剧本输出至：\n\n  %s\n" % md_path)    ## 输出Markdown文件

    except:
        print('写入script失败！退出程序！')
        sys.exit()


##### 统计标签数量 #####

def merge_dict(dict1, dict2):
    
    '''合并字典'''

    try:
        ## 利用字典推导式合并键值对
        merge = {key: dict1.get(key, 0) + dict2.get(key, 0) for key in (dict1.keys() | dict2.keys())}

    except:
        print('获取merge_dict失败！退出程序！')
        sys.exit()
        
    return merge


def tally_tags(file_path):
    
    '''统计标记频率'''
    
    try:
        ## 读入文件数据
        sub_file = open(file_path)
        read_file = sub_file.readlines()

        ## 统计出现的标记
        pattern = re.compile('<!?\w+?>|<!?\w+?\s{1}')
        ori_content = [pattern.findall(line) for line in read_file if pattern.findall(line)]
        
        ## 清洗得到的标记
        content_wash = [re.sub('\s', '>', string) for line in ori_content for string in line]
        content = [string.lower() for string in content_wash]

        ## 利用collections.Counter()统计标记频率
        tags_file = dict(Counter(content))
        
    except:
        sub_file = None
        print("文件'%s'打开失败！退出程序！" % file_path)
        sys.exit()

    finally:
        ## 操作成功后关闭文件
        if sub_file:
            sub_file.close()
            
    return tags_file


def sort_tally_tags():
    
    '''排序统计频率'''

    try:
        ## 创建标记频率表
        tags_dict = dict()

        ## 统计标记数量
        for sub_file in whole_path:
            file_stat = tally_tags(sub_file)
            tags_dict = merge_dict(tags_dict, file_stat)

        ## 排序标记频率表
        tags_sorted = sorted(tags_dict.items(), key = lambda item: item[1], reverse = True)

    except:
        print('获取sort_tags失败！退出程序！')
        sys.exit()

    return tags_sorted


##### 输出统计结果 #####

def write_stat():
    
    '''输出统计结果'''

    try:
        ## 统计并排序标记频率
        tags_list = sort_tally_tags()
    
    except:
        print('统计tags失败！退出程序！')
        sys.exit()

    try:
        ## 处理标记数少于三个的情况
        if len(tags_list) < 3:
            raise
        
        ## 输出标记频率的统计结果
        print('结果2 - 出现次数最多的三个标记及其出现次数：\n')
        for pair in tags_list[0:3]:
            print('  标记 %s 出现 %d 次' % (pair[0], pair[1]))
        print()
            
    except:
        print('结果2 - 标记数量少于三个！\n')
        for pair in tags_list:
            print('  标记 %s 出现 %d 次' % (pair[0], pair[1]))
        print()


############### Settings ###############

##### 加载所需的包 #####

import re    ## 用于正则表达式处理
import sys    ## 用于系统操作
from collections import Counter    ## 用于统计标记


##### 设置文件夹路径变量 #####

main_dir = './The Merchant of Venice/data/'    ## 主网页文件所在目录（.表示Final Project文件夹）


##### 设置文件路径变量 #####

## 为了更方便地展示结果，此处已完成了主网页文件路径变量main_path的设定语句（445行）
## 若需要手动输入文件位置，需要将441行取消注释，同时注释掉442行和445行，并在shell界面输入文件位置
## 若手动输入的主网页文件路径不正确，函数get_scene_path()将返回'获取scene_path失败！退出程序！'的错误信息并退出主程序

## 询问主网页文件位置
## main_path = input('请输入主网页文件位置：\n  ')
print('请输入主网页文件位置：\n  ./The Merchant of Venice/data/Merchant of Venice_ List of Scenes.html')    ## 效果展示

## 设定文件路径变量
main_path = './The Merchant of Venice/data/Merchant of Venice_ List of Scenes.html'    ## 主网页文件路径（.表示Final Project文件夹）
md_path = './The Merchant of Venice.md'    ## 输出文件路径（.表示Final Project文件夹）
scene_path = get_scene_path()    ## 解析获得所有子网页文件路径
whole_path = get_whole_path()    ## 解析获得所有网页文件路径


############### Main ###############

##### 输出剧本 #####

write_script()


##### 输出标记统计结果 #####

write_stat()
