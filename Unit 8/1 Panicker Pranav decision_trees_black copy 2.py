import matplotlib.pyplot as plt
from math import log2
import sys
from random import random, sample, shuffle, randint

sys.setrecursionlimit(2000)

def create_scatterplot(data_tup, x_label, y_label):
    x_data = [x[0] for x in data_tup]
    y_data = [x[1] for x in data_tup]
    plt.scatter(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()



def read_csv(filename):
    infolist = []
    with open(filename) as f:
        c = 0
        for line in f:
            if c == 0:
                featurelist = line.strip().split(",")
                c += 1
            else:
                line = line.strip().split(",")
                infolist.append(line)
    return (featurelist, infolist)

def read_bad_csv(filename):
    infolist = []
    counters = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    weird_data = []
    r_yes_votes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    r_no_votes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    d_yes_votes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    d_no_votes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open(filename) as f:
        c = 0
        for line in f:
            if c == 0:
                featurelist = line.strip().split(",")[1:]
                c += 1
            else:
                line = line.strip().split(",")[1:]
                if "?" not in line:
                    infolist.append(line)
                else:
                    weird_data.append(line)
                for index, feature in enumerate(line):
                    if feature == "y":
                        if line[len(line)-1] == "republican":
                            r_yes_votes[index] += 1
                        else:
                            d_yes_votes[index] += 1
                    elif feature == "n":
                        if line[len(line)-1] == "republican":
                            r_no_votes[index] += 1
                        else:
                            d_no_votes[index] += 1
        for point in weird_data:
            for index, value in enumerate(point):
                if value == "?":
                    party = point[len(point)-1]
                    if party == "republican":
                        if r_yes_votes[index] > r_no_votes[index]:
                            point[index] = "y"
                        else:
                            point[index] = "n"
                    if party == "democrat":
                        if d_yes_votes[index] > d_no_votes[index]:
                            point[index] = "y"
                        else:
                            point[index] = "n"
            #if "?" in point:
            infolist.append(point)
    #print(infolist)
        
    return (featurelist, infolist)

def split_data(infolist, index):
    data_categories = {}
    for l in infolist:
        feature = l[index]
        if feature not in data_categories:
            data_categories[feature] = []
        data_categories[feature].append(l)
    return data_categories

def find_entropy(infolist):
    freq_dict = {}
    entropy = 0
    for l in infolist:
        result = l[len(l)-1]
        if result in freq_dict:
            freq_dict[result] +=1
        else:
            freq_dict[result] = 1
    tot = sum(freq_dict.values())
    for key in freq_dict:
        frac = freq_dict[key]/tot
        entropy += frac*-log2(frac)
    return entropy

def find_best_classifier(featurelist, infolist):
    denominator = len(infolist)
    start_entropy = find_entropy(infolist)
    entropies = []
    split_datasets = []
    for i in range(len(infolist[0])-1):
        entropy = 0
        new_data = split_data(infolist, i)
        split_datasets.append(new_data)
        for key in new_data:
            numerator = len(new_data[key]) 
            entropy += numerator/denominator *  find_entropy(new_data[key])
        
        entropies.append(start_entropy - entropy)
    m = max(entropies)
    if m == 0.0:
        return ("","")
    m_ind = entropies.index(m)
    best = (split_datasets[m_ind],featurelist[m_ind])
    return best

def generate(featurelist,lists,name, depth, root):
    for key in lists:
        l = lists[key]
        newlists,newname = find_best_classifier(featurelist, l)
        if find_entropy(l) == 0.0:
            fin_str = key
            root[(name, depth)][(fin_str,depth+1)] = l[0][len(l[0])-1]
        elif newname == "":
            fin_str = key
            r = randint(0,len(l)-1)
            root[(name, depth)][(fin_str,depth+1)] = l[r][len(l[r])-1]
        else:
            root[(name,depth)][(key,depth+1)] = {}
            # if newname == "":
            #     print(root)
            #     continue
            newname += "?"
            root[(name,depth)][(key,depth+1)][newname, depth+2] = {}
            generate(featurelist, newlists, newname, depth+2,root[(name,depth)][(key,depth+1)])
    return root


def create_tree(featurelist, infolist):
    (lists, name) = find_best_classifier(featurelist, infolist)
    name += "?"
    root = {(name, 0): {}}
    return generate(featurelist, lists,name,  0, root)

def display_tree(dict):
    for key in dict:
        if isinstance(dict[key], str):
            s = ""
            name, depth = key
            for i in range(depth):
                s += "  "
            s += " * " + name + " --> " + dict[key]
            print(s)
        else:
            s = ""
            name, depth = key
            for i in range(depth):
                s += "  "
            s += " * " + name
            print(s)
            display_tree(dict[key]) 

def traverse_tree(feature_list, tree, test_point):
    for key in tree:
        l = tree[key]
        label = key[0][0:len(key[0])-1]
        if label=='': continue
        ind = feature_list.index(label)
        
        val = test_point[ind]
        for tup in l:
            if tup[0] == val:
                if isinstance(l[tup], str):
                    return l[tup]
                else:
                    return traverse_tree(feature_list, l[tup], test_point)
        for tup in l:
            if isinstance(l[tup], str):
                return l[tup]
            else:
                return traverse_tree(feature_list, l[tup], test_point)

def create_learning_curve(csv):
    featurelist, infolist = read_bad_csv(csv)
    test = infolist[len(infolist)-50:]
    train = infolist[0:len(infolist)-50]
    accuracies = []
    for size in range(5, len(train)):
        vals = sample(train, size)
        tree = create_tree(featurelist, vals)
        counter = 0
        for point in test:
            prediction = traverse_tree(featurelist, tree,point)
            actual = point[len(point)-1]
            if prediction == actual:
                counter += 1
        accuracies.append((size, counter/50*100))
    create_scatterplot(accuracies, "size", "percentage correct")

def learning_curve_decision_tree(csv, test_size, start_point, end_point, step):
#    featurelist, infolist = read_csv(csv)
    featurelist, infolist = read_bad_csv(csv)
    shuffle(infolist)
    test = infolist[len(infolist)-test_size:]
    train = infolist[0:len(infolist)-test_size]
    accuracies = []
    for size in range(start_point, end_point+1, step):
        print(size)
        vals = sample(train, size)
        tree = create_tree(featurelist, vals)
        #display_tree(tree)
        counter = 0
        for point in test:
            prediction = traverse_tree(featurelist, tree,point)
            actual = point[len(point)-1]
            if prediction == actual:
                counter += 1
        accuracies.append((size, counter/test_size*100))
    return accuracies

def learning_curve_random_forests(csv, test_size, start_point, end_point, step):
#    featurelist, infolist = read_bad_csv(csv)
    featurelist, infolist = read_bad_csv(csv)
    shuffle(infolist)
    test = infolist[len(infolist)-test_size:]
    train = infolist[0:len(infolist)-test_size]
    accuracies = []
    for size in range(start_point, end_point+1, step):
        print(size)
        trees = []
        counter = 0
        big_vals = sample(train, size)
        for i in range(10):
            small_vals = sample(big_vals, size//10)
            tree = create_tree(featurelist, small_vals)
            trees.append(tree)
        for point in test:
            predictions = []
            for tree in trees:
                print(tree)
                prediction = traverse_tree(featurelist, tree, point)
                predictions.append(prediction)
            actual = point[len(point)-1]
            prediction = max(set(predictions), key=predictions.count)
            if prediction == actual:
                counter += 1
            
        accuracies.append((size, counter/test_size*100))
    return accuracies
def compare_trees_forests(csv, test_size, start_point, end_point, step):
    tup1 = learning_curve_decision_tree(csv, test_size, start_point, end_point,step )
    tup2 = learning_curve_random_forests(csv, test_size, start_point, end_point,step )
    x_data_1 = [x[0] for x in tup1]
    y_data_1 = [x[1] for x in tup1]
    x_data_2 = [x[0] for x in tup2]
    y_data_2 = [x[1] for x in tup2]
    plt.scatter(x_data_1, y_data_1,color="red", label = "decision tree")
    plt.scatter(x_data_2,y_data_2, c='blue', label = "random forest")
    plt.xlabel("TRAINING SET SIZE")
    plt.ylabel("ACCURACY")
    plt.legend()
    plt.title(csv[:-4])
    plt.show()
    

#compare_trees_forests(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),int(sys.argv[5])) 
compare_trees_forests("house-votes-84.csv", 50,20,350,5)
#compare_trees_forests("nursery.csv", 500, 500, 12000, 500)
#compare_trees_forests("connect-four.csv", 7000, 5000, 60000,5000)