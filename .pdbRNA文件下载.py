import requests  
import gzip  
import os  
from concurrent.futures import ThreadPoolExecutor  
from tenacity import retry, stop_after_attempt, wait_fixed  
  
# 读取.txt文件，获取所有的RNA文件名（假设它们由逗号隔开）  
with open('PDB中的全部RNA文件名称.txt', 'r') as f:  
    rna_names_str = f.read().strip()  # 读取整个文件内容为一个字符串  
    rna_names = rna_names_str.split(',')  # 按逗号分割字符串，得到RNA名称列表  
  
# 设置基础URL  
base_download_url = "https://download.rcsb.org/batch/structures/"  
  
# 创建保存文件的目录  
save_dir = 'downloaded_RNA.PDB'  
if not os.path.exists(save_dir):  
    os.makedirs(save_dir)  
  
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))  #最多尝试5次，每次重试之间等待2秒
def download_file(url, path):  
    try:  
        response = requests.get(url)  
        response.raise_for_status()  # 如果状态码不是200，将抛出HTTPError  
        with open(path, 'wb') as f:  
            f.write(response.content)  
    except requests.RequestException as e:  
        raise Exception(f"下载失败: {e}")  
  
def download_and_extract(rna_name, file_count):  
    # 构建完整的文件名和URL  
    file_name = f"{rna_name}.pdb"  
    url = f"{base_download_url}{file_name}"  
    gz_path = os.path.join(save_dir, file_name)  
  
    try:  
        # 尝试下载文件，带有重试机制  
        download_file(url, gz_path)  
        print(f"第 {file_count}个文件: {rna_name}.pdb 下载成功.")  
    except Exception as e:  
        print(f"第 {file_count}个文件: {rna_name}.pdb 下载失败 Error: {e}")  
  
# 使用ThreadPoolExecutor同时下载文件  
with ThreadPoolExecutor(max_workers=10) as executor:  
    futures = []  
    for file_count, rna_name in enumerate(rna_names, start=1):  
        future = executor.submit(download_and_extract, rna_name, file_count)  
        futures.append(future)  
  
    # 等待所有下载任务完成  
    for future in futures:  
        future.result()  # 这会抛出任何在任务执行期间发生的异常