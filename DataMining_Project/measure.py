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
    for gt in groundtruth:
        gt_id += 1
        for output_data in result_list:
            key = list(output_data.keys())[0]
            union = gt | output_data[key]

            if union == gt:
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

        intersection = groundtruth[key_index] & merge_data
        data_measure = len(intersection) / len(groundtruth[key_index])

        tmp = list()
        tmp.append(data_measure)
        tmp.append(merge_data.copy())

        compare_list.append(tmp)

    len_num = range(len(measure_dict))

    compare_list = merge_key_with_list(measure_dict, compare_list)
    compare_list.sort(reverse=True)
    for res_d in compare_list:
        file.write(f"{res_d[0]}\n")
        file.write(f"MG({len(res_d[1])}) : {res_d[1]}\n")
        file.write(f"GT({len(groundtruth[res_d[2]])}) : {groundtruth[res_d[2]]}\n")
        file.write(f"****\n")

def merge_key_with_list(measure_dict, compare_list):
    keys = list(measure_dict.keys())

    for i, data in enumerate(compare_list):
        data.append(keys[i])

    return compare_list


def output_to_file_by_lv(filename, f_measure_list, level_list):
    file = open(filename, 'w')
    none_conn = list()

    for i, data in enumerate(f_measure_list):
        if data[0] == 0:
            none_conn.append(data)
        else:
            file.write("*"*20)
            file.write(f"\nLv : {level_list[i]} | Score : {data[0]}\n")
            file.write(f"DA({len(data[1])}) : {data[1]}\n")
            file.write(f"GT({len(data[2])}) : {data[2]}\n")

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

    for data in f_measure_list:
        if data[0] == 0:
            none_conn.append(data)
        else:
            file.write("*"*20)
            file.write(f"\nLv : {data[-1]} | Score : {data[0]}\n")
            file.write(f"DA({len(data[1])}) : {data[1]}\n")
            file.write(f"GT({len(data[2])}) : {data[2]}\n")

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