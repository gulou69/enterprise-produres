import time
import os
import get_time
from file_manager import file
import tkinter as tk
from tkinter import *
from tkinter import simpledialog, messagebox
from ttkbootstrap import Style, Button
from tkinter.simpledialog import Dialog
from ttkbootstrap.constants import *

LOG_LINE_NUM = 0

#获取当前时间
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

#日志动态打印
def write_log_to_Text(log_data_Text, logmsg):
    global LOG_LINE_NUM
    current_time = get_current_time()
    logmsg_in = str(current_time)  + ":" + "\n" + str(logmsg) + "\n"

    if LOG_LINE_NUM <= 3:
        log_data_Text.insert(END, logmsg_in)
        LOG_LINE_NUM += 1
    else:
        log_data_Text.delete(1.0, 2.0)
        log_data_Text.delete(1.0, 2.0)
        log_data_Text.insert(END, logmsg_in)


#入库选项-弹出有多个输入的对话框
class window_write_goods(Dialog):
    def body(self, master):
        tk.Label(master, text="输入货物名称:").grid(row=0)
        tk.Label(master, text="输入货物颜色:").grid(row=1)
        tk.Label(master, text="输入货物尺寸(毫米):").grid(row=2)
        tk.Label(master, text="输入货物价格(每颗):").grid(row=3)
        tk.Label(master, text="输入货物数量(颗):").grid(row=4)
        #提取输入
        self.name = tk.Entry(master)
        self.colour = tk.Entry(master)
        self.size = tk.Entry(master)
        self.price = tk.Entry(master)
        self.number = tk.Entry(master)
        #输入框定位
        self.name.grid(row=0, column=1)
        self.colour.grid(row=1, column=1)
        self.size.grid(row=2, column=1)
        self.price.grid(row=3, column=1)
        self.number.grid(row=4, column=1)

    def apply(self):
        input_name = self.name.get()
        #如果货物名称有输入
        if input_name:
            input_colour = self.colour.get()
            input_size = self.size.get()
            input_price = self.price.get()
            input_number = self.number.get()
            self.result_write_goods = input_name, input_colour,input_size,input_price,input_number
            #调用文件库写入进货
            file.write_goods(input_name,input_colour,input_size,input_price,input_number)
            #计算进货需要支出的经费
            outcome=float(input_price)*int(input_number)
            #写入data
            file.write_data(f"0,{outcome}")

            write_log_to_Text(log_output,f"货物名称: {input_name}, 货物颜色: {input_colour},货物尺寸:{input_size}毫米,货物价格:{input_price}每颗,货物数量:{input_number}每颗,共支出{outcome}元")
        #未输入货物名称
        else:
            write_log_to_Text(log_output,"请输入货物名称")
            return 0

def button_write_goods():
    user_input = window_write_goods(root)
    #返回一个元组
    # print(f"对话框返回的结果: {window_write_goods.result_write_goods}")


#销售选项-弹出有多个输入的对话框
class window_sale_goods(Dialog):
    def body(self, master):
        tk.Label(master, text="输入货物名称:").grid(row=0)
        tk.Label(master, text="输入货物颜色:").grid(row=1)
        tk.Label(master, text="输入货物尺寸(毫米):").grid(row=2)
        tk.Label(master, text="输入货物数量(颗):").grid(row=3)
        #输入框
        self.name = tk.Entry(master)
        self.colour = tk.Entry(master)
        self.size = tk.Entry(master)
        self.number = tk.Entry(master)
        #输入框定位
        self.name.grid(row=0, column=1)
        self.colour.grid(row=1, column=1)
        self.size.grid(row=2, column=1)
        self.number.grid(row=3, column=1)

    def apply(self):
        input_name = self.name.get()
        #如果货物名称有输入
        if input_name:
            input_colour = self.colour.get()
            input_size = self.size.get()
            input_number = self.number.get()
            self.result_sale_goods = input_name, input_colour,input_size,input_number
            #写新数据
            #库存充足
            if (file.sale_goods(input_name,input_colour,input_size,input_number)==1):
                #计算收入
                income = int(input_number)*float(file.read_specific_goods(input_name,input_colour,input_size)[0])
                #写收入
                file.write_data(f"{income},0")
                write_log_to_Text(log_output,f"{input_name}颜色: {input_colour}尺寸:{input_size}毫米,销售{input_number}颗,收入{income}元")
            
            #库存不足
            elif (file.sale_goods(input_name,input_colour,input_size,input_number)==0):
                write_log_to_Text(log_output,"库存不足,请重新输入")
            
            #货物不存在
            elif (file.sale_goods(input_name,input_colour,input_size,input_number)==2):
                write_log_to_Text(log_output,"货物不存在")
                
        #未输入货物名称
        else:
            write_log_to_Text(log_output,"请输入货物名称")
            return 0

def button_sale_goods():
    user_input = window_sale_goods(root)
    #返回一个元组
    # print(f"对话框返回的结果: {window_sale_goods.result_sale_goods}")


#统计数据选项-弹出多个选项框选择:
"""
统计营销总额:
--------本日营销
--------其他日期输入框:其他日期营销
统计货物库存剩余:
--------输入货物名称获取此货物全部库存
--------输入货物名称和颜色尺寸获取库存
"""
#第一个窗口
class window_statistics(simpledialog.Dialog):
    def body(self, master):
        self.result = None
        self.option = tk.IntVar()
        
        tk.Label(master, text="请选择统计类型:").pack()
        tk.Radiobutton(master, text="统计营销总额\t", variable=self.option, value=1).pack()
        tk.Radiobutton(master, text="统计货物库存剩余\t", variable=self.option, value=2).pack()
        
        return master

    def apply(self):
        if self.option.get() == 1:
            sub_dialog = window_statistics_data(self)
            self.result = sub_dialog.result
        elif self.option.get() == 2:
            sub_dialog = window_statistics_goods(self)
            self.result = sub_dialog.result
#分支窗口1-选择营销统计
class window_statistics_data(simpledialog.Dialog):
    def body(self, master):
        self.result = None
        self.option = tk.IntVar()
        tk.Label(master, text="请选择统计类型:").pack()
        tk.Radiobutton(master, text="本日营销总额\t", variable=self.option, value=3).pack()
        tk.Radiobutton(master, text="其他日期营销额\t", variable=self.option, value=4).pack()
        tk.Label(master, text="其他日期营销额日期输入格式:xxxx年x月x日").pack()
        self.entry = tk.Entry(master)
        self.entry.pack()
        
        return master

    def apply(self):
        #本日营销总额
        if self.option.get() == 3:
           file.read_data(get_time.localtime(),1)
           messagebox.showinfo("本日营销总额", f"今日营销总额为{file.read_data(get_time.localtime(),1)}")
           window_statistics(root)
        #其他日期营销额
        elif self.option.get() == 4:
            user_input = self.entry.get()
            if user_input:
                date_parts = user_input.split("年")[0], user_input.split("年")[1].split("月")[0], user_input.split("月")[1].split("日")[0]
                output_date = "".join(date_parts)
                messagebox.showinfo(f"{user_input}营销总额", f"营销总额为{file.read_data(output_date,1)}")
                window_statistics(root)
            else:
                messagebox.showinfo("请输入信息","请输入信息")
                window_statistics(root)
#分支窗口2-选择货物统计
class window_statistics_goods(simpledialog.Dialog):
    def body(self, master):
        self.result = None
        self.option = tk.IntVar()
        
        tk.Label(master, text="请选择统计类型:").grid(row=0)
        tk.Label(master, text="选项1:").grid(row=1,column=0)
        tk.Radiobutton(master, text="输入货物名称全部库存5量\t", variable=self.option, value=5).grid(row=1,column=1)
        #名称
        tk.Label(master, text="输入货物名称:").grid(row=2,column=0)
        #输入框
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=2,column=1)
        tk.Label(master, text="选项2:").grid(row=3,column=0)
        tk.Radiobutton(master, text="输入货物名称和颜色尺寸获取库存\t", variable=self.option, value=6).grid(row=3,column=1)
        #名称
        tk.Label(master, text="输入货物名称:").grid(row=4,column=0)
        #输入框
        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=4,column=1)
        #颜色
        tk.Label(master, text="输入货物颜色:").grid(row=5,column=0)
        #输入框
        self.entry3 = tk.Entry(master)
        self.entry3.grid(row=5,column=1)
        #尺寸
        tk.Label(master, text="输入货物尺寸:").grid(row=6,column=0)
        #输入框
        self.entry4 = tk.Entry(master)
        self.entry4.grid(row=6,column=1)
        
        return master


    def apply(self):
        #输入货物名称全部库存量
        if self.option.get() == 5:
            user_input = self.entry1.get()
            if user_input:
                if (os.path.exists(f"dir/goods/{user_input}.oc")):
                    total_sum = 0
                    with open(f"dir/goods/{user_input}.oc",'r',encoding="utf-8") as f:
                        for line in f:
                            numbers = line.strip().split(',')
                            last_number = float(numbers[-2])
                            total_sum += last_number

                    messagebox.showinfo(f"货物{user_input}库存量",f"货物{user_input}剩余库存{total_sum}")
                    window_statistics(root)
                else:
                    messagebox.showinfo("货物不存在","货物不存在")
                    window_statistics(root)
            else:
                messagebox.showinfo("请输入信息","请输入信息")
                return window_statistics(root)


        #输入货物名称和颜色尺寸获取库存
        elif self.option.get() == 6:
            user_input_name = self.entry2.get()
            user_input_colour = self.entry3.get()
            user_input_size = self.entry4.get()
            if user_input_name:
                if (os.path.exists(f"dir/goods/{user_input_name}.oc")):
                    num=file.read_specific_goods(user_input_name,user_input_colour,user_input_size)[1]
                    messagebox.showinfo(f"货物{user_input_name}库存量",f"货物{user_input_name},颜色{user_input_colour}尺寸{user_input_size}剩余库存{num}")
                else:
                    messagebox.showinfo("货物不存在","货物不存在")
                    window_statistics(root)
            else:
                messagebox.showinfo("请输入信息","请输入信息")
                return window_statistics(root)

def button_statistics():
    user_choice = window_statistics(root)


class window_backup(simpledialog.Dialog):
    def body(self,master):
        self.result = None
        self.option = tk.IntVar()
        tk.Label(master, text="请选择备份类型:").pack()
        tk.Radiobutton(master, text="备份今日营销数据\t", variable=self.option, value=1).pack()
        tk.Radiobutton(master, text="备份所有营销数据\t", variable=self.option, value=2).pack()
        tk.Radiobutton(master, text="备份所有货物数据\t", variable=self.option, value=3).pack()
        tk.Radiobutton(master, text="备份特定货物数据\t", variable=self.option, value=4).pack()
        #货物名称
        tk.Label(master, text="输入货物名称:").pack()
        #输入框
        self.entry = tk.Entry(master)
        self.entry.pack()

        return master
    def apply(self):
        if self.option.get() == 1:
            file.backup(1,0)
            messagebox.showinfo("备份成功",f"今日营销数据备份成功")
        elif self.option.get() == 2:
            file.backup(2,0)
            messagebox.showinfo("备份成功",f"所有营销数据备份成功")
        elif self.option.get() == 3:
            file.backup(4,0)
            messagebox.showinfo("备份成功",f"所有货物数据备份成功")
        elif self.option.get() == 4:
            user_input_name = self.entry.get()
            if user_input_name:
                file.backup(5,user_input_name)
                messagebox.showinfo("备份成功",f"{user_input_name}信息数据备份成功")
                sub_dialog = window_statistics_goods(self)
                self.result = sub_dialog.result
            else:
                messagebox.showinfo("请输入信息","请输入信息")
                return window_backup(root)
def button_backup():
    user_choice = window_backup(root)

#操作说明界面
def show_instructions():
    messagebox.showinfo("操作说明", "入库：输入货物信息保存在仓库内\n销售：输入货物信息销售货物\n统计数据：统计营销或者货物信息\n备份数据：备份数据信息至bak文件夹内")

# 创建主窗口
root = tk.Tk()

# 设置根窗口的图标
root.iconphoto(True, tk.PhotoImage(file='icon.ico'))

root.geometry('720x480')
style = Style(theme='lumen')
root["bg"] = "WhiteSmoke" #窗口背景色

# root.attributes("-alpha",0.9)  #虚化，值越小虚化程度越高



# 创建按钮并绑定到假设的函数
buttons_frame = tk.Frame(root)
buttons_frame.place(x=530, y=80)

write_goods = Button(buttons_frame, text="入库", command=button_write_goods, bootstyle='success-outline', width=20)
write_goods.pack(pady=5, ipadx=10, ipady=10)

sale_goods = Button(buttons_frame, text="销售", command=button_sale_goods, bootstyle='warning-outline', width=20)
sale_goods.pack(pady=5, ipadx=10, ipady=10)

statistics = Button(buttons_frame, text="统计数据", command=button_statistics, bootstyle='info-outline', width=20)
statistics.pack(pady=5, ipadx=10, ipady=10)

backup = Button(buttons_frame, text="备份数据", command=button_backup, bootstyle='danger-outline', width=20)
backup.pack(pady=5, ipadx=10, ipady=10)


# 圆形问号按钮
canvas = tk.Canvas(buttons_frame, width=40, height=40, bg='white', highlightthickness=0)
canvas.pack(pady=5)
circle = canvas.create_oval(5, 5, 35, 35, fill='lightgrey', outline='lightgrey')
question_text = canvas.create_text(20, 20, text="?", font=('Arial', 16, 'bold'))
canvas.tag_bind(circle, '<Button-1>', lambda x: show_instructions())
canvas.tag_bind(question_text, '<Button-1>', lambda x: show_instructions())

# 日志输出标签和文本框
log_label = tk.Label(root, text="日志输出:")
log_label.place(x=10, y=310)

log_output = tk.Text(root, width=60, height=9)
log_output.place(x=10, y=330)

"""
if user_input:
    log_output.insert(tk.END, f"事件: demo_4 执行，输入为 {user_input}\n")
"""
# 运行主循环
root.mainloop()

