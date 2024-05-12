import os
import get_time
import shutil

#dir存储系统储存的信息,log储存日收入支出,goods储存货物信息
#bak储存备份文件
#定义储存文件以oc结尾,以自定义格式储存
#备份文件为bak结尾

class file():

    #刷新文件内部数据
    def flush_file(file_path):
        """
        调用后将文件按照索引号重新排序
        file_path:文件路径
        """
        pass
    
    #读取日收入支出文件函数
    def read_data(date,mode):
        """
        date:日期数据,2024年4月26日需写为:2024426
        mode:读取文件方法,1:返回销售额,2:返回文档全部数据(尾随格式化后的时间)
        """
        #确定需要读取的文件存在
        if(os.path.exists(f"dir/log/{date}.oc")):
            f=open(f"dir/log/{date}.oc","r",encoding="UTF-8")
            if mode == 1:
                all=0
                i=0
                o=0
                for line in f:
                    read_line=line.split(",")
                    i=read_line[0]
                    o=read_line[1]
                    i=float(i)
                    o=float(o)
                    all += i-o
                return(all)

            elif mode == 2:
                for line in f:
                    
                    read_line=line.split(",")
                    income=read_line[0]#[0]位数据代表收入
                    outcome=read_line[1]#[1]位数据代表支出
                    time=f"{read_line[2][0:2:1]}:{read_line[2][2:4:1]}:{read_line[2][4:6:1]}"#格式化的时间

                    print(income,outcome,time)
            else:
                print("err")
        #文件不存在
        else:
            print("此文件不存在")
            return 0

    #读取货物函数
    def read_goods(goods_name,mode,index):
        """
        goods_name:货物名称,函数内部用以确定文件位置
        mode:读取文件方法,1:返回索引号所在行颜色,2:返回尺寸,3:返回价格,4:返回库存数量,5:返回格式化数据[颜色,尺寸,价格,数量,索引值]
        index:索引值
        """
        #通过索引号找到某一行数据
        def find_target_index(file_path,target_index):
            """
            用于通过索引号找到某一行数据,返回值为索引号行,格式化成列表/无法输出索引值
            file_path:文件路径
            target_index:索引号
            """
            with open(file_path, 'r',encoding="UTF-8") as file:
                for line in file:
                    elements = line.strip().split(",")  # 将每一行按逗号分割成元素
                    if int(elements[-1]) == target_index:  # 判断最后一位数字是否等于目标索引号
                        return(line.split(","))
                        
                else:
                    print("未找到目标索引号对应的行")
        #确定需要读取的货物存在
        if(os.path.exists(f"dir/goods/{goods_name}.oc")):

            if mode==1:
                return find_target_index(f"dir/goods/{goods_name}.oc",index)[0]
            elif mode==2:
                return find_target_index(f"dir/goods/{goods_name}.oc",index)[1]
            elif mode==3:
                return find_target_index(f"dir/goods/{goods_name}.oc",index)[2]
            elif mode==4:
                return find_target_index(f"dir/goods/{goods_name}.oc",index)[3]
            elif mode==5:
                return find_target_index(f"dir/goods/{goods_name}.oc",index)
            else:
                print("err")
                return 0
        #货物不存在
        else:
            print("err")
            return 0
        
    #通过输入颜色与尺寸获取特定货物数据
    def read_specific_goods(goods_name,colour,size):
        """
        通过输入颜色与尺寸获取特定货物数据,所有数据输入格式必须为"字符串格式",返回值为(价格,货物数量,索引行号)
        goods_name:货物名称,函数内部用以确定文件位置
        colour:颜色数据
        size:尺寸数据
        """
        global inner_search_index
        #检测颜色和尺寸是否一样
        def detect_colourandsize(colour,size):
            """
            内置函数,用于文件遍历颜色和尺寸重复项
            相同输出0并且全局公布索引值,不同输出1
            """
            f=open(f"dir/goods/{goods_name}.oc","r",encoding="UTF-8")
            #返回索引值/全局公布
            global inner_search_index
            for line in f:
                read_line=line.split(",")
                #颜色尺寸相同
                if read_line[0]==colour and read_line[1]==size:
                    #返回索引值/全局公布
                    inner_search_index=int(read_line[4])
                    return 0
            #不同
            return 1    
        #确定需要读取的货物存在
        if(os.path.exists(f"dir/goods/{goods_name}.oc")):
            
            
            if(detect_colourandsize(colour,size)):
                #不同
                print(f"{goods_name}货物中不存在颜色为{colour},尺寸为{size}的数据")
            else:
                #相同
                return(file.read_goods(goods_name,3,inner_search_index),file.read_goods(goods_name,4,inner_search_index),inner_search_index)
        #货物不存在
        else:
            print("err")
            return 0
    
    #写日收入支出数据
    def write_data(inout_data):
        """
        inout_data格式: 收入,支出/支出写正数,\t时间(时分秒/自动补充)
        """

        #检测文件夹是否有今天的数据，若不是则创建新文件,若文件夹丢失则创建新文件夹
        if(os.path.exists('dir')):
            #检测log文件夹存在
            if(os.path.exists('dir/log')):
                #存在今日文件，使用追加信息
                if(os.path.exists(f"dir/log/{get_time.localtime()}.oc")):
                    f = open(f"dir/log/{get_time.localtime()}.oc","a",encoding='UTF-8')
                    f.write(inout_data)
                    f.write(f",{get_time.time_hour()}")
                    f.write('\n')
                    print("存在本文件")
                    f.close()

                #不存在今日文件，创建新文件并输入第一条信息
                else:
                    f = open(f"dir/log/{get_time.localtime()}.oc","w",encoding='UTF-8')
                    f.write(inout_data)
                    f.write(f",{get_time.time_hour()}")
                    f.write('\n')
                    print("创建新文件")
                    f.close()
            #不存在log文件夹,则创建文件夹并
            else:
                folder_path = "dir/log/"
                os.makedirs(folder_path)
                return file.write_data(inout_data)
            
        #若不存在dir文件夹则创建文件夹
        else:
            # 指定要创建的文件夹路径
            folder_path = "dir/"
            # 使用os.makedirs()创建文件夹
            os.makedirs(folder_path)
            #新建文件并写入
            return file.write_data(inout_data)

        print(f"写入{inout_data}")
        
        print(f"数据保存成功,系统时间{get_time.print_time()}")

    #写货物清单数据，每个货物单独一个文件，存在goods文件夹中
    def write_goods(goods,colour,size,price,num):
        """
        调用后可直接使用，每次调用产生一次输入
        """
        global search_index

        #通过索引号找到某一行数据
        def find_target_index(file_path,target_index):
            """
            用于通过索引号找到某一行数据,返回值为索引号行,格式化成列表/无法输出索引值
            file_path:文件路径
            target_index:索引号
            """
            with open(file_path, 'r',encoding="UTF-8") as file:
                for line in file:
                    elements = line.strip().split(",")  # 将每一行按逗号分割成元素
                    if int(elements[-1]) == target_index:  # 判断最后一位数字是否等于目标索引号
                        return(line.split(","))
                        
                else:
                    print("未找到目标索引号对应的行")                   
            
        #检测颜色和尺寸是否一样
        def detect_colourandsize(colour,size):
            """
            内置函数,用于文件遍历颜色和尺寸重复项
            相同输出0并且全局公布索引值,不同输出1
            """
            f=open(f"dir/goods/{goods}.oc","r",encoding="UTF-8")
            #返回索引值/全局公布
            global search_index
            for line in f:
                read_line=line.split(",")
                #颜色尺寸相同
                
                if read_line[0]==colour and read_line[1]==size:
                    #返回索引值/全局公布
                    search_index=int(read_line[4])
                    return 0
            #不同
            return 1    
            
        #检测价格是否改变
        def detect_price(search_index):
            """
            内置函数,若输入的新价格与原本价格不同则输出0,相同则输出1
            """
            search_index=int(search_index)
            #读取到索引行           
            #输入与原本数据相同
            if find_target_index(f"dir/goods/{goods}.oc",search_index)[2]==price:
                return 1
            #输入与原本数据不同
            else:
                return 0
                   
        #替换文件内容
        def replace_info_in_file(file_path, line_number, column_number, new_info):
            """
            用于替换文件某行某列内容
            line_number:行数
            colunmn_number:列数(自动过滤符号)
            new_info:需要替换的内容
            """
            with open(file_path, encoding='utf-8') as file:
                    lines = file.readlines()

            # print(type(lines))
            line = lines[line_number - 1]

            #输出原行
            # print(line)

            #格式化此行
            format=line.split(",")
            #整合此行
            print(f"在索引号{line_number-1}写入新数据{new_info}")
            #格式化新数据为单个列表
            new_info=[new_info]
            #整合新行数据
            line = format[:column_number - 1] + new_info + format[column_number:]
            new_line=str(line).strip("[").strip("]").replace("'","").replace(" ","")[:-2]
            #删除旧行数据
            lines.pop(line_number-1)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines[:line_number - 1])
                file.write(new_line)
                file.write('\n')
                file.writelines(lines[line_number - 1:])
            file.close()


        """goods=str(input("请输入货物名称(输入exit退出): "))
        if goods == "":
            print("请输入货物名称")
            return file.write_goods()
        elif goods == "exit":
            return 0
        else:
            colour = str(input("请输入货物颜色: "))
            if colour=="":
                colour=0
            size = str(input("请输入尺寸: (毫米)"))
            if size=="":
                size=0
            price = str(input("请输入货物价格: (每颗)"))
            if price=="":
                price=0
            num = str(input("请输入货物数量: "))
            if num=="":
                num=0"""
        index=0

        #检测dir文件夹存在
        if(os.path.exists('dir')):
            #检测goods文件夹存在
            if(os.path.exists('dir/goods')):
                #存在此货物，使用追加信息
                #若货物名称存在，则更新各种信息
                #整合goods_data
                goods_data=f"{colour},{size},{price},{num},{index}"
                if(os.path.exists(f"dir/goods/{goods}.oc")):
                    #检测颜色尺寸是否相同，若相同则更改价格及数量信息，更改价格信息需提醒确认
                    f=open(f"dir/goods/{goods}.oc","r",encoding="UTF-8")
                    #读取文件的最后一位索引值
                    for line in f:
                        read_line=line.split(",")
                    #索引值更新
                    i=int(read_line[4])
                    index=i+1
                    goods_data=f"{colour},{size},{price},{num},{index}"
                    

                    if(detect_colourandsize(colour,size)):
                    #颜色尺寸任意一个不同
                        f = open(f"dir/goods/{goods}.oc","a",encoding='UTF-8')
                        f.write(goods_data)
                        print(f"写入{goods_data} ")
                        f.write('\n')
                        f.close()
                    #颜色尺寸相同
                    else:
                        print(f"颜色{colour},尺寸{size}")
                        detect_colourandsize(colour,size)
                        print(f"相同索引值为{search_index}")
                        #检测价格是否变动，若价格变动则询问是否确定
                        if(detect_price(search_index)):
                            #价格不变
                            #输入数量则为新入库，在原有基础上加入新数字
                            #读取原数字
                            read_num=find_target_index(f'dir/goods/{goods}.oc',search_index)[3]
                            #计算更改后的数据
                            num=int(num)
                            read_num=int(read_num)
                            new_number=num+read_num
                            #更新数据
                            replace_info_in_file(f'dir/goods/{goods}.oc',(search_index+1),4,f"{new_number}")
                        #价格改变

                        else:

                            choice=input("是否确认更改价格(yes确认更改并录入库存,no取消并重新输入)")

                            if choice=="yes":
                                #更新价格信息
                                replace_info_in_file(f'dir/goods/{goods}.oc', (search_index+1), 3, f'{price}')
                                #输入数量则为新入库，在原有基础上加入新数字
                                #读取原数字
                                read_num=find_target_index(f'dir/goods/{goods}.oc',search_index)[3]
                                #计算更改后的数据
                                num=int(num)
                                read_num=int(read_num)
                                new_number=num+read_num
                                #更新数据
                                replace_info_in_file(f'dir/goods/{goods}.oc',(search_index+1),4,f"{new_number}")
                            elif choice=="no":
                                return file.write_goods()
                            else:
                                print("err")
                                return 0
                #若货物不存在，则创建新货物项
                else:
                    index=0
                    f = open(f"dir/goods/{goods}.oc","w",encoding='UTF-8')
                    f.write(goods_data)
                    f.write('\n')
                    print("创建新文件")
                    f.close()
            #goods文件夹不存在，创建文件夹并重新调用
            else:
                folder_path = "dir/goods/"
                os.makedirs(folder_path)
                return file.write_goods()
        #若不存在dir文件夹则创建文件夹
        else:
            # 指定要创建的文件夹路径
            folder_path = "dir/"
            # 使用os.makedirs()创建文件夹
            os.makedirs(folder_path)
            return file.write_goods()
    
    #销售货物函数，通过输入销售的货物信息修改库存量
    def sale_goods(goods_name,colour,size,num):
        """
        销售货物函数，通过输入销售的货物信息修改库存量/输入全部为正数
        goods_name:货物名称,函数内部用以确定文件位置
        colour:输入销售货物的颜色
        size:输入销售货物的尺寸
        num:销售的数量
        """
        global sale_search_index
        #检测颜色和尺寸是否一样
        def detect_colourandsize(colour,size):
            """
            内置函数,用于文件遍历颜色和尺寸重复项
            相同输出0并且全局公布索引值,不同输出1
            """
            f=open(f"dir/goods/{goods_name}.oc","r",encoding="UTF-8")
            #返回索引值/全局公布
            global sale_search_index
            for line in f:
                read_line=line.split(",")
                #颜色尺寸相同
                
                if read_line[0]==colour and read_line[1]==size:
                    #返回索引值/全局公布
                    sale_search_index=int(read_line[4])
                    return 0
            #不同
            return 1    
            #替换文件内容
        
        def replace_info_in_file(file_path, line_number, column_number, new_info):
            """
            用于替换文件某行某列内容
            line_number:行数
            colunmn_number:列数(自动过滤符号)
            new_info:需要替换的内容
            """
            with open(file_path, encoding='utf-8') as file:
                    lines = file.readlines()

            # print(type(lines))
            line = lines[line_number - 1]

            #输出原行
            # print(line)

            #格式化此行
            format=line.split(",")
            #整合此行
            print(f"在索引号{line_number - 1}写入新数据{new_info}")
            #格式化新数据为单个列表
            new_info=[new_info]
            #整合新行数据
            line = format[:column_number - 1] + new_info + format[column_number:]
            new_line=str(line).strip("[").strip("]").replace("'","").replace(" ","")[:-2]
            #删除旧行数据
            lines.pop(line_number-1)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines[:line_number - 1])
                file.write(new_line)
                file.write('\n')
                file.writelines(lines[line_number - 1:])
            file.close()
        
        def find_target_index(file_path,target_index):
            """
            用于通过索引号找到某一行数据,返回值为索引号行,格式化成列表/无法输出索引值
            file_path:文件路径
            target_index:索引号
            """
            with open(file_path, 'r',encoding="UTF-8") as file:
                for line in file:
                    elements = line.strip().split(",")  # 将每一行按逗号分割成元素
                    if int(elements[-1]) == target_index:  # 判断最后一位数字是否等于目标索引号
                        return(line.split(","))
                        
                else:
                    print("未找到目标索引号对应的行") 
            
        #确定需要读取的货物存在
        if(os.path.exists(f"dir/goods/{goods_name}.oc")):
            #定位到需要更换的索引行
            detect_colourandsize(colour,size)
            #读取原数字
            read_num=find_target_index(f'dir/goods/{goods_name}.oc',sale_search_index)[3]
            #计算更改后的数据
            num=int(num)
            read_num=int(read_num)
            new_number=read_num-num
            #确定库存内是否还有足够货物
            #库存不够
            if new_number<0:
                print(f"库存量为{file.read_goods(goods_name,4,sale_search_index)}")
                print("库存不足,请重新输入")
                return 0
            #库存充足
            else:
                #更新数据
                replace_info_in_file(f'dir/goods/{goods_name}.oc',(sale_search_index+1),4,f"{new_number}")
                return 1
        #货物不存在
        else:
            print("货物不存在")
            return 2

    #备份函数
    def backup(mode,input):
        """
        备份函数,用于备份数据,备份的数据储存在bak文件夹内部
        mode:1:备份当日收入支出数据.2:备份所有收入支出数据到当日新建文件夹内.3:备份特定日期收入支出数据至bak/log.\n
        \t4:备份所有货物数据到bak/goods/新文件夹内(以日期命名新文件夹).5:备份特定货物至bak/goods,尾缀日期.
        input:mode=1,2,4输入0.\n
        \t3:输入日期/输入格式2024429:.5:输入货物名称
        """
        #复制文件到另一个文件夹内
        def copy_file(original_path, copy_path):
            try:
                shutil.copy(original_path, copy_path)
                print(f"文件成功从 {original_path} 保存至 {copy_path}")
            except FileNotFoundError:
                print("文件不存在")
            except IOError:
                print("复制文件失败")

        def copy_folder_contents(original_path, copy_path):
            try:
                for item in os.listdir(original_path):
                    item_path = os.path.join(original_path, item)
                    if os.path.isfile(item_path):
                        shutil.copy(item_path, copy_path)
                        print(f"文件{item} 成功复制到 {copy_path}")
            except FileNotFoundError:
                print("文件夹不存在")
            except IOError:
                print("复制文件夹失败")

        print(input)

        #检测日志备份文件夹是否存在
        if(os.path.exists('bak/log')):
            pass
        #文件夹不存在则创建新文件夹
        else:
            folder_path = "bak/log/"
            os.makedirs(folder_path)
            return file.backup(mode,input)
        
        #检测货物备份文件夹是否存在
        if(os.path.exists('bak/goods')):
            pass
        #文件夹不存在则创建新文件夹
        else:
            folder_path = "bak/goods/"
            os.makedirs(folder_path)
            return file.backup(mode,input)

        #备份当日收入支出数据
        if mode==1:
            #确认当日日志文件存在
            if(os.path.exists(f"dir/log/{get_time.localtime()}.oc")):
                copy_file(f"dir/log/{get_time.localtime()}.oc","bak/log/")
            else:
                print("当日文件不存在")
                return 0
            print(mode)
        #备份所有收入支出数据到当日新建文件夹内
        elif mode==2:
            #确认文件夹存在
            if(os.path.exists("dir/log")):
                #创建当日新建文件夹
                folder_path = f"bak/log/{get_time.localtime()}"
                os.makedirs(folder_path)
                #移动文件
                copy_folder_contents("dir/log",f"bak/log/{get_time.localtime()}")
            else:
                print("文件夹不存在")
                return 0
            print(mode)
        #备份特定日期收入支出数据
        elif mode==3:
            #检测文件是否存在
            if (os.path.exists(f"dir//log/{input}.oc")):
                copy_file(f"dir/log/{input}.oc","bak/log/")
            else:
                print("文件不存在")
                return 0
            print(mode)

        #备份所有货物数据到bak/goods/新文件夹内(以日期命名新文件夹)
        elif mode==4:
            #确认文件夹存在
            if (os.path.exists("dir/goods")):
                #创建当日新建文件夹
                folder_path = f"bak/goods/{get_time.localtime()}"
                os.makedirs(folder_path)
                #移动文件
                copy_folder_contents("dir/goods",f"bak/goods/{get_time.localtime()}")
            else:
                print("文件夹不存在")
                return 0

            print(mode)
        #备份特定货物至bak/goods,尾缀日期
        elif mode==5:
            #检测是否存在需要备份的文件
            if (os.path.exists(f"dir/goods/{input}.oc")):
                copy_file(f"dir/goods/{input}.oc","bak/goods/")
            else:
                print("货物不存在")
                return 0
            print(mode)

        else:
            print("err")
            return 0

    #恢复备份数据函数
    def recover_backup(mode,input):
        """
        恢复备份数据函数,用于恢复备份的数据,会将备份数据恢复到dir文件夹内,如有冲突则询问是否保留
        mode:1:恢复特定日期的日志至dir/log.2:恢复全部的日志至dir/log.3:恢复特定日期的货物至dir/goods.4:恢复全部的货物信息至dir/goods
        input:2,4:输入0.\n1,3:日期/格式为20241210.
        !!!会覆盖原文件!!!
        """

        #复制文件到另一个文件夹内
        def copy_file(original_path, copy_path):
            try:
                shutil.copy(original_path, copy_path)
                print(f"文件成功从 {original_path} 保存至 {copy_path}")
            except FileNotFoundError:
                print("文件不存在")
            except IOError:
                print("复制文件失败")
        
        #复制文件夹内部文件至另一个文件夹内
        def copy_folder_contents(original_path, copy_path):
            try:
                for item in os.listdir(original_path):
                    item_path = os.path.join(original_path, item)
                    if os.path.isfile(item_path):
                        shutil.copy(item_path, copy_path)
                        print(f"文件{item} 成功复制到 {copy_path}")
            except FileNotFoundError:
                print("文件夹不存在")
            except IOError:
                print("复制文件夹失败")


        #恢复特定日期的日志至dir/log
        if mode==1:
            #检测日志文件夹是否存在
            if(os.path.exists('bak/log')):
                copy_file(f"bak/log/{input}.oc","dir/log")

            #文件夹不存在则退出函数
            else:
                print("备份文件夹不存在")
                return 0
        #恢复全部的日志至dir/log
        elif mode==2:
            #检测日志文件夹是否存在
            if(os.path.exists('bak/log')):
                copy_folder_contents("bak/log","dir/log")

            #文件夹不存在则退出函数
            else:
                print("备份文件夹不存在")
                return 0
        #恢复特定日期的货物至dir/goods
        elif mode==3:
            #检测货物文件夹是否存在
            if(os.path.exists(f'bak/goods/{input}')):
                copy_folder_contents(f"bak/goods/{input}","dir/goods")
            #文件夹不存在则退出函数
            else:
                print("备份文件夹不存在")
                return 0
        #恢复全部的货物信息至dir/goods
        if mode==4:
            #检测货物文件夹是否存在
            if(os.path.exists('bak/goods')):
                copy_folder_contents("bak/goods","dir/goods")
            #文件夹不存在则退出函数
            else:
                print("备份文件夹不存在")
                return 0
            
        else:
            print("err")
            return 0





#测试区域

#测试写日收入销售数据
# file.write_data("200,20")

#测试读日收入支出数据
# print(file.read_data(2024429,2))

#测试写货物数据
# file.write_goods()

#测试读货物数据
# print(file.read_goods("砂金石",5,1))
# print(file.read_goods("砂金石",4,0))

#测试通过输入颜色与尺寸获取特定货物数据
# print(file.read_specific_goods("砂金石","浅绿色","12"))
# print(file.read_specific_goods("砂金石","黄绿色","12"))
# print(file.read_specific_goods("砂金石","黄绿色","10")[2])
# print(file.read_specific_goods("砂金石","黄绿色","8"))

#测试销售货物函数，通过输入销售的货物信息修改库存量
# file.sale_goods("砂金石","浅绿色","12",12)
# file.sale_goods("砂金石","黄绿色","12",12)

#测试备份函数
# file.backup(4,0)

#测试恢复备份数据函数
