import numpy as np
def initial_data(filename):
    result_list = list()
    tmp_dict = dict()
    input_file = open(filename, 'r')
    for line in input_file:
        data_line = line.split()
        data_line.pop(1)
        tmp_dict[data_line[0]] = set(data_line[1:])
        result_list.append(tmp_dict.copy())
        tmp_dict.clear()

    return result_list

def read_groundtruth(filename):
    data_group = set()
    data = list()
    with open(filename) as file:
        for row in file:
            for i in row.split():
                data_group.add(i)
            data.append(data_group.copy())
            data_group.clear()

    return data

def f_measure(result_list, groundtruth):
    f_measure_list = list()
    level_list = list()

    for based_data in result_list:
        prev_f_mesure = [0, 0, 0]
        b_key = list(based_data.keys())[0]
        level_list.append(b_key)

        for gr_data in groundtruth:
            recall = len(based_data[b_key] & gr_data) / len(gr_data)
            precision = len(based_data[b_key] & gr_data) / len(based_data[b_key])

            if recall == 0 and precision == 0:
                prev_f_mesure[1] = based_data[b_key]
                continue

            t_f_measure = 2 * (recall * precision) / (recall + precision)
            t_f_measure = round(t_f_measure, 3)


            if prev_f_mesure[0] < t_f_measure:
                prev_f_mesure[0] = t_f_measure
                prev_f_mesure[1] = based_data[b_key]
                prev_f_mesure[2] = gr_data.copy()

        f_measure_list.append(prev_f_mesure.copy())

    return f_measure_list, level_list

def measure(result_list, groundtruth):
    measure_dict = dict()
    gt_id = -1
    threshold = 3
    for gt in groundtruth:
        gt_id += 1
        for output_data in result_list:
            key = list(output_data.keys())[0]
            union = gt | output_data[key]

            if len(union) - len(gt) <= threshold :
                if measure_dict.get(gt_id) == None:
                    measure_dict[gt_id] = list()
                    measure_dict[gt_id].append(output_data[key])
                else:
                    measure_dict[gt_id].append(output_data[key])

    return measure_dict

def output_to_merge_with_gt(filename, measure_dict, groundtruth):
    file = open(filename, 'w')

    compare_list = list()
    for key_index in measure_dict.keys():
        merge_data = set()
        for cluster_list in measure_dict[key_index]:
            for data in cluster_list:
                merge_data.add(data)

        data_measure = round(len(merge_data & groundtruth[key_index]) / len(groundtruth[key_index]), 3)
        sub_num = abs(len(merge_data) - len(groundtruth[key_index]))

        tmp = list()
        tmp.append(data_measure)
        tmp.append(sub_num)
        tmp.append(merge_data.copy())

        compare_list.append(tmp)

    compare_list = merge_key_with_list(measure_dict, compare_list)
    compare_list.sort(reverse=True)
    err_table = 0
    result_table = np.zeros((3,4))
    for res_d in compare_list:
        if res_d[0] == 1:
            if res_d[1] == 0:
                result_table[0][0] += 1
            elif res_d[1] <= 3:
                result_table[1][0] += 1
            elif res_d[1] <= 6:
                result_table[2][0] += 1
            else:
                err_table += 1
        elif res_d[0] > 0.7:
            if res_d[1] == 0:
                result_table[0][1] += 1
            elif res_d[1] <= 3:
                result_table[1][1] += 1
            elif res_d[1] <= 6:
                result_table[2][1] += 1
            else:
                err_table += 1
        elif res_d[0] > 0.4:
            if res_d[1] == 0:
                result_table[0][2] += 1
            elif res_d[1] <= 3:
                result_table[1][2] += 1
            elif res_d[1] <= 6:
                result_table[2][2] += 1
            else:
                err_table += 1
        elif res_d[0] > 0.0:
            if res_d[1] == 0:
                result_table[0][3] += 1
            elif res_d[1] <= 3:
                result_table[1][3] += 1
            elif res_d[1] <= 6:
                result_table[2][3] += 1
            else:
                err_table += 1
        else:
            err_table += 1

        file.write(f"{res_d[0]}, {res_d[1]}\n")
        file.write(f"MG({len(res_d[2])}) : {res_d[2]}\n")
        file.write(f"GT({len(groundtruth[res_d[3]])}) : {groundtruth[res_d[3]]}\n")
        file.write(f"****\n")

    index = ['0 ~ 0', '1 ~ 3', '4 ~ 6']
    file.write(f"       [ 1 | ~ 0.7 | ~ 0.4 | ~ 0 ]\n")
    for i, row in enumerate(result_table):
        file.write(f"{index[i]} :\t")
        for j in row:
            file.write(f"{int(j):3}    ")
        file.write("\n")

    file.write(f"Total : {len(compare_list)}\n")
    file.write(f"Valid : {len(compare_list) - err_table}, Unvalid : {err_table}\n")
    file.write(f"Total ratio : {round(len(compare_list) / 734, 3)}\n")
    file.write(f"Valid ratio : {round((len(compare_list) - err_table) / len(compare_list), 3)}\n")


def merge_key_with_list(measure_dict, compare_list):
    keys = list(measure_dict.keys())

    for i, data in enumerate(compare_list):
        data.append(keys[i])

    return compare_list


def output_to_file_by_lv(filename, f_measure_list, level_list):
    file = open(filename, 'w')
    none_conn = list()
    unique_lv = list()
    unique_value = set(level_list)
    sum_list = dict()

    for val in unique_value:
        unique_lv.append(int(val))
    unique_lv.sort()

    for i, data in enumerate(f_measure_list):
        if data[0] == 0:
            none_conn.append(data)
        else:
            if sum_list.get(level_list[i]) == None:
                sum_list[level_list[i]] = data[0]
            else:
                sum_list[level_list[i]] += data[0]

            file.write("*" * 20)
            file.write(f"\nLv : {level_list[i]} | Score : {data[0]}\n")
            file.write(f"DA({len(data[1])}) : {data[1]}\n")
            file.write(f"GT({len(data[2])}) : {data[2]}\n")


    file.write("*" * 20)
    file.write("\n")

    file.write(f"Total : {len(level_list)}, Lv_cnt : {len(unique_lv)}\n")
    file.write("lv : count\n")
    for i in range(len(unique_lv)):
        data_count = level_list.count(str(unique_lv[i]))
        file.write(f"{unique_lv[i]} : {data_count}\n")

    file.write("*" * 20)
    file.write("\n")
    file.write("Not include data from ground_truth\n")
    file.write("*" * 20)
    file.write("\n")
    for data in none_conn:
        file.write(f"Len : {len(data[1])} | {data[1]}\n")

def output_to_file_by_score(filename, f_measure_list, level_list):
    file = open(filename, 'w')
    none_conn = list()
    for i, data in enumerate(f_measure_list):
        data.append(level_list[i])

    f_measure_list.sort(reverse=True)
    range_dict = [0, 0, 0]

    for data in f_measure_list:
        if data[0] == 0:
            none_conn.append(data)
        else:
            if data[0] >= 0.7:
                range_dict[0] += 1
            elif data[0] >= 0.4:
                range_dict[1] += 1
            else:
                range_dict[2] += 1
            file.write("*" * 20)
            file.write(f"\nLv : {data[-1]} | Score : {data[0]}\n")
            file.write(f"DA({len(data[1])}) : {data[1]}\n")
            file.write(f"GT({len(data[2])}) : {data[2]}\n")

    file.write("***********\n")
    file.write("Score Range : Count\n")
    file.write(f"0.7 ~ 1.0 : {range_dict[0]}\n")
    file.write(f"0.4 ~ 0.7 : {range_dict[1]}\n")
    file.write(f"0.0 ~ 0.4 : {range_dict[2]}\n")

    file.write("*" * 20)
    file.write("\n")
    file.write("Not include data from ground_truth\n")
    file.write("*" * 20)
    file.write("\n")
    for data in none_conn:
        file.write(f"Len : {len(data[1])} | {data[1]}\n")

# The main function
def main():
    input_filename = 'result.txt'
    result_list = initial_data(input_filename)
    groundtruth = read_groundtruth('groundtruth.txt')
    measure_dict = measure(result_list, groundtruth)
    f_measure_list, level_list = f_measure(result_list, groundtruth)

    # 결과 값 출력 ------------
    output1_filename = 'f_measure_by_lv.txt'
    output2_filename = 'f_measure_by_score.txt'
    output_to_file_by_lv(output1_filename, f_measure_list, level_list)
    output_to_file_by_score(output2_filename, f_measure_list, level_list)

    output1_filename = 'measure_by_lv.txt'
    output2_filename = 'measure_by_score.txt'
    output_to_merge_with_gt(output1_filename, measure_dict, groundtruth)





if __name__ == '__main__':
    main()