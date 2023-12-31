# -*- coding: utf-8 -*-
"""comite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BFhpOCMgwCxAVPuGaBMIWaA400o1DN0X
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import numpy as np
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.preprocessing import Normalizer
import graphviz

dadosAcademicos = pd.read_excel('dataset.xlsx')

dadosAcademicos = dadosAcademicos[dadosAcademicos['Target'] != 'Enrolled']

mapeamento = {'Graduate': 1, 'Dropout': 0}
dadosAcademicos['Target'] = dadosAcademicos['Target'].map(mapeamento)

colunas_para_remover = ['Application mode', 'Gender', 'Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)', 'GDP', 'Unemployment rate', 'Inflation rate', 'Application order']
dadosAcademicos = dadosAcademicos.drop(colunas_para_remover, axis=1)

X = dadosAcademicos.iloc[:, :-1]
y = dadosAcademicos['Target']

print(dadosAcademicos)

#ARVORE DE DECISÃO

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3)
clf = clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

print("\nMatriz de confusão detalhada:\n",
      pd.crosstab(y_test, predictions, rownames=['Real'], colnames=['Predito'], margins=True, margins_name='Todos'))

print("Relatório sobre a qualidade:\n")
print(metrics.classification_report(y_test, predictions, target_names=['Graduate', 'Dropout']))

# Calcular a acurácia do modelo
acuracia = metrics.accuracy_score(y_test, predictions)
print("Acurácia do modelo:", acuracia)

#KNN

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

# Criando o objeto KNN
knn = KNeighborsClassifier(n_neighbors=7)

# Ajustando o modelo aos dados de treinamento
knn.fit(X_train, y_train)

# Fazendo previsões nos dados de teste
y_pred = knn.predict(X_test)

# Calculando a acurácia do modelo
accuracy = accuracy_score(y_test, y_pred)
print("Acurácia: %.2f" % accuracy)

# Fazer previsões nos dados de teste
y_pred = knn.predict(X_test)

# Criar a matriz de confusão
confusion_mat = confusion_matrix(y_test, y_pred)

print("Matriz de Confusão:")
print(confusion_mat)

print(metrics.classification_report(y_test, y_pred, target_names=['Graduate', 'Dropout']))

#PAIRPLOT GRAFICO DE CRUZAMENTO DE DADOS
#sns.pairplot( data=df_iris, vars=('sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm
#)'), hue='target' )
#df_iris.describe()

#NAIVE BAYES

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

#instanciando o modelo
modeloKNN = KNeighborsClassifier()

#treinando o modelo utilizando o conjunto de treino
modeloKNN.fit(X_train, y_train)

#validando o modelo utilizando o conjunto de teste
precisaoKNN = str(round(modeloKNN.score(X_test, y_test) * 100, 2)) + "%"

#imprimindo o resultado
print("A acurácia do modelo k-nn", precisaoKNN)

# predizendo o teste
y_pred = modeloKNN.predict(X_test)

#comparando predição com o real
print(classification_report(y_test, y_pred))
#---------------------------------------------------------------------------------------------------------------
#naive Bayes
#cria um classificador Guassiano
modeloNB = GaussianNB()

#Treinando o modelo usando os ajustes de treinamento
modeloNB.fit(X_train, y_train)

#validando o modelo utilizando o conjunto de teste
precisaoNB = str(round(modeloNB.score(X_test, y_test)* 100, 2)) + "%"

#imprimindo o resultado
print("A acurácia do modelo Naive Bayes foi",precisaoNB)

#predizendo o teste
y_pred = modeloNB.predict(X_test)

#comparando predição com o real
print(classification_report(y_test, y_pred))

#normalizando
scaler = Normalizer()
scaler.fit(X)
X = scaler.transform(X)
scoresKNN = []
scoresNB = []
for i in range (2000):
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    modeloKNN = KNeighborsClassifier()
    modeloKNN.fit(X_train, y_train)
    precisaoKNN = modeloKNN.score(X_test, y_test)
    scoresKNN.append(precisaoKNN)
    modeloNB = GaussianNB()
    modeloNB.fit(X_train, y_train)
    precisaoNB = modeloKNN.score(X_test, y_test)
    scoresNB.append(precisaoNB)

print("Média do KNN: {:.2f}%".format(np.mean(scoresKNN)*100))
print("Desvio padrão do KNN: {:.2f}%".format(np.std(scoresKNN)*100))

print("Média do Naive Bayes: {:.2f}%".format(np.mean(scoresNB)*100))
print("Desvio padrão do Naive Bayes: {:.2f}%".format(np.std(scoresNB)*100))

sns.distplot(scoresKNN, hist_kws={'rwidth':0.8})
plt.yticks([])
plt.title("Acurácias do KNN")
plt.show()

sns.distplot(scoresNB, hist_kws={'rwidth':0.8})
plt.yticks([])
plt.title("Acurácias do Naive Bayers")
plt.show()

# COMITÊ DE CLASSIFICADORES #

tot_formado = 0
tot_abandonado = 0

lista_dados = [1,5,1,1,1,22,27,10,10,1,0,0,0,0,19,0,0,6,0,0,0,0,6,0,0,0]

pred_arv = (clf.predict([lista_dados]))
if pred_arv == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

pred_nb = (modeloNB.predict([lista_dados]))
if pred_nb == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

pred_knn = (knn.predict([lista_dados]))
if pred_knn == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

if tot_formado >= 2:
  print("O comitê acredita que o aluno se formou.")
else:
  print("O comitê acredita que o aluno abandonou o curso.")

if tot_formado == 3 or tot_abandonado == 3:
  print("O comitê é unânime na opinião.")
else:
  print("O comitê não é unânime na opinião.")

print(tot_formado)
print(tot_abandonado)

# COMITÊ DE CLASSIFICADORES #

tot_formado = 0
tot_abandonado = 0

lista_dados = [1,6,1,1,1,13,28,5,8,1,0,0,1,0,19,0,0,6,15,6,0,0,6,13,6,0]

pred_arv = (clf.predict([lista_dados]))
if pred_arv == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

pred_nb = (modeloNB.predict([lista_dados]))
if pred_nb == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

pred_knn = (knn.predict([lista_dados]))
if pred_knn == 0 :
  tot_abandonado = tot_abandonado + 1
else:
  tot_formado = tot_formado + 1

if tot_formado >= 2:
  print("O comitê acredita que o aluno se formou.")
else:
  print("O comitê acredita que o aluno abandonou o curso.")

if tot_formado == 3 or tot_abandonado == 3:
  print("O comitê é unânime na opinião.")
else:
  print("O comitê não é unânime na opinião.")

print(tot_formado)
print(tot_abandonado)

feature_names = [str(col) for col in dadosAcademicos.columns.tolist()[:-1]]

class_names = dadosAcademicos['Target'].astype(str).tolist()

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("Dados Academicos")
dot_data = tree.export_graphviz(clf, out_file=None,
feature_names=feature_names,
class_names=class_names,
filled=True, rounded=True,
special_characters=True)
graph = graphviz.Source(dot_data, format="png")
graph

sns.pairplot(dadosAcademicos, hue='Target')
plt.show()