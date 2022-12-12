import argparse

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split as tts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import asyncio
from argparse import ArgumentParser
import time

LOW_NEIGHBOR = 1
HIGH_NEIGHBOR = 9


class Tester:
    def __init__(self, inputDir, testSize, randomState):
        self.inputDir = inputDir
        self.testSize = testSize
        self.randomState = randomState

    async def read_file(self, path):
        y = []
        df = pd.read_csv(path)
        x_arr = df[["alphas", "theta", "phi"]].to_numpy()

        if("Natural" in path):
            y.append(0)
        else:
            y.append(1)

        return x_arr, y

    async def read_files(self):
        tasks = []
        for filename in os.listdir(self.inputDir):
            file = os.path.join(self.inputDir, filename)
            if os.path.isfile(file) and ".csv" in file:
                tasks.append(asyncio.ensure_future(self.read_file(file)))
        training_arr = await asyncio.gather(*tasks)

        data = []
        labels = []
        for val in training_arr:
            data.append(val[0].flatten())
            labels.append(val[1][0])

        return data, labels

    async def grab_clean_and_split(self):
        data, labels = await self.read_files()
        np_data = np.array(data, dtype=object)
        biggest_list_length = len(max(np_data, key=len))
        for i, x in enumerate(np_data):
            list_length = len(x)
            zeros_length = biggest_list_length - list_length
            np_data[i] = np.concatenate((x, np.zeros(zeros_length)), axis=None)

        data_train, data_test, labels_train, labels_test = tts(np_data, labels, test_size=self.testSize, random_state=self.randomState)
        return data_train, data_test, labels_train, labels_test

    async def train_knn(self):
        data_train, data_test, labels_train, labels_test = await self.grab_clean_and_split()
        np.asarray(data_train)

        neighbors = np.arange(LOW_NEIGHBOR, HIGH_NEIGHBOR)

        train_acc = []
        test_acc = []
        for i, k in enumerate(neighbors):
            print("Testing...", i)
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(list(data_train), labels_train)

            train_acc.append(knn.score(list(data_train), labels_train))
            test_acc.append(knn.score(list(data_test), labels_test))

        plt.plot(neighbors, test_acc, label='Testing dataset Accuracy')
        plt.plot(neighbors, train_acc, label='Training dataset Accuracy')

        plt.legend()
        plt.xlabel('n_neighbors')
        plt.ylabel('Accuracy')
        plt.show()

def check_positive_float(val):
    fvalue = float(val)
    if fvalue <= 0 and fvalue > 1:
        raise argparse.ArgumentTypeError("%s is an invalid positive float value" % val)
    return fvalue

def check_positive_int(val):
    ivalue = int(val)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('%s is an invalid positive int value' % val)
    return ivalue

async def main():
    parser = ArgumentParser()
    parser.add_argument('-id', '--input_dir',
                        dest='input_dir',
                        help='The directory that contains all csvs for mound data alphas, phis, thetas',
                        required=True)
    parser.add_argument('-ts', '--test_size',
                        type=check_positive_float,
                        dest='test_size',
                        help='The test size for train test split',
                        default=0.2)
    parser.add_argument('-rs', '--random_state',
                        type=check_positive_int,
                        dest='random_state',
                        help='Random state for testing',
                        default=42)

    args = parser.parse_args()
    input_dir = args.input_dir
    test_size = args.test_size
    random_state = args.random_state

    tester = Tester(input_dir, test_size, random_state)
    await tester.train_knn()

if __name__ == "__main__":
    asyncio.run(main())