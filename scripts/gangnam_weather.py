"""
서울 강남구 날씨 + 미세먼지 정보를 API 키 없이 가져와 weather.txt 에 기록.
데이터 출처: 네이버 검색(search.naver.com) 날씨 위젯 HTML 스크래핑.
매일 09:00 실행을 전제로 하며, 매 실행마다 weather.txt 에 한 줄씩 이력을 append 한다.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

QUERY = "강남구 날씨"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "weather.txt"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

WEATHER_EMOJI = {
    "맑음": "☀️",
    "구름조금": "🌤️",
    "구름많음": "⛅",
    "흐림": "☁️",
    "흐리고 비": "🌧️",
    "비": "🌧️",
    "소나기": "🌦️",
    "눈": "❄️",
    "눈/비": "🌨️",
    "뇌우": "⛈️",
    "안개": "🌫️",
}

GRADE_EMOJI = {
    "좋음": "🟢",
    "보통": "🟡",
    "나쁨": "🟠",
    "매우나쁨": "🔴",
}


def weather_emoji(desc: str | None) -> str:
    if not desc:
        return "🌈"
    for key, emoji in WEATHER_EMOJI.items():
        if key in desc:
            return emoji
    return "🌈"


def grade_emoji(grade: str) -> str:
    return GRADE_EMOJI.get(grade, "⚪")


def fetch_html() -> str:
    resp = requests.get(
        "https://search.naver.com/search.naver",
        params={"query": QUERY},
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.text


def text_or_none(el) -> str | None:
    return el.get_text(" ", strip=True) if el else None


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    region = text_or_none(soup.select_one("h2.title")) or "서울특별시 강남구"

    temp_raw = text_or_none(soup.select_one(".temperature_text"))
    # "현재 온도 27.6 °" 형태에서 숫자만 추출
    temp = None
    if temp_raw:
        digits = "".join(c for c in temp_raw if c.isdigit() or c == ".")
        temp = digits if digits else temp_raw

    weather_main = text_or_none(soup.select_one(".weather_main"))

    summary_el = soup.select_one(".summary_list") or soup.select_one(".main_info")
    summary = text_or_none(summary_el) or ""

    # "체감 29.4° 습도 77% 서풍 1.1m/s" 형태에서 값 추출
    feels_like = None
    m = re.search(r"체감\s*([\d.\-]+)\s*°", summary)
    if m:
        feels_like = m.group(1)

    humidity = None
    m = re.search(r"습도\s*(\d+)\s*%", summary)
    if m:
        humidity = m.group(1)

    wind = None
    m = re.search(r"([가-힣]*풍)\s*([\d.]+\s*m/s)", summary)
    if m:
        wind = f"{m.group(1)} {m.group(2)}"

    dust = "정보 없음"
    fine_dust = "정보 없음"
    uv = "정보 없음"
    for li in soup.select(".today_chart_list li.item_today"):
        label = text_or_none(li)
        if not label:
            continue
        if label.startswith("초미세먼지"):
            fine_dust = label.replace("초미세먼지", "").strip()
        elif label.startswith("미세먼지"):
            dust = label.replace("미세먼지", "").strip()
        elif label.startswith("자외선"):
            uv = label.replace("자외선", "").strip()

    return {
        "region": region,
        "temp": temp,
        "weather_main": weather_main,
        "feels_like": feels_like,
        "humidity": humidity,
        "wind": wind,
        "dust": dust,
        "fine_dust": fine_dust,
        "uv": uv,
    }


def format_entry(data: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    w_emoji = weather_emoji(data["weather_main"])
    temp_line = f"🌡️ 현재 {data['temp'] or '?'}°C"
    if data["feels_like"]:
        temp_line += f" (체감 {data['feels_like']}°C)"

    detail_bits = []
    if data["humidity"]:
        detail_bits.append(f"💧 습도 {data['humidity']}%")
    if data["wind"]:
        detail_bits.append(f"🍃 {data['wind']}")
    detail_line = "   ".join(detail_bits)

    lines = [
        "🌈" + "═" * 30,
        f"📍 {data['region']}  |  🕘 {now}",
        "─" * 32,
        f"{w_emoji} 날씨: {data['weather_main'] or '정보 없음'}",
        temp_line,
    ]
    if detail_line:
        lines.append(detail_line)
    lines += [
        "─" * 32,
        f"😷 미세먼지    : {data['dust']} {grade_emoji(data['dust'])}",
        f"🤧 초미세먼지  : {data['fine_dust']} {grade_emoji(data['fine_dust'])}",
        f"🕶️ 자외선      : {data['uv']} {grade_emoji(data['uv'])}",
        "═" * 32,
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    try:
        html = fetch_html()
        data = parse(html)
        entry = format_entry(data)
    except Exception as e:
        entry = f"⚠️ [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 조회 실패: {e}\n"

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    print(entry)


if __name__ == "__main__":
    sys.exit(main() or 0)
