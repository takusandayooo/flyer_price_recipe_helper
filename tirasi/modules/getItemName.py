import google.generativeai as genai


def getGeminiAPIResponse(prompt):
    GOOGLE_API_KEY = "Gemini API Key"

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        "次の()に挟まれた文章の中から食材だけをを出力してください。例えば、「国産牛肩うす造り焼肉用交雑種100g本体498価格税込価格537円」だった場合「牛肉」という最小な文字列を出力してください。複数食材がある場合はコンマで区切って出力してください。\n("
        + prompt
        + ")?"
    )
    try:
        return response.text
    except:
        return "なし"


if __name__ == "__main__":
    print(getGeminiAPIResponse("カナダ産豚回一スしゃぶしやぶ用100g108円税込価格116"))
