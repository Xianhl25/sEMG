import os
import pandas as pd

def process_csv_file(input_file, output_folder):
    """
    处理单个CSV文件，删除前5行，删除特定列，去除末尾非数字行。
    """
    data_df = pd.read_csv(input_file, low_memory=False, header=5) # 直接以第六行作为列名

    colums_to_drop = ['X [Percent].1', 'X [Percent].2', 'X []', 'X [].1', 'Trigno sensor 3: EMG 3->filter (FilterSlidingRMS63)->Captured Data []']
    data_df = data_df.drop(columns=colums_to_drop)

    # 修改剩余列的列名
    new_column_names = {
        'X [Percent]': 'X',
        'Trigno sensor 3: EMG 3->filter (FilterSlidingRMS63)->Mean [Volts]': 'Mean',
        'Trigno sensor 3: EMG 3->filter (FilterSlidingRMS63)->Mean + Std Dev [Volts]': 'Mean + Std Dev',
        'Trigno sensor 3: EMG 3->filter (FilterSlidingRMS63)->Mean - Std Dev [Volts]': 'Mean - Std Dev',
        'Trigno sensor 3: EMG 3->filter (FilterSlidingRMS63)->Std Dev [Volts]': 'Std Dev'
    }
    data_df = data_df.rename(columns=new_column_names)

    # 检查是否存在非数字的情况，并删除包含非数字值的行
    data_df = data_df.apply(pd.to_numeric, errors='coerce')  # 将非数字值转换为 NaN
    data_df = data_df.dropna()  # 删除包含 NaN 的行

    output_file = os.path.join(output_folder, os.path.basename(input_file))
    data_df.to_csv(output_file, index=False)

def batch_process_csv_files(input_folder):
    """
    批量处理指定文件夹中的所有CSV文件。
    """
    output_folder = os.path.join(input_folder, "processed")

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            print(f"正在处理: {file_path}")
            process_csv_file(file_path, output_folder)

if __name__ == "__main__":
    input_folder = r"D:\GitHub\sEMG\data"  # 请修改为你的Excel文件所在的文件夹路径
    batch_process_csv_files(input_folder)