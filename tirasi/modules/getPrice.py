import re

import google.generativeai as genai


def extract_numbers(text):
    numbers = re.findall(r"\d+", text)
    return numbers


def getGeminiAPIResponse(prompt):
    GOOGLE_API_KEY = "Gemini API Key"

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        prompt + "の文字列の中から値段情報を摘出してください、もしも税込価格があった場合税込価格を出力してください"
    )
    price = extract_numbers(response.text)
    if len(price) == 0:
        return 0
    else:
        try:
            return int(price[0])
        except:
            return price


if __name__ == "__main__":
    print(getGeminiAPIResponse("青森県産きおう13128色税迅固搭138"))
