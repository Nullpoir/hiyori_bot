def ClassifyTweet(text):
    text = text.strip("@mHiyori0324").strip(" ").strip("　").strip("\n")
    if text == "天気を教えて、ひよりちゃん":
        return "weather"
    else:
        return "markov"
