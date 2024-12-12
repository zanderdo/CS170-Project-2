"""
Group:
Alexander Dobmeier, adobm001, Section 24

DatasetID: this was not mentioned anywhere else in the 
  instructions and I have no idea what is supposed to go here

Small Dataset Results:
  Forward: Feature Subset: {4,2}, Acc: 92%
  Backward: Feature Subset: {0, 1, 3, 4, 6, 8, 9}, Acc: 78%

Large Dataset Results:
  Forward: Feature Subset: {26, 0}, Acc: 95.5%
  Backward: Feature Subset: {0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39}, Acc: 71.7%

Titanic Dataset Results:
  Forward: Feature Subset: {1}, Acc: 78.0%
  Backward: Feature Subset: {0, 1, 3, 4}, Acc: 76.3%
"""


import random
import math
import numpy
import time

class Classifier:
    def __init__(self):
        self.training_data = [[]]
        self.feature_maxes = []

    def train(self, training_data: list[list]):
        self.training_data = training_data

    def normalize(self):
        for feature in range(1, len(self.training_data[0])):
            curr_max = self.training_data[0][feature]
            for curr_point in self.training_data:
                if curr_point[feature] > curr_max:
                    curr_max = curr_point[feature]
            self.feature_maxes.append(curr_max)
            for curr_point in self.training_data:
                curr_point[feature] = curr_point[feature] / curr_max

    def test(self, point, features):
        distances = []

        for test_point in self.training_data:
            sum = 0
            for i in range(len(point)):
                if i in features:
                    sum += (point[i] - test_point[i + 1])**2
            distances.append(math.sqrt(sum))
        min_index = numpy.argmin(distances)
        return self.training_data[min_index][0]

class Validator:
    def validate(self, numbers, features):
        start_time = time.time()
        right = 0
        wrong = 0

        classifier = Classifier()
        for i in range(len(numbers)):
            curr_testdata = numbers.copy()
            del curr_testdata[i]
            classifier.train(curr_testdata)
            curr_point = numbers[i].copy()
            del curr_point[0]
            classification = classifier.test(curr_point, features)
            if classification == numbers[i][0]:
                right += 1
            else:
                wrong += 1
            # print(f"Trained and tested without point {i}, classified as {classification}, actual was {numbers[i][0]} and took {elapsed_time}s")

        elapsed_time = time.time() - start_time
        accuracy = right / (right + wrong)
        print(f'Accuracy: {accuracy}, got {right}/{wrong + right} correct!  Took {elapsed_time}s')
        return accuracy

def Rate_Node() -> float:
    return random.random() * 100

def Forward_Selection(raw_data, feature_list, curr_features, curr_accuracy):
    if len(feature_list) == len(curr_features):
        print(f"Finished search!  The subset {curr_features} is best with accuracy {curr_accuracy}")
        return
    best_accuracy = 0.0
    best_index = 0
    for i in feature_list:
        if i in curr_features:
            continue
        curr_features.append(i)
        validatussy = Validator()
        accuracy = validatussy.validate(raw_data, curr_features)
        print(f"Using feature(s) {curr_features} accuracy is {accuracy}")
        curr_features.pop()
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_index = i
    if best_accuracy < curr_accuracy:
        print("Accuracy Decreased!")
        print(f"Finished search!  The subset {curr_features} is best with accuracy {curr_accuracy}")
        return
    else:
        curr_features.append(best_index)
        print(f"Feature set {curr_features} is the best, accuracy was {best_accuracy}")
        Forward_Selection(raw_data, feature_list, curr_features, best_accuracy)
        

    

def Backward_Elimination(raw_data, feature_list: list[int], curr_features: list[int], curr_accuracy):
    if len(curr_features) == 1:
        print(f"Finished search!  The subset{curr_features} is the best with accuracy {curr_accuracy}")
        return
    if curr_accuracy > 90:
        print(f"Accuracy surpassed 90%, search complete!")
        print(f"Best features are {curr_features} and accuracy is {curr_accuracy}")
        return
    if len(feature_list) == len(curr_features):
        curr_accuracy = 0
    highest_accuracy = 0
    highest_index = 0
    for i, j in enumerate(curr_features):
        if i not in curr_features:
            continue
        test_features = curr_features.copy()
        test_features.remove(i)
        validatussy = Validator()
        accuracy = validatussy.validate(raw_data, test_features)
        print(f"Accuracy without feature {j} is {accuracy}")
        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            highest_index = i
    highest_loss = highest_accuracy - curr_accuracy
    print(f"CURR = {curr_accuracy}, LOSS = {highest_loss}")
    new_accuracy = highest_accuracy
    print(f"Dropping feature {curr_features[highest_index]}, new accuracy is {new_accuracy}, loss is {highest_loss}")
    if highest_loss < 0.01:
        print(f"Accuracy gain < 5%, search complete")
        print(f"Best features are {curr_features} and accuracy is {curr_accuracy}")
        return
    curr_features.remove(highest_index)
    Backward_Elimination(raw_data, feature_list, curr_features, new_accuracy)

def Nearest_Neighbor(testdata_path, test_features):
    # testdata_path = input("Enter the path to the data you'd like to use: ")
    # test_features = input("Enter the features you'd like to test separated by spaces: ")
    # features = test_features.split()
    # features = list(map(int, features))
    # credit to stack overflow for the code
    validator = Validator()
    # validator.validate(numbers, test_features)

def main():
    testdata_path = input("Enter the path to the data you'd like to use: ")
    with open(testdata_path, "r") as file:
        lines = file.readlines()
    raw_data = [[]]
    for line in lines:
        raw_data.extend([[float(x) for x in line.split()]])
    del raw_data[0]
    num_features = input("Please enter total number of features: ")
    feature_list = []
    for i in range(int(num_features)):
        feature_list.append(i)

    print("\nPlease type the number of the algorithm you want to run")
    print("\n(1) Forward Selection")
    print("\n(2) Backward Elimination")
    print("\n(3) Nearest Neighbor")
    selected_algorithm = int(input(""))

    match selected_algorithm:
        case 1:
            Forward_Selection(raw_data, feature_list, [], 0)

        case 2:
            Backward_Elimination(raw_data, feature_list, feature_list.copy(), 0)
        
        case 3:
            Nearest_Neighbor()

if __name__ == "__main__":
    main()