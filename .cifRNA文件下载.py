import requests  
import gzip  
import os  
from concurrent.futures import ThreadPoolExecutor  
  
# 读取.txt文件，获取所有的RNA文件名（假设它们由逗号隔开）  
with open('.txt', 'r') as f:  
    rna_names_str = f.read().strip()  # 读取整个文件内容为一个字符串  
    rna_names = rna_names_str.split(',')  # 按逗号分割字符串，得到RNA名称列表  
  
# 设置基础URL  
base_download_url = "https://files.rcsb.org/download/"  
  
# 创建保存文件的目录  
save_dir = 'downloaded_RNA.cif'  
if not os.path.exists(save_dir):  
    os.makedirs(save_dir) 
  
def download_and_extract(rna_name, file_count):  
    # 构建完整的文件名和URL  
    file_name = f"{rna_name}.cif.gz"  
    url = f"{base_download_url}{file_name}"  
      
    try:  
        # 发送HTTP请求，下载文件  
        response = requests.get(url)  
          
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 保存下载的.cif.gz文件  
            gz_path = os.path.join(save_dir, file_name)  
            with open(gz_path, 'wb') as f:  
                f.write(response.content)  
           
              
            print(f"第 {file_count}个文件: {rna_name}.cif.gz 下载成功.")  
        else:  
            print(f"第 {file_count}个文件: {rna_name}.cif.gz 下载失败，状态码: {response.status_code}")  
    except Exception as e:  
        print(f"第 {file_count}个文件: {rna_name}. 下载时出错 Error: {e}")  
  
# 使用ThreadPoolExecutor同时下载文件  
with ThreadPoolExecutor(max_workers=10) as executor:  
    futures = []  
    for file_count, rna_name in enumerate(rna_names, start=1):  
        future = executor.submit(download_and_extract, rna_name, file_count)  
        futures.append(future)  
  
    # 等待所有下载任务完成  
    for future in futures:  
        future.result()  # 这会抛出任何在任务执行期间发生的异常