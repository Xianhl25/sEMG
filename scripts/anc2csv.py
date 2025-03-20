import os
import csv
import glob

"""
用于处理Cortex导出的 .anc 文件，将其转换为 .csv 格式
"""

# 指定输入和输出路径
input_folder = r'D:\code\muscle_analysis\data\20250320_EMG'    # 替换为 .anc 文件所在的文件夹路径
output_folder = os.path.join(input_folder, 'csv')

# 如果输出文件夹不存在，创建它
os.makedirs(output_folder, exist_ok=True)

# * 遍历所有 .anc 文件
anc_files = glob.glob(os.path.join(input_folder, '*.anc'))

for file_path in anc_files:
    print(f"Processing: {file_path}")
    
    # * 读取文件内容
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile, delimiter='\t'))  # ✅ 使用 '\t' 作为分隔符
    
    # * 找到包含 "Name" 的行号
    name_row_idx = -1
    for row_num, row in enumerate(reader):
        if any(cell.strip() == 'Name' for cell in row):
            name_row_idx = row_num
            print(f"Row containing 'Name' found at row {row_num + 1}: {row}")
            break

    if name_row_idx != -1:
        # ✅ 保留 "Name" 行，但删除其上方的行和下方的两行
        data = reader[name_row_idx:]  # 保留从 "Name" 行开始的所有行
        data = [data[0]] + data[3:]  # 删除 "Name" 行之后的 2 行

        # ✅ 查找 "Name" 行中空单元格的索引
        empty_cells = [i for i, cell in enumerate(reader[name_row_idx]) if cell.strip() == '']
        print(f"Empty cells at columns: {empty_cells}")

        # ✅ 删除空单元格所在的列（在所有行中删除）
        if empty_cells:
            for i in sorted(empty_cells, reverse=True):  # 逆序删除，防止索引错位
                for row in data:
                    del row[i]

        # ✅ 生成输出文件路径（改为 .csv 格式）
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.csv')

        # ✅ 将结果写入到新的 .csv 文件中
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        print(f"Processed file saved to: {output_file}\n")
    else:
        print(f"No row containing 'Name' found in {file_path}\n")

print("All files processed successfully!")
