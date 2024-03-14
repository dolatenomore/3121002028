# 导入所需库
import jieba
import numpy as np
from collections import Counter
import argparse
import os


# 定义对文本进行分词的函数，其会剔除停用词
def tokenize(stopwords_file, text):
    # 检查stopwords.txt文件是否存在
    if not os.path.exists(stopwords_file):
        # 如果文件不存在则创建
        open(stopwords_file, 'w', encoding='utf-8').close()

    # 在文件存在的情况下读取文件内容
    stopwords = set(line.strip() for line in open(stopwords_file, 'r', encoding='utf-8').readlines())
    # 使用jieba分词
    words = jieba.cut(text)
    # 删除停用词
    return [word for word in words if word not in stopwords]


# 定义词频统计函数，返回固定长度的向量
def count_words(tokens, total_unique_words):
    word_counts = Counter(tokens)
    vector = [word_counts.get(word, 0) for word in total_unique_words]
    return vector


# 定义计算向量余弦相似度的函数
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


# 定义主函数
def main(args):
    stopwords_file = 'stopwords.txt'

    # 读取原文本
    with open(args.source_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    # 读取待比较文本
    with open(args.target_file, 'r', encoding='utf-8') as f:
        target_text = f.read()

    # 对原文和待比较文本进行分词
    source_tokens = tokenize(stopwords_file, source_text)
    target_tokens = tokenize(stopwords_file, target_text)

    # 获取所有文本中出现的唯一词汇
    total_words = list(set(source_tokens + target_tokens))

    # 形成固定长度的词频向量
    source_vector = count_words(source_tokens, total_words)
    target_vector = count_words(target_tokens, total_words)

    # 计算两文本的相似度
    similarity = cosine_similarity(source_vector, target_vector)
    similarity_percentage = similarity * 100

    # 将计算结果写入指定文件，保留2位小数，并转换为百分数形式
    with open(args.res_file, 'w', encoding='utf-8') as f:
        f.write('%.2f%%' % similarity_percentage)


# 此处代码确保在被作为模块导入时，不会自动运行主函数
if __name__ == "__main__":
    # 定义解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', help='原文文件的绝对路径')
    parser.add_argument('target_file', help='抄袭版本文件的绝对路径')
    parser.add_argument('res_file', help='输出答案文件的绝对路径')
    # 解析参数
    args = parser.parse_args()
    # 执行主函数
    main(args)