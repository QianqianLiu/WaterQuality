import os
import pandas as pd
import numpy as np

def calculate_F1_metrics(file):
    data = pd.read_csv(file)
    ground_truth = data.loc[:, "Groud_Truth"].to_numpy()
    prediction = data.loc[:, "Prediction"].to_numpy()
    true_positive = np.sum(np.logical_and(ground_truth > ALGAL_BLOOM_THRESHOLD, prediction > ALGAL_BLOOM_THRESHOLD))
    false_positive = np.sum(np.logical_and(ground_truth <= ALGAL_BLOOM_THRESHOLD, prediction > ALGAL_BLOOM_THRESHOLD))
    true_negative = np.sum(np.logical_and(ground_truth <= ALGAL_BLOOM_THRESHOLD, prediction <= ALGAL_BLOOM_THRESHOLD))
    false_negative = np.sum(np.logical_and(ground_truth > ALGAL_BLOOM_THRESHOLD, prediction <= ALGAL_BLOOM_THRESHOLD))
    return true_positive, false_positive, true_negative, false_negative

folder = "data/Result/LSTM"
dataset = "NRE" # "NRE" or "Scripps Pier"
ALGAL_BLOOM_THRESHOLD = 40

if __name__ == "__main__":
    assert dataset in ["NRE", "Scripps Pier"], "dataset should be NRE or Scripps Pier!"
    file_list = os.listdir(folder)

    if dataset == "NRE":
        file_list = [file for file in file_list if "Station" in file]
    else:
        file_list = [file for file in file_list if "Scripps" in file]
    
    true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0
    for file in file_list:
        result = calculate_F1_metrics(os.path.join(folder, file))
        true_positive += result[0]
        false_positive += result[1]
        true_negative += result[2]
        false_negative += result[3]
    POD = true_positive / (true_positive + false_negative)
    POFD = false_positive / (false_positive + true_negative)
    B = (true_positive + false_positive) / (true_positive + false_negative)
    PSS = POD - POFD
    F1 = 2*true_positive / (2*true_positive + false_positive + false_negative)
    print(f"true_positive: {true_positive}\nfalse_positive: {false_negative}\ntrue_negative: {true_negative}\nfalse_negative: {false_negative}")
    print(f"POD: {POD}\nPOFD: {POFD}\nB: {B}\nPSS: {PSS}\nF1: {F1}")
    