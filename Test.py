import pandas as pd
import unreal
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()  # Tkinter 창을 숨깁니다.
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    return file_path

def read_excel_data(file_path):
    df = pd.read_excel(file_path)
    return df

def create_class(excel_data):
    print()
    
# DataAsset 생성 함수
def create_data_asset(asset_name, asset_path, asset_class, excel_data):
    # Unreal Engine에서 사용할 에셋 도구를 가져옵니다.
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # DataAssetFactory를 생성합니다.
    factory = unreal.DataAssetFactory()

    # 새로운 DataAsset을 생성합니다.
    data_asset = asset_tools.create_asset(
        asset_name,
        asset_path,
        asset_class,
        factory
    )

    # 생성된 DataAsset의 DataArray에 데이터를 추가합니다.
    if data_asset:
        data_array = data_asset.get_editor_property("DataArray")
        for index, row in excel_data.iterrows():
            my_data = unreal.FMyData()
            my_data.name = row['Name']  # 'Name' 컬럼에 맞게 변경
            my_data.value = int(row['Value'])  # 'Value' 컬럼에 맞게 변경
            data_array.append(my_data)
        data_asset.set_editor_property("DataArray", data_array)

        # DataAsset 저장
        unreal.EditorAssetLibrary.save_loaded_asset(data_asset)
        print("DataAsset 생성 완료:", data_asset.get_path_name())
    else:
        print("DataAsset 생성 실패")

asset_name = "TestAsset"
asset_path = "/Game/Temp"
asset_class = unreal.load_class(None, "/Script/ProjectCR/Data/DataAsset.UCRJsonAsset")

# 파일 선택 창을 띄워 엑셀 파일을 선택합니다.
excel_file_path = select_file()
if excel_file_path:
    # 엑셀 데이터를 읽습니다.
    excel_data = read_excel_data(excel_file_path)

    # DataAsset을 생성하고 데이터를 설정합니다.
    create_data_asset(asset_name, asset_path, asset_class, excel_data)
else:
    print("파일을 선택하지 않았습니다.")