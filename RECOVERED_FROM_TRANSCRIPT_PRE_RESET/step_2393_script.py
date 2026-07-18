import sys
file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

index = content.find("fig_2_2_combined.update_yaxes(")
if index != -1:
    print(content[index:index+500])