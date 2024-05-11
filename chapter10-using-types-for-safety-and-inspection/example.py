import textwrap

data = {"title": "Gegenes nostrodamus"}

summary = data.get("extract")
summary = textwrap.fill(summary)
