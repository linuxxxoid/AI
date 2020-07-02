import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from sklearn.metrics import accuracy_score
import tensorflow as tf
import keras
import keras.models as M
import keras.layers as L
import keras.backend as K
from keras.optimizers import SGD

plt.rcParams['figure.figsize'] = (7,7)


def split_train_test(data, test_ratio, state = 7):    
    shuffled_indices = np.random.RandomState(seed=state).permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return train_indices, test_indices 

def get_size(path, classes):
    size = 0
    for cl in classes:
        size += len(next(os.walk(path + cl))[2])
    ans = [size]
    one_path = path + classes[0] + '/' + next(os.walk(path + classes[0]))[2][0]
    one_im = cv2.imread(one_path)
    ans.extend(list(one_im.shape))
    return tuple(ans)


def img_data_reader(path, classes):
    if path[-1] != '/':
        path += '/'
    size = get_size(path, classes)
    X_cols = np.zeros(size).astype(np.uint8)
    Y_cols = np.zeros((size[0], len(classes))).astype(np.uint8)
    last_bound = 0
    for i in range(len(classes)):
        images = next(os.walk(path + classes[i]))[2]
        for j in range(len(images)):
            X_cols[last_bound + j] = cv2.imread(path + classes[i] + '/' + images[j])
            Y_cols[last_bound + j][i] = 1
        last_bound += len(images)
    return X_cols, Y_cols


classes = ['good', 'bad', 'ugly']
path_to_lina = '/Users/linuxoid/desktop/vuzich/ai/lab2/data/lina/'
path_to_max = '/Users/linuxoid/desktop/vuzich/ai/lab2/data/max/'
path_to_roma = '/Users/linuxoid/desktop/vuzich/ai/lab2/data/roma/'

X_max, Y_max = img_data_reader(path_to_max, classes)
X_lina, Y_lina = img_data_reader(path_to_lina, classes)
X_roma, Y_roma = img_data_reader(path_to_roma, classes)


X_train_1 = np.concatenate([X_max, X_lina])
Y_train_1 = np.concatenate([Y_max, Y_lina])

X_test_1 = X_roma
Y_test_1 = Y_roma

X_full = np.concatenate([X_max, X_lina, X_roma])
Y_full = np.concatenate([Y_max, Y_lina, Y_roma])

train_i, test_i = split_train_test(X_full, 0.2)

X_train_2, Y_train_2 = X_full[train_i], Y_full[train_i]
X_test_2, Y_test_2 = X_full[test_i], Y_full[test_i]


X_train_1 = X_train_1.astype(np.float32) / 255.0
X_test_1 = X_test_1.astype(np.float32) / 255.0

X_train_2 = X_train_2.astype(np.float32) / 255.0
X_test_2 = X_test_2.astype(np.float32) / 255.0

epc = 120
batch = 50
k_size = 3 
hidden_size_1 = 256
hidden_size_2 = 128
hidden_size_3 = 64


K.clear_session()


#one layer
"""
model_one = M.Sequential()
model_one.add(L.Flatten())
model_one.add(L.Dense(output_dim = len(classes), input_shape=(k_size,), activation='softmax'))


model_one.compile(
	loss='categorical_crossentropy',
	optimizer='adam',
	metrics=['accuracy']
)

hist = model_one.fit(
	X_train_2,
	Y_train_2,
	batch_size = batch,
	epochs = epc,
	validation_data=(X_test_2, Y_test_2)
)

test_acc = model_one.evaluate(X_train_2,  Y_train_2, verbose = 2)
print("\nТочность на тренировочных(обучающих) данных: %.3f" % test_acc[1])
print("%s: %.3f" % (model_one.metrics_names[0], test_acc[0])) # loss (потери)


test_acc = model_one.evaluate(X_test_2,  Y_test_2, verbose = 2)
print("\nТочность на проверочных(тестовых) данных: %.3f" % test_acc[1])
print("%s: %.3f" % (model_one.metrics_names[0], test_acc[0])) # loss (потери)

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

"""

#many layers

inputer_layer = L.Input(shape = X_train_2.shape[1:])
flat = L.Flatten(input_shape = X_train_2.shape[1:])(inputer_layer)

layer_1 = L.Dense(
	output_dim = hidden_size_2,
	input_shape=(3,),
	kernel_initializer = 'random_uniform',
	activation = 'relu')(flat)

layer_2 = L.Dense(
	output_dim = hidden_size_3,
	kernel_initializer = 'random_uniform',
	activation = 'relu')(layer_1)

layer_3 = L.Dense(
	output_dim = hidden_size_3,
	kernel_initializer = 'random_uniform',
	activation = 'relu')(layer_2)

outputer_layer = L.Dense(
	output_dim = len(classes),
	activation = 'softmax')(layer_2)


model_two = M.Model(input = inputer_layer, output = outputer_layer)

model_two.compile(
	loss='categorical_crossentropy',
	optimizer='adam',
	metrics=['accuracy']
)

history = model_two.fit(
	X_train_2,
	Y_train_2,
	batch_size = batch,
	epochs = epc,
	validation_data=(X_test_2, Y_test_2)
)

test_acc = model_two.evaluate(X_train_2,  Y_train_2, verbose = 2)
print('\nТочность на тренировочных(обучающих) данных:', test_acc[1])
print("%s: %.3f" % (model_two.metrics_names[0], test_acc[0])) # loss (потери)


test_acc = model_two.evaluate(X_test_2,  Y_test_2, verbose = 2)
print('\nТочность на проверочных(тестовых) данных:', test_acc[1])
print("%s: %.3f" % (model_two.metrics_names[0], test_acc[0])) # loss (потери)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

