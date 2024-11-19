import random

def Rate_Node() -> float:
    return random.random() * 100

def Forward_Selection(feature_list, curr_features, curr_accuracy):
    if len(feature_list) == len(curr_features):
        print(f"Finished search!  The subset {curr_features} is best with accuracy {curr_accuracy}")
        return
    best_accuracy = 0.0
    best_index = 0
    for i in feature_list:
        if i in curr_features:
            continue
        accuracy = Rate_Node()
        curr_features.append(i)
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
        Forward_Selection(feature_list, curr_features, best_accuracy)
        

    

def Backward_Elimination(feature_list: list[int], curr_features: list[int], curr_accuracy):
    if len(curr_features) == 1:
        print(f"Finished search!  The subset{curr_features} is the best with accuracy {curr_accuracy}")
        return
    if curr_accuracy > 90:
        print(f"Accuracy surpassed 90%, search complete!")
        print(f"Best features are {curr_features} and accuracy is {curr_accuracy}")
        return
    if len(feature_list) == len(curr_features):
        curr_accuracy = 0
    worst_accuracy = 101.0
    worst_index = 0
    for i, j in enumerate(curr_features):
        if i not in curr_features:
            continue
        accuracy = Rate_Node()
        print(f"Feature {j}'s impact is {accuracy}")
        if accuracy < worst_accuracy:
            worst_accuracy = accuracy
            worst_index = i
    gain = random.random() * 40
    print(f"CURR = {curr_accuracy}, GAIN = {gain}")
    new_accuracy = curr_accuracy + gain
    print(f"Dropping feature {curr_features[worst_index]}, new accuracy is {new_accuracy}")
    if new_accuracy - curr_accuracy < 5:
        print(f"Accuracy gain < 5%, search complete")
        print(f"Best features are {curr_features} and accuracy is {curr_accuracy}")
        return
    curr_features.remove(worst_index)
    Backward_Elimination(feature_list, curr_features, new_accuracy)
    


def main():
    num_features = input("Please enter total number of features: ")
    feature_list = []
    for i in range(int(num_features)):
        feature_list.append(i)

    print("\nPlease type the number of the algorithm you want to run")
    print("\n(1) Forward Selection")
    print("\n(2) Backward Elimination")
    selected_algorithm = int(input(""))

    match selected_algorithm:
        case 1:
            Forward_Selection(feature_list, [], 0)

        case 2:
            Backward_Elimination(feature_list, feature_list.copy(), 0)

if __name__ == "__main__":
    main()