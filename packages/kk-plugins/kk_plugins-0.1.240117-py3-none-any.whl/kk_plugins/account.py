def format_accounting(number):
    # 将数字转换为字符串，并去除小数部分
    str_number = str(int(number))

    # 检查数字的正负性
    if number < 0:
        sign = '-'
        str_number = str_number[1:]  # 去除负号
    else:
        sign = ''

    # 添加千位分隔符
    parts = []
    while str_number:
        parts.append(str_number[-3:])
        str_number = str_number[:-3]
    formatted_number = ','.join(reversed(parts))

    # 添加货币符号和负号（如果有）
    formatted_number = f'{sign} {formatted_number}'

    return formatted_number



def find_sum_combinations(arr: [float | int], target: float | int) -> [] | None:
    """
    找出数组中和为目标值的所有组合 ex: [1,3,5] and 8 -> [3,5]
    :param arr: 需要查找的数组
    :param target: 目标值
    :return:
    """

    def find_sum_combinations_base(arr, n, y):
        arr.sort()  # 对数组进行排序，以便按顺序选择元素
        result = []
        current_combination = []
        current_sum = 0
        start_index = 0

        def backtrack(start_index, current_sum):
            nonlocal result, current_combination

            if current_sum == y and len(current_combination) == n:
                result.append(current_combination[:])
                return

            for i in range(start_index, len(arr)):
                if current_sum + arr[i] > y:  # 当前和已经超过目标和，剪枝
                    break

                if len(current_combination) < n:
                    current_combination.append(arr[i])
                    current_sum += arr[i]
                    backtrack(i + 1, current_sum)
                    current_combination.pop()
                    current_sum -= arr[i]

        backtrack(start_index, current_sum)
        return result

    for i in range(1, len(arr)):
        result = find_sum_combinations_base(arr, i, target)
        if result:
            # print(f"找到了{n}个数的和为{y}的组合：")
            for combination in result:
                print(combination)