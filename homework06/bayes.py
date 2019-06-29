from collections import Counter
import math


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):

        """ Fit Naive Bayes classifier according to X, y. """
        self.w = []
        for word in y:
            if word not in self.w:
                self.w.append(word)
        chet = []
        for kl in self.w:
            ver = y.count(kl)
            chet.append(ver)
        d = len(y)
        self.v_k = []
        for el in chet:
            self.v_k.append(el / d)
        tabl = []
        for el in y:
            if el not in tabl:
                tabl.append(el)
                tabl.append([])
        slova = []
        for el in X:
            a = el.split()
            slova.append(a)
        self.list_sl = []
        for i in range(len(slova)):
            for el in slova[i]:
                self.list_sl.append(el)
        self.k_s = (len(self.list_sl))
        for i in range(len(y)):
            for j in range(len(tabl)):
                if tabl[j] == y[i]:
                    for el in slova[i]:
                        tabl[j + 1].append(el)
        self.itog = []
        for i in range(0, len(tabl), 2):
            a = tabl[i]
            b = Counter(tabl[i + 1])
            di = {a: b}
            self.itog.append(di)

        return self.w, self.v_k, self.itog, self.list_sl, self.k_s

    def predict(self, X):

        """ Perform classification on an array of test vectors X. """
        self.new = []
        for el in X:
            a = el.split()
            self.new.append(a)
        self.labelsnew = []
        max = -500
        for j in range(len(self.new)):
            n = self.new[j]
            for i in range(len(self.w)):
                nc = sum((self.itog[i][self.w[i]]).values())
                b = 0
                for word in n:
                    if word not in self.list_sl:
                        formslova = 0
                    elif word not in (self.itog[i][self.w[i]]).keys():
                        c = 0
                        formslova = math.log(((c + self.alpha) / (nc + self.alpha * self.k_s)), math.e)
                    else:
                        c = self.itog[i][self.w[i]][word]
                        formslova = math.log(((c + self.alpha) / (nc + self.alpha * self.k_s)), math.e)
                    b += formslova
                b = b + self.v_k[i]
                if b > max:
                    max = b
                    max_i = self.w[i]
            self.labelsnew.append(max_i)
        return self.labelsnew


    def score(self, y_test):

        """ Returns the mean accuracy on the given test data and labels. """
        prav = []
        for i in range(len(y_test)):
            if y_test[i] == self.labelsnew[i]:
                prav.append(self.labelsnew[i])
        accuracy = len(prav)/len(y_test)
        return accuracy
