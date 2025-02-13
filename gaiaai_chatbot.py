import requests
import time
import random
import logging
from requests.exceptions import Timeout, RequestException

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# API 请求的URL
url = "https://pengu.gaia.domains/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"  # 替换为你的API密钥
}

# 问题列表
questions = [
    "What is a neural network?",
    "What is the Big Bang theory?",
    "What is artificial intelligence?",
    "What is a VPN?",
    "What is turbulence?",
    # 添加更多问题
]

# 请求数据的结构
def create_payload(question):
    return {
        "model": "qwen2-0.5b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }

# 发送请求的函数
def send_request(question, retries=3, timeout=30):
    payload = create_payload(question)
    attempt = 1
    delay = 2  # 初始延迟时间

    while attempt <= retries:
        try:
            logger.info(f"Attempt {attempt} for question: {question}")
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

            # 如果响应成功
            if response.status_code == 200:
                logger.info(f"Successfully processed question: {question}")
                return response.json()
            else:
                logger.warning(f"Request failed with status code: {response.status_code}")
                break  # 如果返回非200状态码，退出重试

        except Timeout:
            logger.warning(f"Timeout error, retrying in {delay} seconds...")
        except RequestException as e:
            logger.error(f"Request failed with error: {e}")
            break

        # 重试时延迟
        time.sleep(delay)
        delay *= 2  # 每次重试延迟翻倍
        attempt += 1

    logger.error(f"Max retries exceeded for question: {question}")
    return None

# 主程序执行
def main():
    for question in questions:
        response = send_request(question)

        if response:
            logger.info(f"Response for '{question}': {response}")
        else:
            logger.error(f"Failed to get response for question: {question}")

        # 问题间增加随机延迟，避免过度频繁请求
        delay = random.uniform(1, 3)  # 随机延迟1到3秒
        time.sleep(delay)

if __name__ == "__main__":
    main()

