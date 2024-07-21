import pandas as pd
import os
import tkinter as tk
import numpy as np
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

# 엑셀 데이터를 읽어온다
def read_excel_data(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if (file_extension.find("csv")):
        return pd.read_csv(file_path)
    else:
        return pd.read_excel(file_path)

# 엑셀 데이터를 읽어서 property로 변환한다.
def get_excel_value_to_property():
    unreal_property_option = "UPROPERTY(BlueprintReadOnly, VisibleAnywhere)"
    all_excel_value_to_property = ""
    for i in range(excel_data.shape[0]):
        for j in range(excel_data.shape[1]):
            all_excel_value_to_property += f"\t{unreal_property_option}\n"
            key = excel_data.columns[j]
            value = excel_data.iloc[i, j]
            value_type = type(value)
            # 타입 확인
            if value_type ==  int:
                all_excel_value_to_property += f"\tint32 {key} = 0;\n"
            if value_type ==  np.int64:
                all_excel_value_to_property += f"\tint64 {key} = 0;\n"
            elif value_type ==  float:
                all_excel_value_to_property += f"\tfloat {key} = 0.0f;\n"
            elif value_type ==  str:
                all_excel_value_to_property += f"\tFString {key} = \"\";\n"
            elif value_type ==  bool:
                all_excel_value_to_property += f"\tbool {key} = false;\n"
    #마지막 개행 제거
    all_excel_value_to_property = all_excel_value_to_property[:-1]
    return all_excel_value_to_property

# Header file의 본문을 얻어온다.
def get_header_body(file_name, excel_file_name):
    all_excel_value_to_property = get_excel_value_to_property()
    class_body = (
f"""#pragma once
#include "CoreMinimal.h"
#include "DataAssets/DDDataAsset_DataAssetBase.h"
#include "{file_name}.generated.h"

USTRUCT(BlueprintType)
struct F{excel_file_name}
{{
    GENERATED_BODY()
    
public:
{all_excel_value_to_property}
}};

UCLASS()
class PROJECTDD_API U{file_name} : public UDDDataAsset_DataAssetBase
{{
    GENERATED_BODY()

public:
    U{file_name}();
    
    UPROPERTY(BlueprintReadOnly, VisibleAnywhere)
    TMap<int64/*ItemUID*/, F{excel_file_name}> Values;
}};
""")
    return class_body
def get_cpp_body(class_h_file, file_name):
    cpp_body = (
f"""#include "{class_h_file}"

U{file_name}::U{file_name}()
{{
        
}}
""")
    return cpp_body

# 엑셀 데이터를 읽어서 DataAsset Class를 생성.
def create_class(class_path):
    excel_file_name = os.path.splitext(os.path.basename(excel_file_path))[0]
    file_name = "DDDataAsset_" + excel_file_name
    class_cpp_file = f"{class_path}/{file_name}.cpp"
    class_h_file = f"{class_path}/{file_name}.h"
    header_body = get_header_body(file_name, excel_file_name)
    cpp_body = get_cpp_body(class_h_file, file_name)
    cpp_file = open(class_cpp_file, 'w')
    h_file = open(class_h_file, 'w')
    h_file.write(header_body)
    cpp_file.write(cpp_body)
    return file_name

# Main
print("읽어들일 엑셀 파일을 선택하세요.")
excel_file_path = select_file()
file_name = ""
class_path = "C:/UnrealProject/Dev/ProjectDD/Source/ProjectDD/DataAssets"
if excel_file_path:
    excel_data = read_excel_data(excel_file_path)
    file_name = create_class(class_path)
    print("완료되었습니다.")
else:
    print("파일을 선택하지 않았습니다.")