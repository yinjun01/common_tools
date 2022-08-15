# -*- coding: utf-8 -*-
# 
import codecs
import os
import sys
from dictmatch import TriedTree

DEBUG_FILE = "debug.log"

def load_match_dict(dict_file):
    """载入匹配词典
    :param dict_file:str 匹配词典文件
    :return: dic:dict 匹配词典
    """
    dic = dict()
    for line in codecs.open(dict_file, 'r', 'utf-8'):
        line = line.strip("\n\r")
        if not line:
            continue

        items = line.split("\t")
        key = items[0]
        val = items[1] if len(items) >= 2 else ""
        dic[key] = val
    return dic


def serialize_dict(dm_tree, dm_file):
    """serialize查询词典
    :param: dm_tree:TriedTree tried树
    :return: dm_file:file 序列化存储文件
    """
    import pickle
    dm_f = open(dm_file, 'wb')
    pickle.dump(dm_tree.tree, dm_f)
    dm_f.close()


def create_dm(dict_file, dm_file):
    """create_dm"""
    if os.path.exists(dm_file):
        os.remove(dm_file)
    words = load_match_dict(dict_file)
    dm_tree = TriedTree()
    dm_tree.make(words) # 构建tried树
    serialize_dict(dm_tree, dm_file)


def load_dm(dm_file):
    """load_dmfile"""
    import pickle
    dm_tree = TriedTree()
    dm_f = open(dm_file, "rb")
    dm_tree.tree = pickle.load(dm_f)
    dm_f.close()
    return dm_tree


def search_dm(dm_file, test_file, DEBUG_FLAG=False):
    """search_dm
    :param dm_file:str   dm二进制文件
    :param test_file:str 测试文件
    :return: DEBUG_FLAG:bool 是否debug
    """
    dm_tree = load_dm(dm_file)
    if DEBUG_FLAG:
        result_list = []

    for line in codecs.open(test_file, 'r', 'utf-8'):
        line = line.strip('\n\r')
        text = line.split("\t")[0]
        dm_results = dm_tree.search(text)
        if dm_results:
            for dm_result in dm_results:
                word, begin, end, val = dm_result
                print(text, word, begin, end, val)
            if DEBUG_FLAG:
                result_list.append((text, dm_results))
    if DEBUG_FLAG:
        output_debug(result_list)


def output_debug(result_list):
    """output_debug"""
    debug_file = open(DEBUG_FILE, "a")
    d = dict()
    for (text, dm_result) in result_list:
        for (word, begin, end, val) in dm_result:
            word = word + '\t' + val
            if word not in d:
                d[word] = {"count": 0, "sample": set()}

            d[word]["count"] += 1
            if len(d[word]["sample"]) < 3:
                d[word]["sample"].add(text)

    for item in sorted(d.items(), key=lambda x: x[1]["count"], reverse=True):
        word = item[0]
        count = item[1]["count"]
        samples = '\t'.join(item[1]["sample"])
        debug_file.write("%s\t%d\t%s\n" % (word, count, samples))
    debug_file.close()


if __name__ == "__main__":
    DEBUG_FLAG = True

    if DEBUG_FLAG and os.path.exists(DEBUG_FILE):
        os.remove(DEBUG_FILE)

    flag = sys.argv[1]
    if flag == 'create':
        match_dic = sys.argv[2]  #"search_word.dic"
        dm_dic = sys.argv[3]     #"sensitive_word.dm"
        create_dm(match_dic, dm_dic)

    if flag == 'search':
        dm_dic = sys.argv[2]
        test_file = sys.argv[3]
        search_dm(dm_dic, test_file, DEBUG_FLAG)
