def search(df, keywords):
    """
    Functino for returning documents containing specified keywords
    :param df: dataframe to be searched
    :param keywords: keywords to be searched for
    :return: dataframe with only text columns where keywords are present
    """
    keywords = keywords.split()

    l = len(keywords)

    arr = "[" + ("word[%i].lower() in string.lower() or " * (l-1)) + "word[%i].lower() in string.lower()" + \
          " for string in df.text]"
    arr = arr %tuple([i for i in range(l)])

    df = df[arr]

    return df