import os
import json
from collections import defaultdict

def generate_db_json():
    # 定义路径
    icon_dir = "./public/icon"
    output_file = "./public/db.json"
    
    # 创建数据结构
    category_data = defaultdict(list)
    
    # 遍历icon目录下的所有分类文件夹
    for category in os.listdir(icon_dir):
        category_path = os.path.join(icon_dir, category)
        
        # 确保是目录
        if not os.path.isdir(category_path):
            continue
            
        # 遍历分类目录中的所有文件
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            
            # 跳过目录
            if os.path.isdir(file_path):
                continue
                
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            
            # 跳过没有扩展名的文件和隐藏文件
            if not ext or name.startswith('.'):
                continue
                
            # 添加到数据结构
            category_data[category].append({
                "name": name,
                "type": ext[1:].lower(),  # 去掉点并转小写
                "course": ""
            })
    
    # 转换为标准字典
    result = dict(category_data)
    
    # 写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"成功生成 {output_file}，包含 {len(result)} 个分类")

if __name__ == "__main__":
    generate_db_json()