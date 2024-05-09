import io
import unittest

from random_wikipedia_article import Article, show


class TestShow(unittest.TestCase):
    def setUp(self):
        self.article = Article("Lorem Ipsum", "Lorem ipsum dolor sit amet.")
        self.file = io.StringIO()

    def test_final_newline(self):
        show(self.article, self.file)
        self.assertEqual("\n", self.file.getvalue()[-1])
