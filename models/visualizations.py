import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from collections import OrderedDict
import re
from sklearn.externals import joblib
from prep_data import *


# data files
EXPERIMENT_1 = 'data/experiment1_data.csv'
EXPERIMENT_2 = 'data/experiment2_data.csv'


def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def top_predictors(rf, x_train):
    '''
    for a random forest model will show the best predictors

    rf - random forest classifier class
    x_train - training data for the rf
    '''
    var_names = list(x_train)
    var_scores = rf.feature_importances_

    var_selection = dict(zip(var_names, var_scores))
    var_selection = OrderedDict(sorted(var_selection.items(), key=lambda t: t[1]))

    plt.rcParams.update({'font.size':3})
    plt.figure(figsize=(5, 15))
    plt.barh(range(len(var_selection)), list(var_selection.values()), align='center')
    plt.yticks(range(len(var_selection)), list(var_selection.keys()))
    plt.show()


def load_model(model_name):
    '''
    loads a saved model
    '''
    path = 'saved_models/' + model_name
    model = joblib.load(path)

    return model


def display_confusion_matrix(model_name):
    '''
    given a model will display the confusion matrix
    '''
    model = load_model(model_name)

    s = model_name.replace('.', '_')
    s = s.split('_')

    if s[0] == 'e1':
        data = EXPERIMENT_1
        states = EXP1_STATES
        class_names = ['0', '1', '2', '3', '4', '5']
    elif s[0] == 'e2':
        data = EXPERIMENT_2
        states = EXP2_STATES
        class_names = ['0', '1', '2', '3', '4', '5', '6', '7',
               '8', '9', '10', '11', '12', '13', '14', '15']

    mode = int(s[4])

    if s[1] == 'binary':
        x_train, x_test, y_train, y_test = binary_prep(data, mode, seed=None)
        class_names = ['1', '0']
    elif s[1] == 'app':
        x_train, x_test, y_train, y_test = app_prep(data, mode, seed=None)
        class_names = ['0', '1', '2', '3', '4', '5']
    elif s[1] == 'state':
        x_train, x_test, y_train, y_test = state_prep(data, mode, states, seed=None)

    y_pred = model.predict(x_test)
    cnf_matrix = confusion_matrix(y_test, y_pred)
    plt.rcParams.update({'font.size':10})
    plt.figure(figsize=(8, 8))
    plot_confusion_matrix(cnf_matrix, classes=class_names, title='Confusion Matrix')
    plt.show()


def results_from_file(filename):
    '''
    '''
    path = 'model_results/' + filename
    f = open(path)
    f = f.read()
    f = f.replace('\t', '')
    f = f.replace('\n', '')
    f = f.replace(' ', '')

    pattern = 'TestData:Score:([0-9.]+)'
    result = re.findall(pattern, f)

    return float(result[0])


def autolabel(rects, ax):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%.2f'%(h),
                ha='center', va='bottom')


def graph_binary_results():
    '''
    graph results from binary models
    '''
    plt.style.use('ggplot')
    plt.rc('font', size=12)
    # first graph the binary classification results together
    # only random forest results were saved because the other results were bad
    e1_binary = ['e1_binary_rf_m_3.txt', 'e1_binary_rf_m_4.txt']
    e2_binary = ['e2_binary_rf_m_3.txt', 'e2_binary_rf_m_4.txt']
    # first value is for mode 3 and second value is for mode 4
    e1 = [results_from_file(f) for f in e1_binary]
    e2 = [results_from_file(f) for f in e2_binary]
    x_labels = ['With App Data', 'Without App Data']

    N = 2
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, e1, width)
    rects2 = ax.bar(ind+width, e2, width)

    plt.title('Binary Classification')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_labels)
    ax.legend((rects1[0], rects2[0]), ('Experiment 1', 'Experiment 2'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    plt.show()


def graph_app_results():
    '''
    graph results from application models

    For this I will need to make 2 graphs, one for mode 3 and one for mode 4
    '''
    plt.style.use('ggplot')
    plt.rc('font', size=12)
    # mode 3 graph
    rf = ['e1_app_rf_m_3.txt', 'e2_app_rf_m_3.txt']
    ab = ['e1_app_ab_m_3.txt', 'e2_app_ab_m_3.txt']
    gb = ['e1_app_gb_m_3.txt', 'e2_app_gb_m_3.txt']
    x_labels = ['Experiment 1', 'Experiment 2']
    rf = [results_from_file(f) for f in rf]
    ab = [results_from_file(f) for f in ab]
    gb = [results_from_file(f) for f in gb]

    N = 2
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, rf, width)
    rects2 = ax.bar(ind+width, ab, width)
    rects3 = ax.bar(ind+width*2, gb, width)

    plt.title('Application Classification (With State Data)')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_labels)
    ax.legend((rects1[0], rects2[0], rects3[0]), \
                ('Random Forest', 'Adaboost', 'Gradientboost'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    plt.show()

    # mode 4 graph
    rf = ['e1_app_rf_m_4.txt', 'e2_app_rf_m_4.txt']
    ab = ['e1_app_ab_m_4.txt', 'e2_app_ab_m_4.txt']
    gb = ['e1_app_gb_m_4.txt', 'e2_app_gb_m_4.txt']
    x_labels = ['Experiment 1', 'Experiment 2']
    rf = [results_from_file(f) for f in rf]
    ab = [results_from_file(f) for f in ab]
    gb = [results_from_file(f) for f in gb]

    N = 2
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, rf, width)
    rects2 = ax.bar(ind+width, ab, width)
    rects3 = ax.bar(ind+width*2, gb, width)

    plt.title('Application Classification (Without State Data)')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_labels)
    ax.legend((rects1[0], rects2[0], rects3[0]), \
                ('Random Forest', 'Adaboost', 'Gradientboost'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    plt.show()


def graph_state_results():
    '''
    graph results from state models
    '''
    plt.style.use('ggplot')
    plt.rc('font', size=12)
    # mode 1 graph
    rf = ['e1_state_rf_m_1.txt', 'e2_state_rf_m_1.txt']
    ab = ['e1_state_ab_m_1.txt', 'e2_state_ab_m_1.txt']
    gb = ['e1_state_gb_m_1.txt', 'e2_state_gb_m_1.txt']
    x_labels = ['Experiment 1', 'Experiment 2']
    rf = [results_from_file(f) for f in rf]
    ab = [results_from_file(f) for f in ab]
    gb = [results_from_file(f) for f in gb]

    N = 2
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, rf, width)
    rects2 = ax.bar(ind+width, ab, width)
    rects3 = ax.bar(ind+width*2, gb, width)

    plt.title('State Classification (Access)')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_labels)
    ax.legend((rects1[0], rects2[0], rects3[0]), \
                ('Random Forest', 'Adaboost', 'Gradientboost'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    plt.show()

    # mode 4 graph
    rf = ['e2_state_rf_m_4.txt']
    ab = ['e2_state_ab_m_4.txt']
    gb = ['e2_state_gb_m_4.txt']
    x_labels = ['Experiment 2']
    rf = [results_from_file(f) for f in rf]
    ab = [results_from_file(f) for f in ab]
    gb = [results_from_file(f) for f in gb]

    N = 1
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, rf, width)
    rects2 = ax.bar(ind+width, ab, width)
    rects3 = ax.bar(ind+width*2, gb, width)

    plt.title('State Classification (No Access)')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_labels)
    ax.legend((rects1[0], rects2[0], rects3[0]), \
                ('Random Forest', 'Adaboost', 'Gradientboost'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    plt.show()
