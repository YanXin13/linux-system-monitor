# -*- coding:utf-8 -*-

import os
import time
import datetime
import xlsxwriter
import psutil
from pathlib import Path


def percent_to_float(per):
    try:
        aa = float(per.strip().strip('%'))
        bb = aa / 100.0
        return bb
    except:
        return -1


def get_system_memory():
    try:
        return float(os.popen('''
        free -m | awk 'NR==2{printf "%.2f\t\t", $3/1024 }'
        ''').read())
    except:
        return -1

def get_system_disk():
    try:
        return float(os.popen('''
        df -h | awk '$NF=="/"{printf "%.2f\t\t", $3}'
        ''').read())
    except:
        return -1


def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def get_gpu_usage1():
    return percent_to_float(os.popen('''
    nvidia-smi --query-gpu=utilization.gpu --format=csv | awk 'NR==2{printf "%s%s\t\t", $1, $2}'
    ''').read())


def get_gpu_memory1():
    try:
        return float(os.popen('''
        nvidia-smi --query-gpu=memory.used --format=csv | awk 'NR==2{printf "%.2f\t\t", $1/1024}'
        ''').read())
    except:
        return -1

def get_gpu_usage2():
    return percent_to_float(os.popen('''
    nvidia-smi --query-gpu=utilization.gpu --format=csv | awk 'NR==3{printf "%s%s\t\t", $1, $2}'
    ''').read())


def get_gpu_memory2():
    try:
        return float(os.popen('''
        nvidia-smi --query-gpu=memory.used --format=csv | awk 'NR==3{printf "%.2f\t\t", $1/1024}'
        ''').read())
    except:
        return -1

def get_gpu_usage3():
    return percent_to_float(os.popen('''
    nvidia-smi --query-gpu=utilization.gpu --format=csv | awk 'NR==4{printf "%s%s\t\t", $1, $2}'
    ''').read())


def get_gpu_memory3():
    try:
        return float(os.popen('''
        nvidia-smi --query-gpu=memory.used --format=csv | awk 'NR==4{printf "%.2f\t\t", $1/1024}'
        ''').read())
    except:
        return -1


def get_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def debug_data():
    return 1


def is_end():
    end = Path(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'end'))
    if end.is_file():
        return True
    if end.is_dir():
        return True
    return False


# file exists

def main():
    # 创建一个excel
    workbook = xlsxwriter.Workbook("monitor_result.xlsx")
    # 创建一个sheet
    resultsheet = workbook.add_worksheet()
    worksheet = workbook.add_worksheet()
    # worksheet = workbook.add_worksheet("bug_analysis")

    # 自定义样式，加粗
    bold = workbook.add_format({'bold': 1})

    # --------1、准备数据并写入excel---------------
    # 向excel中写入数据，建立图标时要用到
    headings = ['Date', 'CPU', 'Memory', 'Disk', 'GPU Usage1', 'GPU Memory1', 'GPU Usage2', 'GPU Memory2', 'GPU Usage3', 'GPU Memory3']
    data = [get_date, get_cpu_usage, get_system_memory, get_system_disk, get_gpu_usage1, get_gpu_memory1, get_gpu_usage2, get_gpu_memory2, get_gpu_usage3, get_gpu_memory3]
    # data = [get_date, get_cpu_usage, debug_data, get_system_disk, get_cpu_usage, get_cpu_usage]

    # 写入表头
    worksheet.write_row('A1', headings, bold)

    # 写入数据
    row = 1
    per_format = workbook.add_format({'num_format': '0.00%'})
    while not is_end():
        print(data[0]())
        row += 1
        worksheet.write('A'+str(row), data[0]())
        worksheet.write('B'+str(row), data[1]())
        worksheet.write('C'+str(row), data[2]())
        worksheet.write('D'+str(row), data[3]())
        worksheet.write('E'+str(row), data[4](), per_format)
        worksheet.write('F'+str(row), data[5]())
        worksheet.write('G'+str(row), data[6](), per_format)
        worksheet.write('H'+str(row), data[7]())
        worksheet.write('I'+str(row), data[8](), per_format)
        worksheet.write('J'+str(row), data[9]())
        time.sleep(5)

    # --------2、生成图表并插入到excel---------------
    # 创建一个柱状图(column chart)
    cpu_col = workbook.add_chart({'type': 'column'})
    system_memory_col = workbook.add_chart({'type': 'column'})
    system_disk_col = workbook.add_chart({'type': 'column'})
    gpu_usage_col1 = workbook.add_chart({'type': 'column'})
    gpu_memory_col1 = workbook.add_chart({'type': 'column'})
    gpu_usage_col2 = workbook.add_chart({'type': 'column'})
    gpu_memory_col2 = workbook.add_chart({'type': 'column'}) 
    gpu_usage_col3 = workbook.add_chart({'type': 'column'})
    gpu_memory_col3 = workbook.add_chart({'type': 'column'})

    # 配置第一个系列数据
    cpu_col.add_series({
        # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
        # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
        'name': '=Sheet2!$B$1',
        # 'categories': '=Sheet1!$A$2:$A$7',
        'values': '=Sheet2!$B$2:$B$'+str(row),
        # 'line': {'color': 'red'},
    })
    system_memory_col.add_series({'name': '=Sheet2!$C$1', 'values': '=Sheet2!$C$2:$C$'+str(row)})
    system_disk_col.add_series({'name': '=Sheet2!$D$1', 'values': '=Sheet2!$D$2:$D$'+str(row)})
    gpu_usage_col1.add_series({'name': '=Sheet2!$E$1', 'values': '=Sheet2!$E$2:$E$'+str(row)})
    gpu_memory_col1.add_series({'name': '=Sheet2!$F$1', 'values': '=Sheet2!$F$2:$F$'+str(row)})
    gpu_usage_col2.add_series({'name': '=Sheet2!$G$1', 'values': '=Sheet2!$G$2:$G$'+str(row)})
    gpu_memory_col2.add_series({'name': '=Sheet2!$H$1', 'values': '=Sheet2!$H$2:$H$'+str(row)})
    gpu_usage_col3.add_series({'name': '=Sheet2!$I$1', 'values': '=Sheet2!$I$2:$I$'+str(row)})
    gpu_memory_col3.add_series({'name': '=Sheet2!$J$1', 'values': '=Sheet2!$J$2:$J$'+str(row)})
    
    # 设置图表的风格
    # chart_col.set_style(1)
    # 把图表插入到worksheet以及偏移
    resultsheet.insert_chart('A1', cpu_col, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A17', system_memory_col, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A33', system_disk_col, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A49', gpu_usage_col1, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A65', gpu_memory_col1, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A81', gpu_usage_col2, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A97', gpu_memory_col2, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A113', gpu_usage_col3, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})
    resultsheet.insert_chart('A129', gpu_memory_col3, {'x_offset': 25, 'y_offset': 10, 'x_scale': 3})

    workbook.close()


if __name__ == '__main__':
    main()
