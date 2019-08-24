import math


def get_page_range(page_num, show_num, current_page):
    # 分偶数和奇数
    current_page = int(current_page)
    page_num = int(page_num)
    show_num = int(show_num)

    if show_num % 2 == 0:
        fore = int((show_num - 1) / 2)
        after = int(show_num / 2)
    else:
        fore = int(show_num / 2)
        after = math.ceil((show_num - 1) / 2)

    star = current_page - fore
    end = current_page + after
    if star == 0:
        star = 1
        end += star
    elif star < 0:
        end += int(math.fabs(star))
        end += 1
        star = 1

    if end > page_num:
        star -= end - page_num
        end = page_num

    if star < 1:
        star = 1
    if end > page_num:
        end = page_num
    return star, end


# 获取页码
def get_numbers(total, size, current, show_number):
    current = int(current)
    total_page_num = int((total - 1) / size + 1)
    start, end = get_page_range(total_page_num, show_number, current)

    array = []
    # 循环计算页码
    for i in range(start, end + 1):
        array.append(i)

    return array

# current = 100
# arr = get_numbers(1011, 5, current, 7)
# print(arr)
