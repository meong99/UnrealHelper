import unreal
import os
import tkinter as tk
from tkinter import filedialog

# 파일을 선택한다
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls *.csv")]
    )
    return file_path


# 에셋 경로와 이름을 정의합니다.
excel_file_path = select_file()
asset_path = "/Game/Datas"
asset_name = "DataAsset_" + os.path.splitext(os.path.basename(excel_file_path))[0]

# 팩토리 클래스를 사용하여 PrimaryDataAsset 인스턴스를 생성합니다.
factory = unreal.DataAssetFactory()
new_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, asset_path, getattr(unreal, f"{asset_name}"), factory)

# 생성된 PrimaryDataAsset 인스턴스에 데이터를 설정합니다.
if new_asset:
    unreal.EditorAssetLibrary.save_loaded_asset(new_asset)
    print(f"PrimaryDataAsset created at {asset_path}/{asset_name}")
else:
    print("Failed to create PrimaryDataAsset")