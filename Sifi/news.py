from newsdataapi import NewsDataApiClient

# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey="pub_19348ced16687bb956e90fc4ba74f90d363e7")

# You can pass empty or with request parameters {ex. (country = "us")}

response = api.news_api(language = "en", country = "in")
thislist = response["results"]
news = []
for i in range(len(thislist)):
    news.append(thislist[i]["title"])
print(news)