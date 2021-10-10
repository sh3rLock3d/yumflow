from sklearn.datasets import load_digits
digits = load_digits(as_frame=True)

x = digits.data
#y = digits.target
labels = ['pixel_0_1']
y = x[labels]
x = x.loc[:, ~x.columns.isin(labels)]
a = x.head()
print(str(y))

