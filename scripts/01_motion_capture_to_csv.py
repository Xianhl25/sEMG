import os
import csv
import glob

# 指定输入和输出路径
input_folder = r'D:\code\muscle_analysis\data\20250321_MC_EMG\input'   # 存放 txt 和 anc 文件的文件夹路径
output_folder = r'D:\code\muscle_analysis\data\20250321_MC_EMG\output'  # 处理后的 csv 文件存放路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取所有 .txt 文件
txt_files = glob.glob(os.path.join(input_folder, '*.txt'))

for txt_file in txt_files:
    file_name = os.path.splitext(os.path.basename(txt_file))[0]  # 获取文件名（无扩展名）
    anc_file = os.path.join(input_folder, file_name + '.anc')  # 对应的 .anc 文件路径

    # 检查 .anc 文件是否存在
    if not os.path.exists(anc_file):
        print(f"⚠️ Warning: No matching .anc file for {txt_file}, skipping...")
        continue

    # 读取 anc 文件，获取总时间 T
    T = None
    with open(anc_file, 'r', encoding='utf-8') as ancfile:
        reader = list(csv.reader(ancfile, delimiter='\t'))  # 读取 .anc 文件
        if reader:
            T = float(reader[-1][0])  # 最后一行第一列的值即为 T
            print(f"✅ Found T = {T} from {anc_file}")

    print(f"📂 Processing: {txt_file}")

    # 读取 txt 文件内容
    with open(txt_file, 'r', encoding='utf-8') as txtfile:
        # 自动检测分隔符（默认使用制表符 '\t'，否则使用逗号 ',')
        first_line = txtfile.readline()
        delimiter = '\t' if '\t' in first_line else ','
        txtfile.seek(0)  # 重新回到文件开头
        
        # 读取数据
        reader = list(csv.reader(txtfile, delimiter=delimiter))

    # 查找 "Left Ankle Angle" 行的索引 A
    target_row_idx = -1
    for row_num, row in enumerate(reader):
        if any(cell.strip() == 'Left Ankle Angle' for cell in row):
            target_row_idx = row_num
            print(f"🔍 Found 'Left Ankle Angle' at row {row_num + 1}: {row}")
            break

    # 仅在找到目标行时进行处理
    if target_row_idx != -1:
        # 计算要删除的行索引（B = A-1, C = A+1, D = A+2），**保留 A**
        indices_to_delete = {target_row_idx - 1, target_row_idx + 1, target_row_idx + 2}
        indices_to_delete = {i for i in indices_to_delete if 0 <= i < len(reader)}  # 过滤有效索引

        # 过滤数据，删除 B, C, D 行，但保留 A
        filtered_data = [row for idx, row in enumerate(reader) if idx not in indices_to_delete]

        # **确保 "Left Ankle Angle" 行不会被删除，即使有空单元格**
        clean_data = []
        for idx, row in enumerate(filtered_data):
            if idx == target_row_idx-1 or all(cell.strip() != '' for cell in row):  
                clean_data.append(row)

        # 找到 ITEM 列的索引
        item_col_idx = -1
        print("col 0:", clean_data[1])
        if clean_data:
            for col_idx, value in enumerate(clean_data[1]):
                if value.strip().upper() == 'ITEM':
                    item_col_idx = col_idx
                    clean_data[1][col_idx] = 'Time(s)'  # 修改列名
                    break

        # 处理 ITEM 列的时间转换
        if item_col_idx != -1 and T is not None:
            try:
                tmax = float(clean_data[-1][item_col_idx])  # ITEM 列的最大值（最后一行该列的值）
                print(f"⏳ Max ITEM value (tmax): {tmax}")
                for row in clean_data[2:]:  # 跳过表头行
                    row[item_col_idx] = str(T * float(row[item_col_idx]) / tmax)  # 替换 ITEM 列的值
            except ValueError as e:
                print(f"❌ Error processing ITEM column: {e}")

        # 生成输出文件路径（改为 .csv 格式）
        output_file = os.path.join(output_folder, file_name + '.csv')

        # 保存到 CSV 文件
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(clean_data)

        print(f"✅ Processed file saved to: {output_file}\n")
    else:
        print(f"⚠️ No row containing 'Left Ankle Angle' found in {txt_file}\n")

print("🎉 All TXT files have been processed successfully!")
