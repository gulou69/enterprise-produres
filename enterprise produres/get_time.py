#获取系统时间(精确到秒)
import datetime

#输出时间数据（格式：年，月，日，时，分，秒，周几）
def time():
    current_time = datetime.datetime.now()
    #星期
    weekday = current_time.weekday()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    #时间
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    #输出补0
    if second<10: 
        global se
        se=0
    else:
        se=""
    if minute<10:
        global mi
        mi=0
    else:
        mi=""
    return(year,month,day,hour,minute,second,weekdays[weekday])
    # print(f"年: {year}")
    # print(f"月: {month}")
    # print(f"日: {day}")
    # print(f"今天是{weekdays[weekday]}")
    # print(f"时: {hour}")
    # print(f"分: {minute}")
    # print(f"秒: {second}")

#输出格式化时间
def print_time():
    return(f"{time()[0]}年{time()[1]}月{time()[2]}日{time()[3]}:{mi}{time()[4]}:{se}{time()[5]},{time()[6]}")

#输出数字格式化年月日/文件创建用
def localtime():
    return(f"{time()[0]}{time()[1]}{time()[2]}")

#输出数字格式化时分秒/文件记录用
def time_hour():
    return(f"{time()[3]}{mi}{time()[4]}{se}{time()[5]}")