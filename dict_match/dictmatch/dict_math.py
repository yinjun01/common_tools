# -*- encoding: utf-8 -*-
'''
@File    :   dict_match.py
@Desc    :   基于一个前缀组成的dict去实现Tried树的类
'''

class TriedTree(object):
    """TriedTree"""
    def __init__(self):
        """使用单个dict存储trie树"""
        self.tree = {}
        
    def add_word(self, word, val = 0) -> None:
        """添加单词word到Trie树中
        Args:
            word: string类型, 要添加的单词
            val: 非None的任意类型, 因为None有特殊含义
        """
        assert val != None, "val can't be None"
        # assert用于判断一个表达式，在表达式条件为false的时触发异常
        # 前缀也存于dict中，用None进行区分
        # 查询时依次查询前缀是否在词表中
        self.tree[word] = val
        for i in range(1, len(word)):
            wfrag = word[:i]
            self.tree[wfrag] = self.tree.get(wfrag, None)

    def make(self, dic):
        """make"""
        for (key, val) in dic.items():
            self.add_word(key, val)
    
    def search(self, content, mode="FMM"):
        """search"""
        if mode == "FMM":
            return self.search_fmm(content)
        elif mode == "ALL":
            return self.search_all(content)
    
    def search_fmm(self, content):
        """前向最大匹配／Forward maximum matching
        对content的文本进行多模匹配，返回前向最大匹配的单词
        Args:
            content: string类型, 用于多模匹配的字符串
        Returns:
            list类型, 匹配到的单词列表，返回每个结果包含为匹配到的单词，在句中的起止位置，val值，
            每个元素格式为(word, begin, end, val) 具体示例：[("华为", 0, 2, 'BRAND'), ("笔记本", 4, 7, "PRODUCT)]
        """
        result = []
        length = len(content)
        start = 0
        while start < length:
            for end in range(start+1, length + 1):
                cur_word = content[start:end]
                # 当前前缀不在Tried表中了，前进start位置
                if cur_word not in self.tree:
                    if len(result) == 0 or start != result[-1][1]:
                        start += 1
                    else:
                        start = result[-1][2]
                    break
                
                # 查到单词，更新到词表中
                val = self.tree[cur_word] 
                if val is not None:
                    if len(result) == 0 or start != result[-1][1]:
                        result.append((cur_word, start, end, val))
                    else:
                        result[-1] = (cur_word, start, end, val)
            else:
                start += 1

        return result

    def search_all(self, content):
        """完全匹配
        对content的文本进行多模匹配，返回所有匹配的单词
        Args:
            content: string类型, 用于多模匹配的字符串
        Returns:
            list类型, 所有匹配单词列表，每个元素为匹配的模式串在句中的起止位置，比如：
            [[0, 2], [4, 7]]
        """
        result = []
        length = len(content)
        for start in range(length):
            for end in range(start+1, length + 1):
                cur_word = content[start:end]
                if cur_word not in self.tree:
                    break
                val = self.tree[cur_word]
                if val is not None:
                    result.append((cur_word, start, end, val))
        return result


if __name__ == "__main__":
    words = {"a": "ORG", "ab": "m", "c": 0, "d": 'adj', "e": 0, "f": "n", "g": 'n'}
    text = 'cba'
    tree = TriedTree()
    for word, val in words.items():
        tree.add_word(word, val)
        print(tree.tree)
