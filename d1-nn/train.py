from package.data import get_character
from package.data import get_data
import matplotlib.pyplot as plt
import cv2 as opencv
import numpy as np
import random
import os
import sys
import argparse
import tensorflow.keras as keras
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print("Using tensorflow :", tf.__version__)


def get_model():
    '''
    This method will define the tensorflow model, compile it and return
    the compiled model
    '''
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(end_nodes, activation=tf.nn.softmax)
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def train_model(matrixvalue, matrixlabel, model_name, test_epoch=5, train_epoch=20):
    '''
    This method will train the compiled model based on the numpy arrays that is generated
    with values and labels. And then trained model is saved in data/hindi-num.model
    '''
    values, labels = get_data("data/%s" % (matrixvalue), "data/%s" % (matrixlabel))
    values = tf.keras.utils.normalize(values, axis=1)
    model = get_model()
    print(values.shape, labels.shape)
    session = model.fit(values, labels, epochs=train_epoch)
    print("----\nTesting\n----")
    history = model.fit(values, labels, epochs=test_epoch)
    print("Test Loss :", history)
    print("Test Accuracy :", history)
    model.save("data/%s" % (model_name))


def test_model(matrixvalue, matrixlabel, model_name, label_type):
    '''
    This method will load the saved model and test the model with randomly fetched
    values from the numpy array and plots them in the graph
    '''
    values, labels = get_data("data/%s" % (matrixvalue), "data/%s" % (matrixlabel))
    saved_model = tf.keras.models.load_model('data/%s' % (model_name))
    prediction = saved_model.predict(values)
    grid = 3
    for i in range(1, grid*grid+1):
        index = random.randint(0, len(values))
        getmax = np.argmax(prediction[index])
        plt.subplot(grid, grid, i).set_title(get_character(getmax, label_type))
        plt.imshow(values[index], cmap="gray", interpolation="nearest")
    plt.show()


if __name__ == "__main__":
    # Parsing the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset", help="Name of training and testing dataset. USAGE: -v - vowel, -c - consonant, -n - numeral")
    val = parser.parse_args()
    if val.dataset == "-v":
        print("Using vowel dataset. .")
        value_name = "vowel_value.npy"
        label_name = "vowel_label.npy"
        model_name = "vowel_model.model"
        label_type = "vowels"
        end_nodes = 13
    elif val.dataset == "-c":
        print("Using consonant dataset. .")
        value_name = "consonant_value.npy"
        label_name = "consonant_label.npy"
        model_name = "consonant_model.model"
        label_type = "consonants"
        end_nodes = 37
    else:
        print("Using numeral dataset. .")
        value_name = "numeral_value.npy"
        label_name = "numeral_label.npy"
        model_name = "numeral_model.model"
        label_type = "numerals"
        end_nodes = 10

    # Calling the methods
    train_model(value_name, label_name, model_name)  # This will generate the trained model
    # This will load the model and predict the values
    test_model(value_name, label_name, model_name, label_type)
