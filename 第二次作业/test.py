import unittest
from main import tokenize, count_words, cosine_similarity


class TestTextSimilarity(unittest.TestCase):

    def test_tokenize(self):
        # 测试 tokenize 函数
        stopwords_file = 'test_stopwords.txt'
        text_with_stopwords = "这是一个测试文本"

        expected_tokens_with_stopwords = ['这是', '一个', '测试', '文本']

        tokens_with_stopwords = tokenize(stopwords_file, text_with_stopwords)

        # 验证每个标记是否正确
        self.assertEqual(tokens_with_stopwords[0], expected_tokens_with_stopwords[0])
        self.assertEqual(tokens_with_stopwords[1], expected_tokens_with_stopwords[1])
        self.assertEqual(tokens_with_stopwords[2], expected_tokens_with_stopwords[2])
        self.assertEqual(tokens_with_stopwords[3], expected_tokens_with_stopwords[3])

    def test_count_words(self):
        # 测试 count_words 函数
        tokens = ['a', 'b', 'a', 'c']
        total_unique_words = ['a', 'b', 'c', 'd']
        expected_vector = [2, 1, 1, 0]

        vector = count_words(tokens, total_unique_words)

        self.assertEqual(vector, expected_vector)

    def test_cosine_similarity(self):
        # 测试 cosine_similarity 函数
        vec1 = [1, 2, 3]
        vec2 = [2, 3, 4]
        expected_similarity = 0.9925833339709303

        similarity = cosine_similarity(vec1, vec2)

        self.assertAlmostEqual(similarity, expected_similarity, places=4)


if __name__ == '__main__':
    unittest.main()