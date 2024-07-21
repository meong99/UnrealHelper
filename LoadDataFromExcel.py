import pandas as pd
import unreal
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import re
import sys

def convert_to_python_name(ue_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', ue_name)
    python_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return python_name

def convert_to_unreal_compatible(value):
    if isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, np.floating):
        return float(value)
    elif isinstance(value, np.int64):
        return unreal.Int64Property()
    elif isinstance(value, str):
        return f"{value}"
    return value
# 파일을 선택한다
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls *.csv")]
    )
    return file_path

# 엑셀 데이터를 읽어온다
def read_excel_data(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if (file_extension.find("csv")):
        return pd.read_csv(file_path)
    else:
        return pd.read_excel(file_path)

def set_asset_data_from_excel():
    data_map = {}
    for i in range(excel_data.shape[0]):
        struct_type = getattr(unreal, f"{struct_name}")
        struct_instance = struct_type()
        for j in range(excel_data.shape[1]):
            key = excel_data.columns[j]
            value = excel_data.iloc[i, j]
            setattr(struct_instance, convert_to_python_name(key), convert_to_unreal_compatible(value))
        data_map[convert_to_unreal_compatible(excel_data.iloc[i][0])] = struct_instance
    setattr(loaded_asset, "values", data_map)

# 에셋 경로와 이름을 정의합니다.
excel_file_path = select_file()
excel_data = read_excel_data(excel_file_path)
asset_path = "/Game/Datas"
asset_name = "DDDataAsset_" + os.path.splitext(os.path.basename(excel_file_path))[0]
struct_name = os.path.splitext(os.path.basename(excel_file_path))[0]

# 팩토리 클래스를 사용하여 PrimaryDataAsset 인스턴스를 생성합니다.
loaded_asset = unreal.load_asset(f"{asset_path}/{asset_name}.{asset_name}")
if loaded_asset is None:
    print(f"에셋을 가져올 수 없습니다. {asset_path}에 {asset_name}이 있는지 확인하세요")
    sys.exit(0)

set_asset_data_from_excel()

# 생성된 PrimaryDataAsset 인스턴스에 데이터를 설정합니다.
if loaded_asset:
    unreal.EditorAssetLibrary.save_loaded_asset(loaded_asset)
    print(f"PrimaryDataAsset Changed at {asset_path}/{asset_name}")