import requests
import re
import os
from tqdm import tqdm
import subprocess  # 新增导入

def get_bvid_from_url(url):
    """
    从B站视频URL中提取BV号（B站视频的唯一标识）
    参数:
        url (str): B站视频页面的完整URL（如 https://www.bilibili.com/video/BV123456789）
    返回:
        str/None: 提取到的BV号（格式为BV+10位字母数字组合），若未匹配到则返回None
    """
    # 正则匹配BV号（B站URL中BV号格式固定为BV开头+10位字符）
    bvid_match = re.search(r"BV[\w]{10}", url)
    if not bvid_match:
        print(f"警告：未从URL '{url}' 中匹配到有效的BV号（格式应为BV+10位字母数字）")  # 新增明确提示
    return bvid_match.group() if bvid_match else None

def get_video_info(bvid):
    """获取视频基础信息"""
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        data = response.json()
        
        if data["code"] != 0:
            return {"error": data["message"]}
            
        return {
            "title": data["data"]["title"],
            "up_name": data["data"]["owner"]["name"],
            "view": data["data"]["stat"]["view"],
            "danmaku": data["data"]["stat"]["danmaku"],
            "duration": data["data"]["duration"]  # 单位：秒
        }
    except Exception as e:
        return {"error": f"获取信息失败: {str(e)}"}

def download_video(bvid, save_path="."):
    """
    实现真实视频下载功能（需先安装you-get）
    参数:
        bvid (str): 视频BV号
        save_path (str): 保存目录路径
    """
    video_info = get_video_info(bvid)
    if "error" in video_info:
        print(f"下载失败: {video_info['error']}")
        return
    
    try:
        # 创建保存目录（如果不存在）
        os.makedirs(save_path, exist_ok=True)
        
        # 调用you-get下载
        subprocess.run([
            "D:\\python\\Scripts\\you-get.exe",  # 使用完整路径
            "-o", save_path,
            f"https://www.bilibili.com/video/{bvid}"
        ], check=True)
        
        print(f"视频下载完成，保存至: {os.path.abspath(save_path)}")
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {e}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    # 替换为您提供的视频链接
    target_url = "https://www.bilibili.com/video/BV1GEVxzVEWN?spm_id_from=333.788.recommend_more_video.1&vd_source=33c5e956aa342acc667ebf2736eb5a17"
    bvid = get_bvid_from_url(target_url)
    
    if not bvid:
        print("错误：无效的B站视频链接")
    else:
        info = get_video_info(bvid)
        if "error" in info:
            print(f"信息获取失败: {info['error']}")
        else:
            print("视频信息:")
            print(f"标题: {info['title']}")
            print(f"UP主: {info['up_name']}")
            print(f"播放量: {info['view']}")
            # 取消下面这行的注释以启用下载
            download_video(bvid, "e:\\hhggg\\downloads")