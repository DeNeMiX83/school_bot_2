def merge(left_list, right_list):
    sorted_list = []
    left_index = right_index = 0
    len_left, len_right = len(left_list), len(right_list)
    for _ in range(len_left + len_right):
        if left_index < len_left and right_index < len_right:
            if left_list[left_index] < right_list[right_index]:
                sorted_list.append(left_list[left_index])
                left_index += 1
            else:
                sorted_list.append(right_list[right_index])
                right_index += 1
        elif left_index == len_left:
            sorted_list.append(right_list[right_index])
            right_index += 1
        elif right_index == len_right:
            sorted_list.append(left_list[left_index])
            left_index += 1
    return sorted_list


def merge_sort(num):
    if len(num) <= 1:
        return num
    k = len(num) // 2
    left_list = merge_sort(num[:k])
    right_list = merge_sort(num[k:])
    return merge(left_list, right_list)


num = [1, 6, 7, 9, 3, 4, 5]
print(merge_sort(num))
