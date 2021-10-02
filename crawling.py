import requests
from bs4 import BeautifulSoup
import dload

# 유저에이전트 ㅡ 개인마다 다름
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}


for i in range(1, 11):  # 페이지 수 범위 (1~10 페이지 )
    url = f"https://mypetlife.co.kr/popular-posts/page/{i}/?filter=cat"
    res = requests.get(url, headers=headers)
    res.raise_for_status()  # 정상적으로 정보 받았는지 확인

    soup = BeautifulSoup(res.text, "lxml")
