import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

'''dataset'''
digits = datasets.load_digits()

# print digits.data
# print digits.target
# print digits.images[0]
# print len(digits.data)

'''training'''
clf = svm.SVC(gamma=0.001, C=100)
x,y = digits.data[:-10],digits.target[:-10]
clf.fit(x,y)

'''testing'''
print 'Prediction:',clf.predict(digits.data[[-3]])
plt.imshow(digits.images[-3], cmap=plt.cm.gray_r, interpolation = "nearest")
plt.show()