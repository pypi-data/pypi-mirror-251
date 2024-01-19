import Levenshtein
import pypinyin
import edit_distance_correction.utils as utils
import pandas as pd
import re
import jieba
import os

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))
class Corrector:
    def __init__(self):
        #pinyin:set(word)
        self.pinyin_di = dict()
        #start:set(pinyin)
        self.start_pinyin_di = dict()
        self.correction_dict = dict()
        self.same_stroke_dict = dict()
        self._load_correction()
        self._load_same_stroke()


    def _load_correction(self):
        correction = pd.read_excel(_get_module_path("correction.xlsx"))
        for original, corr in zip(correction["original"], correction["correction"]):
            if original not in self.correction_dict:
                self.correction_dict[original] = set()
            self.correction_dict[original].add(corr)


    def _load_same_stroke(self):
        with open(_get_module_path("same_stroke.txt")) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                arr = re.split("\s+", line)
                if len(arr) > 1:
                    for i, elem1 in enumerate(arr):
                        for j, elem2 in enumerate(arr):
                            if elem1 not in self.same_stroke_dict:
                                self.same_stroke_dict[elem1] = set()
                            self.same_stroke_dict[elem1].add(elem2)


    def load_target_words(self, target_words):
        for word in target_words:
            res = utils.get_pinyin(word, True)
            if res["pinyin"] not in self.pinyin_di:
                self.pinyin_di[res["pinyin"]] = set()
            self.pinyin_di[res["pinyin"]].add(word)
            if res["start"] not in self.start_pinyin_di:
                self.start_pinyin_di[res["start"]] = set()
            self.start_pinyin_di[res["start"]].add(res["pinyin"])




    #     #任意拼音转换
    #     #重复拼音
    #     #特定容易混淆拼音:n:l, s: sh, 多g
    #     #开头同拼音
    #     #相邻拼音换位
    #     #少、多字母
    #     #本身拼音，没有汉语转拼音
    def _transform_pinyin(self, pinyin, include_self=False):
        res = utils.replace_char(pinyin, self.correction_dict, max_k=6)
        res = res.union(utils.transform_char(pinyin))
        if include_self:
            res.add(pinyin)
        return res


    def max_backward_match_transform(self, word_list, vocab, max_k=10):
        res = []
        second_res = []
        end = len(word_list)
        while end > 0:
            break_flag = False
            for i in range(max_k):
                start = end - max_k + i
                if start  < 0: continue
                temp = "".join(word_list[start:end])
                temp_res = self._transform_pinyin(temp)
                #直接匹配是最好的
                if temp in vocab:
                    res.append([temp, start, end])
                    end = start
                    break_flag = True
                    break
                #其次是有转换的匹配
                else:
                    for second_temp in temp_res:
                        if second_temp in vocab:
                            second_res.append([second_temp, start, end, temp])
            if not break_flag:
                end -= 1
        res.reverse()
        return res, second_res



    # def find_word(self, word, pinyin_threshold=2, char_threshold=4):
    #     # word = word.strip().lower()
    #     # if re.match("^[a-z]+$", word) is not None:
    #     word_pinyin = self._get_pinyin(word)
    #     print(word_pinyin)
    #     word_pinyin, word_start_pinyin = word_pinyin["pinyin"], word_pinyin["start"]
    #     candidate_pinyin = self._transform_pinyin(word_pinyin).union(self.start_pinyin_di.get(word_start_pinyin, set()))
    #     pinyin_dis = [(elem, Levenshtein.distance(word_pinyin, elem)) for elem in candidate_pinyin]
    #     pinyin_dis = list(filter(lambda x: x[1] <= pinyin_threshold, pinyin_dis))
    #     valid_choice = dict()
    #     for pinyin in pinyin_dis:
    #         dis = Levenshtein.distance(word, pinyin[0])
    #         candidate_chars = self.pinyin_di.get(pinyin[0], set())
    #         for cc in candidate_chars:
    #             char_dis = min(Levenshtein.distance(word, cc), dis)
    #             print(cc, char_dis)
    #             if char_dis <= char_threshold:
    #                 valid_choice[cc] = pinyin[1] + char_dis
    #     if len(valid_choice) > 0:
    #         res = sorted(valid_choice.items(), key=lambda x:x[1])
    #         return res[0][0]
    #     return None


    def recall_word(self, query):
        cuts = jieba.lcut(query)
        query_pinyin, query_start_pinyin, query_pinyin_list = "", "", []
        for cut in cuts:
            qp = utils.get_pinyin(cut, mode="pinyin")
            #query_pinyin_list.extend(qp)
            query_pinyin_list.append(qp)
        #todo:考虑简拼
        #todo:max_k为词典中最大词长度？
        #todo:召回形近字
        #todo:目前只取一个，后面考虑怎样展示，多种可能的排列组合？
        res, second_res = self.max_backward_match_transform(query_pinyin_list, self.pinyin_di, max_k=10)
        insider = []
        outsider = []
        for elem in res:
            original = "".join(cuts[elem[1]:elem[2]])
            pinyin = "".join(query_pinyin_list[elem[1]:elem[2]])
            candidates = []
            for word in self.pinyin_di.get(pinyin, []):
                transform_words = utils.get_all([[char, utils.get_pinyin(char, "pinyin")] for char in word])
                print("transform_words: ", transform_words)
                candidates.append([word, min([Levenshtein.distance(w, original) for w in transform_words]), elem[1], elem[2]])
            #candidates = [[word, min(Levenshtein.distance(word, original), Levenshtein.distance(pinyin, original)), elem[1], elem[2]] for word in self.pinyin_di.get(pinyin, [])]
            candidates = sorted(candidates, key=lambda x: x[1])
            candidates = [candidates[0]]
            # i = len(candidates)
            # if len(candidates) > 1:
            #     for ii in range(1, len(candidates)):
            #         if candidates[ii][1] > candidates[0][1]:
            #             i = ii
            #             break
            # candidates = candidates[:i]
            insider.extend(candidates)
        for elem in second_res:
            original = "".join(cuts[elem[1]:elem[2]])
            pinyin = elem[0]
            candidates = []
            for word in self.pinyin_di.get(pinyin, []):
                transform_words = utils.get_all([[char, utils.get_pinyin(char, "pinyin")] for char in word])
                print("transform_words: ", transform_words)
                candidates.append(
                    [word, min([Levenshtein.distance(w, original) for w in transform_words]), elem[1], elem[2]])
            #candidates = [[word, min(Levenshtein.distance(word, original), Levenshtein.distance(pinyin, original)), elem[1], elem[2]] for word in self.pinyin_di.get(pinyin, [])]
            candidates = sorted(candidates, key=lambda x: x[1])
            candidates = [candidates[0]]
            # i = len(candidates)
            # if len(candidates) > 1:
            #     for ii in range(1, len(candidates)):
            #         if candidates[ii][1] > candidates[0][1]:
            #             i = ii
            #             break
            # candidates = candidates[:i]
            outsider.extend(candidates)
        all_candidates = utils.check_conflict(insider, outsider)
        all_candidates = list(filter(lambda x: x[0] != "".join(cuts[x[2] : x[3]]), all_candidates))
        print(all_candidates)
        # print(insider)
        # print(outsider)
        # print(all_candidates)
        res = utils.get_correct(all_candidates, cuts)
        return res






# import time
# c = Corrector()
# target_words = utils.read_files("target_words")
# c.load_target_words(target_words)
# test_words = utils.read_files("test_file", True)
# start = time.time()
# for w in test_words:
#     print(w)
#     res = c.recall_word(w)
#     print(res)
#     print("\n")
# print(time.time() - start)




























