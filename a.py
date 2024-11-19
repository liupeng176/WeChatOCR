import wcocr
import os
import time
from colorama import init, Fore, Style

def find_wechat_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    common_paths = os.path.join(script_dir, 'path')
    if os.path.exists(common_paths):
        #print(f"找到WeChat路径: {common_paths}")
        return common_paths
    else:
        print(f"The path folder does not exist at {common_paths}.")
        return None

def find_wechatocr_exe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wechatocr_exe_path = os.path.join(script_dir, 'path', 'WeChatOCR', 'WeChatOCR.exe')
    if os.path.isfile(wechatocr_exe_path):
        return wechatocr_exe_path
    else:
        print(f"The WeChatOCR.exe does not exist at {wechatocr_exe_path}.")
        return None

def wechat_ocr(image_path):
    wechat_path = find_wechat_path()
    wechatocr_exe_path = find_wechatocr_exe()
    if not wechat_path or not wechatocr_exe_path:
        return []  # 返回空结果

    wcocr.init(wechatocr_exe_path, wechat_path)
    result = wcocr.ocr(image_path)
    texts = []

    for temp in result['ocr_response']:
        text = temp['text']
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
        texts.append(text)

    return texts

def save_to_txt(texts, output_path):
    """
    将识别出的文字内容保存到txt文件中
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for text in texts:
            f.write(text + '\n')

def process_all_images():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_folder = os.path.join(script_dir, 'src')
    txt_folder = os.path.join(script_dir, 'txt')

    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    # 支持的图像格式
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif')

    start_time_all = time.time()  # 记录开始处理所有图片的初始时间（精确到秒）

    # 遍历 src 文件夹及其所有子文件夹
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, src_folder)
                file_extension = os.path.splitext(file)[1].lower().lstrip('.')  # 获取文件扩展名（不含.）
                output_folder = os.path.join(txt_folder, file_extension)  # 根据扩展名构建输出目录
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # 处理图片文件前打印时间（精确到毫秒）
                start_time_single = time.time()
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time_single))
                millisecond = int((start_time_single % 1) * 1000)
                print(Fore.GREEN + f"开始处理 {os.path.relpath(image_path, script_dir)} 的时间为: {time_str}.{millisecond:03d}" + Style.RESET_ALL)

                texts = wechat_ocr(image_path)
                image_name = os.path.splitext(file)[0]
                output_txt = os.path.join(output_folder, f'{image_name}_OCR.txt')
                save_to_txt(texts, output_txt)
                # 显示相对路径
                relative_txt_path = os.path.relpath(output_txt, script_dir)
                print(f"OCR 结果:{texts}:已保存到: {relative_txt_path}")

                end_time_single = time.time()  # 记录处理完当前图片的时间
                cost_time_single = (end_time_single - start_time_single) * 1000  # 计算处理当前图片花费的时间（转换为毫秒）
                print(Fore.YELLOW + f"处理 {os.path.relpath(image_path, script_dir)} 花费时间: {cost_time_single:.2f} 毫秒\n" + Style.RESET_ALL)

    end_time_all = time.time()  # 记录处理完所有图片后的时间（精确到秒）
    cost_time_all = (end_time_all - start_time_all) * 1000  # 计算处理所有图片花费的总时间（转换到毫秒）
    print(Fore.BLUE + f"处理所有图片共花费时间: {cost_time_all:.2f} 毫秒" + Style.RESET_ALL)

if __name__ == '__main__':
    init(autoreset=True)  # 初始化colorama
    process_all_images()
    print(Fore.RED + "全部文件处理完成，请按 Enter 键退出……" + Style.RESET_ALL)
    input()
    
