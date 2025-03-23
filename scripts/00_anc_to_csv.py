import csv
import os


def anc_to_csv(anc_file_path, csv_file_path):
    try:
        # 打开 .anc 文件进行读取
        with open(anc_file_path, 'r', encoding='utf-8') as anc_file:
            # 逐行读取 .anc 文件内容
            lines = anc_file.readlines()

        # 解析 .anc 文件内容
        data = []
        for line in lines:
            # 按空格分割每行数据
            row = line.strip().split()
            data.append(row)

        # 查找包含 'Name' 的行索引
        name_row_index = None
        for i, row in enumerate(data):
            if 'Name' in row:
                name_row_index = i
                break

        if name_row_index is not None:
            # 删除 Name 所在行上面的所有行
            data = data[name_row_index:]
            # 删除 Name 所在行下面的 2 行
            if len(data) > 3:
                data = data[:1] + data[3:]

        # 打开 .csv 文件进行写入
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # 写入数据到 CSV 文件
            writer.writerows(data)

        print(f"成功将 {anc_file_path} 转换为 {csv_file_path}")
    except FileNotFoundError:
        print(f"错误: 未找到 {anc_file_path} 文件。")
    except Exception as e:
        print(f"发生未知错误: {e}")


def convert_all_anc_files(anc_folder_path):
    # 创建 csv 文件夹
    csv_folder = os.path.join(anc_folder_path, 'csv')
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # 遍历指定路径下的所有文件
    for root, dirs, files in os.walk(anc_folder_path):
        for file in files:
            if file.endswith('.anc'):
                anc_file_path = os.path.join(root, file)
                # 生成对应的 csv 文件路径
                csv_file_name = os.path.splitext(file)[0] + '.csv'
                csv_file_path = os.path.join(csv_folder, csv_file_name)
                anc_to_csv(anc_file_path, csv_file_path)


if __name__ == "__main__":
    anc_folder_path = r'D:\code\muscle_analysis\data\20250320_EMG'  # 替换为实际的 .anc 文件所在文件夹路径
    convert_all_anc_files(anc_folder_path)
    