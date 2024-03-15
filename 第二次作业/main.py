import jieba
import numpy as np
from collections import Counter
import argparse
import os
import tracemalloc

# 分词函数，将文本分词并去除停用词
def tokenize(stopwords_file, text):
    stopwords = set()
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(line.strip() for line in file.readlines())
    words = jieba.cut(text)  # 使用结巴分词进行分词
    return [word for word in words if word.strip() and word not in stopwords]

# 统计词频函数，将分词后的文本转换为词向量
def count_words(tokens, total_unique_words):
    word_counts = Counter(tokens)
    vector = [word_counts.get(word, 0) for word in total_unique_words]
    return vector

# 计算余弦相似度函数
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# 主函数
def main(args):
    stopwords_file = 'test_stopwords.txt'

    with open(args.source_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    with open(args.target_file, 'r', encoding='utf-8') as f:
        target_text = f.read()

    # 对原文和抄袭版本文本进行分词处理
    source_tokens = tokenize(stopwords_file, source_text)
    target_tokens = tokenize(stopwords_file, target_text)

    # 获取总词汇表
    total_words = list(set(source_tokens + target_tokens))

    # 将分词后的文本转换为词向量
    source_vector = count_words(source_tokens, total_words)
    target_vector = count_words(target_tokens, total_words)

    # 计算余弦相似度
    similarity = cosine_similarity(source_vector, target_vector)
    similarity_percentage = similarity * 100

    with open(args.res_file, 'w', encoding='utf-8') as f:
        f.write('相似度为：%.2f%%' % similarity_percentage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', help='原文文件的绝对路径')
    parser.add_argument('target_file', help='抄袭版本文件的绝对路径')
    parser.add_argument('res_file', help='输出答案文件的绝对路径')
    args = parser.parse_args()

    # 启用 tracemalloc 模块，用于跟踪内存分配
    tracemalloc.start()

    # 调用主函数处理文本相似度计算
    main(args)

    # 获取内存分配的堆栈跟踪信息
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("[ Top 10 ]")
    # 打印内存分配前 10 个堆栈跟踪信息
    for stat in top_stats[:10]:
        print(stat)