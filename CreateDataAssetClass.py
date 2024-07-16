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
def get_header_body(file_name):
    all_excel_value_to_property = get_excel_value_to_property()
    class_body = (
f"""#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "{file_name}.generated.h"

UCLASS()
class PROJECTCR_API U{file_name} : public UDataAsset
{{
    GENERATED_BODY()

public:
{all_excel_value_to_property}
}};
""")
    return class_body
def get_cpp_body(class_h_file):
    cpp_body = (
f"""#include "{class_h_file}"
""")
    return cpp_body

# 엑셀 데이터를 읽어서 DataAsset Class를 생성.
def create_class(excel_data):
    file_name = "DataAsset_" + os.path.splitext(os.path.basename(excel_file_path))[0]
    class_cpp_file = f"./{file_name}.cpp"
    class_h_file = f"./{file_name}.h"
    header_body = get_header_body(file_name)
    cpp_body = get_cpp_body(class_h_file)
    cpp_file = open(class_cpp_file, 'w')
    h_file = open(class_h_file, 'w')
    h_file.write(header_body)
    cpp_file.write(cpp_body)
    return file_name

# Main
print("읽어들일 엑셀 파일을 선택하세요.")
excel_file_path = select_file()
file_name = ""
output_file = open("C:/Users/USER/Desktop/MyGit/Output.txt", 'w')
if excel_file_path:
    excel_data = read_excel_data(excel_file_path)
    file_name = create_class(excel_data)
    output_file.write(f"FileName={file_name}")
    print("완료되었습니다.")
else:
    output_file.write("Fail")
    print("파일을 선택하지 않았습니다.")