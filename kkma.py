import jpype
from konlpy.tag import Kkma


class kkma(object):

    MORP, POS = 0, 1

    def __init__(self, jar_path):
        kkma = Kkma()
        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), "-Dfile.encoding=UTF-8",
                           "-Djava.class.path="+jar_path+"org.snu.ids.ha.jar")

        java_pkg_ma = jpype.JPackage('org.snu.ids.ha.ma')
        kkma_analyzer = java_pkg_ma.MorphemeAnalyzer
        kkma_sentence = java_pkg_ma.Sentence
        self.analyzer = kkma_analyzer()
        self.sentence = kkma_sentence()

        java_pkg_sp = jpype.JPackage('org.snu.ids.ha.sp')
        kkma_tree = java_pkg_sp.ParseTree
        kkma_parser = java_pkg_sp.Parser
        self.tree = kkma_tree()
        self.parser = kkma_parser()

    def word_info(self, sentence):
        word_list, morphs_list, poses_list, mp_list = [], [], [], []
        sentences = self.__analysis__(sentence)
        for sentence in sentences:
            for word_info in sentence:
                word_list.append(word_info.getExp())
                morphs, poses, mps = [], [], []
                for morph_info in word_info:
                    mp = morph_info.getSmplStr()
                    segments = mp.split('/')
                    morphs.append(segments[self.MORP])
                    poses.append(segments[self.POS])
                    mps.append(mp)
                morphs_list.append(morphs)
                poses_list.append(poses)
                mp_list.append(mps)
        return word_list, morphs_list, poses_list, mp_list

    def relation(self, sentence):
        word_list, relation_list =[], []
        sentences = self.__analysis__(sentence)
        for sentence in sentences:
            self.sentence = sentence
            self.tree = self.parser.parse(self.sentence)
            for idx_word in range(0, self.sentence.size()):
                for idx_edge in range(0, self.tree.getEdgeList().size()):
                    if self.tree.getEdgeList().get(idx_edge).getChildNode().getEojeol().getExp() == self.sentence.get(idx_word).getExp():
                        word_list.append(self.sentence.get(idx_word).getExp())
                        relation_list.append(self.tree.getEdgeList().get(idx_edge).getRelation())
        return word_list, relation_list

    def __analysis__(self, sentence):
        analysis = self.analyzer.analyze(sentence)
        process = self.analyzer.postProcess(analysis)
        result = self.analyzer.leaveJustBest(process)
        return self.analyzer.divideToSentences(result)


if __name__ == '__main__':
    morph = kkma("lib/")
    test_sentence = "오늘은 날씨가 참좋네."

    w, m, p, mp = morph.word_info(test_sentence)
    print("입력문장: {}".format(test_sentence))
    print("-단어: {}".format(w))
    print("-형태소: {}".format(m))
    print("-품사: {}".format(p))
    print("-형태소/품사: {}".format(mp))

    w_idx = 0
    print("{}번째 단어:'{}'는 형태소'{}'와 품사'{}'로 구성됨을 알 수 있음".format(w_idx, w[w_idx], m[w_idx], p[w_idx]))

    w, r = morph.relation(test_sentence)
    print("입력문장: {}".format(test_sentence))
    print("-단어: {}".format(w))
    print("-관계: {}".format(r))





