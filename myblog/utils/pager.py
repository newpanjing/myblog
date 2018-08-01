import math


# 获取页码
def get_numbers(total, size, current, show_number):
    current = int(current)
    total_page_num = int((total - 1) / size + 1)
    val = show_number / 2
    # 向上取整，-1 减去当前页
    left = math.ceil(val) - 1
    # 向下取整
    right = math.floor(val)

    array = []

    # 计算开始和结束
    start = current - left
    end = current + right

    # 如果开始小于1，求从0开始的负数绝对值
    if start < 1:
        val = 0 - start
        end += abs(val) + 1
        start = 1

    # 结束大于总页数，结束就等于总页数
    if end > total_page_num:
        end = total_page_num

    # 循环计算页码
    for i in range(start, end + 1):
        array.append(i)

    return array

# current = 100
# arr = get_numbers(1011, 5, current, 7)
# print(arr)
