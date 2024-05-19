from random_wikipedia_article import build_user_agent

def test_build_user_agent():
    assert "random-wikipedia-article" in build_user_agent()
