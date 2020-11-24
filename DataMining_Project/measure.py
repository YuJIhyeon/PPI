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
    f_measure_list, level_list = f_measure(result_list, groundtruth)

    # 결과 값 출력 ------------
    output1_filename = 'f_measure_by_lv.txt'
    output2_filename = 'f_measure_by_score.txt'
    output_to_file_by_lv(output1_filename, f_measure_list, level_list)
    output_to_file_by_score(output2_filename, f_measure_list, level_list)


if __name__ == '__main__':
    main()