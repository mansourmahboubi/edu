
"""https://gist.github.com/owenlamont/cb6312afa50dca6ce94eb9a07e570c67"""
from wordcloud import WordCloud

word_dict = {
    "startup": 2,
    "saas": 2,
    "linux": 2,
    "python": 2,
    "clouds": 2,
    "javascript": 1,
    "django": 1,
    "fastapi": 1,
    "resiliency": 1,
    "reliability": 1,
    "high-availability": 1,
    "imigration": 1,
    "fintech": 2,
    "crypto": 1,
    "stock":1,
    "blockchain":1,
    "edtech": 1,
    "moodle": 1,
    "realtime": 1,
    "product": 2,
    "scrum": 1,
    "agile": 1,
    "scurmban": 1,
    "iterations": 2,
    "modular-monolith": 1,
    "microservice": 1,
    "postgresql": 1,
    "neo4j": 1
}

wordcloud = WordCloud(
    width=1584,
    height=396,
    prefer_horizontal=0.9,
    min_font_size=1,
    relative_scaling=0.5,
    colormap="prism",
).generate_from_frequencies(word_dict)

wordcloud.to_image().save("wordcloud_linkedin.png")