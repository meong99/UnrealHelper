import subprocess

result = subprocess.run(['python', 'C:/Users/USER/Desktop/MyGit/CreateDataAssetClass.py'])

output_file = open("C:/Users/USER/Desktop/MyGit/Output.txt", 'r')
output_body = output_file.read()
if not output_body.__contains__('fail'):
    print(output_body)
else:
    print("DataAsset만들기에 실패했습니다.")