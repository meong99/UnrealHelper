import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

#
test_struct = getattr(unreal, f"{struct_name}")
attributes = dir(test_struct)
# 속성 이름과 값을 출력합니다.
for attr_name in attributes:
    # 내장된 속성/메서드 등을 제외하기 위해 필터링합니다.
    if not attr_name.startswith('__') and not callable(getattr(test_struct, attr_name)):
        attr_value = getattr(test_struct, attr_name)
        print(f"{attr_name}: {attr_value}")
#
