import base64
from PIL import Image
import numpy as np
import io
import requests
import json
import subprocess
from datetime import datetime
import urllib, os, base64
import time
import urllib.parse
import pytesseract

cache_file_path = "baidu_aip_token.txt"
pytesseract.pytesseract.tesseract_cmd = r"D:\Soft\Tesseract-OCR\tesseract.exe"


def ocr_img_file_to_text_by_tesseract(file, ocr_red_text, debug=True):
    image_data = Image.open(file)
    if not ocr_red_text:
        image_data = remove_red_channal(image_data)
    result = pytesseract.image_to_string(image=image_data, lang="chi_sim", config="--psm 1 --oem 0")  #路径；语言；配置
    return result


def get_access_token(expiry_duration, debug=False):
    if os.path.isfile(cache_file_path):
        if debug: print("file exists, check expiry duration")
        # 获取文件的最后修改时间
        last_modified_time = os.path.getmtime(cache_file_path)
        # 计算当前时间与最后修改时间的差值（秒）
        current_time = time.time()
        time_difference = current_time - last_modified_time
        if time_difference < expiry_duration:
            with open(cache_file_path, "r") as f:
                token = f.read()
                print("token=", token)
                return token

    token = 取access_token()
    with open(cache_file_path, "w") as f:
        f.write(token)
    print("token=", token)

    return token


urllib.parse.urlencode


def 取access_token():
    client_id = "oUMYZOr7fO8IL4kZ5MDUZB4a"  #client_id： 必须参数，应用的API Key；
    client_secret = "NiubEsOip1eUY9sDgD0Gjs6GxomGgc3P"  #必须参数，应用的Secret Key；

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', 'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials"
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    jsresult = json.loads(response.text)
    token = jsresult['access_token']
    #print(("token = " +token) )
    #print("--------------------------------")
    return token


def basicGeneral(image, options=None):
    """
        通用文字识别（标准版）
    """
    options = options or {}
    data = {}
    data['image'] = base64.b64encode(image).decode()
    data.update(options)


def img2gray(local_img):
    import cv2
    gray = cv2.imread(local_img)
    gray2 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    ret, gray2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_OTSU)
    cv2.imwrite(local_img, gray2)


def remove_red_channal(image):
    # 将图片转换为RGB模式
    image = image.convert('RGB')
    # 将图片转换为numpy数组
    image_array = np.array(image)
    # 去除红色通道
    image_array[:, :, 0] = 0
    # 将numpy数组转换回PIL图片
    image = Image.fromarray(image_array)
    return image


def 百度OCR(img_file, ocr_red_text, debug=False):
    if debug: print("Fimg_url=" + img_file)
    image_data = Image.open(img_file)

    if not ocr_red_text:
        image_data = remove_red_channal(image_data)
    # 将图片转换为 base64 编码
    buffered = io.BytesIO()
    image_data.save(buffered, format="PNG")
    img_byte = buffered.getvalue()
    data = {"detect_direction": "false", "paragraph": "false", "probability": "false"}
    data['image'] = base64.b64encode(img_byte).decode()
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token(3600 * 24 * 3)

    # payload=f'image={img_data_base64}&detect_direction=false&paragraph=false&probability=false'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=data)
    print("response.txt=", response.text)
    if response:
        clear_text = response.json()
        print(clear_text)
        both = ""
        for i in clear_text['words_result']:
            both = both + i['words'] + ""
    if debug: print("here baiduocr", both)

    return both


def ocr_img_by_umi_ocr_exe(img):

    cmd = ['D:\\Soft\\Office\\Umi-OCR_Paddle_v2.0.1\\Umi-OCR.exe', '--path', f'D:/UserData/resource/ocr/cls_ocr_test.jpg', '--thread']
    print("cmd=", cmd)
    result = subprocess.Popen(cmd, shell=True)
    print(result)
    return result


def preprocess_image(image_path, ocr_red_text=False, debug=False):
    """
    对图片进行处理以便ocr识别

    Args:
        image_path (str): 文件路径

    Returns:
        _type_: image data of base64 str
    """
    # 打开图片
    image = Image.open(image_path)
    if not ocr_red_text:
        image = remove_red_channal(image)
    # 灰度化
    image = image.convert('L')
    # 二值化
    #image = image.point(lambda x: 0 if x < 100 else 255, '1')

    # 将图片转换为 base64 编码
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    #image.save('preprocessed.png')#保存到硬盘
    img_byte = buffered.getvalue()
    return base64.b64encode(img_byte).decode('utf-8')


def encode_image(image_path):
    """
    将图片转换为 base64 编码
    
    """
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_byte = buffered.getvalue()
        return base64.b64encode(img_byte)


def ocr_img_file_to_text(image_path, ocr_red_text=False, option=None, debug=False):
    """
    识别图像文件，使用Umi-Ocr http方式

    Args:
        image_path (str): 图像文件路径
        debug (bool, optional): 是否打印详细处理过程中的信息. Defaults to False.

    Returns:
        _type_: 返回识别后的文本
    """
    if debug: print("------------------------------------ocr----------------------------------------")
    base64img = preprocess_image(image_path, ocr_red_text=ocr_red_text, debug=debug)

    url = "http://127.0.0.1:10024/api/ocr"
    data = {"base64": base64img, "ocr": {"language": "models/config_chinese.txt", "cls": False, "limit_side_len": 960, "tbpu": {"merge": "MergeLine"}}, "rapid": {"language": "简体中文", "angle": False, "maxSideLen": 1024, "tbpu": {"merge": "MergeLine"}}}
    if option: data['option'] = option
    if debug: print("post image data to umi-ocr")
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        text = ""
        result_data = result.get("data")
        if "No text" in result_data:  #No text found in image. Path: "base64"
            return False
        for i in result_data:
            t = i['text']
            #t= t+"\n"  if len(t)>10 else " "
            text += t
        if debug: print("ocr response result=，=", text)

    else:
        print("识别失败")
        return False
    return text


if __name__ == "__main__":

    # 测试
    import lyyddforward
    url = r"https://static.dingtalk.com/media/lAPPD2P17inUJrtkzQHC_450_100.bmp"
    fl = lyyddforward.download_file(url)
    base64_image = preprocess_image(fl)  # 替换为你的图片文件路径
    result = 百度OCR(fl, False)
    print("result = ", result)
