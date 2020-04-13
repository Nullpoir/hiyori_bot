def ClassifyTweet(text):
    text = text.strip("@mHiyori0324").strip(" ").strip("　").strip("\n")
    print(text)
    if text == "天気を教えて。":
        return "weather"
    else:
        return "markov"
