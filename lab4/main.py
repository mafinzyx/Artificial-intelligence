import numpy as np
import time

from decision_tree import DecisionTree
from random_forest import RandomForest
from load_data import generate_data, load_titanic

def main():
    np.random.seed(123)

    train_data, test_data = load_titanic()
    
    print("\n\nDecisionTree:")
    start_time = time.time()
    dt = DecisionTree({"depth": 14})
    dt.train(*train_data)
    dt.evaluate(*train_data)
    dt.evaluate(*test_data)
    end_time = time.time()
    total_time = end_time - start_time
    print("Time: ", total_time)

    print("\nRandomForest:")
    start_time = time.time()
    rf = RandomForest({"ntrees": 10, "feature_subset": 2, "depth": 14})
    rf.train(*train_data)
    rf.evaluate(*train_data)
    rf.evaluate(*test_data)
    end_time = time.time()
    total_time = end_time - start_time
    print("Time: ", total_time)
    

if __name__=="__main__":
    main()