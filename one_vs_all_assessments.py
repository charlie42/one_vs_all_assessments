# Expected folder structure:
#   - ../diagnosis_predictor_data
#       - reports
#           - evaluate_models_on_feature_subsets
#               - 2023-01-03 17.51.26___first_dropped_assessment__ICU_P___other_diag_as_input__0___debug_mode__True
#                   - auc-on-subsets-test-set-optimal-threshold.csv
#               - 2023-01-03 17.51.26___single_assessment_used__ICU_P___other_diag_as_input__0___debug_mode__True
#                   - auc-on-subsets-test-set-optimal-threshold.csv
 
# Folder name containing "first_dropped_assessment" contains performance on all assessments.
# Folder names containing "single_assessment_used" contain performance on a single assessment.

# Output: 
# For each diagnosis, print:
#   1/ the assessment with the highest AUC on all features
#   2/ the AUC on all features using the best assessment
#   3/ the AUC using all assessments, on the number of features equal to number of features on the best assessment for the diagnosis
#   4/ the number of features where AUC on all assessments reaches the AUC on all features on the best assessment
#   5/ the number of features where AUC on the best assessment on reaches the AUC on the best assessment on all features - 0.01
#   6/ the number where AUC on all assessments reaches the value the AUC on the best assessment on all features - 0.01
#   7/ the AUC when scored manually (best among all total and subscale scores)

import os
import pandas as pd

def get_num_features_for_best_assessment(diag):
    # Get the number of features for the best assessment
    best_assessment, _ = best_assessment_per_diagnosis_and_score[diag]
    return assessment_item_counts[best_assessment]

def get_optimal_nb_features(auc_table, diag):
    max_score = auc_table[diag].max()
    optimal_score = max_score - 0.01
    # Get index of the first row with a score >= optimal_score
    return auc_table[diag][auc_table[diag] >= optimal_score].index[0]

def get_newest_non_empty_dir_in_dir_containing_string(path, string):
    dirs = [path+d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    dirs = [d for d in dirs if len(os.listdir(d)) > 0] # non empty
    dirs = [d for d in dirs if string in d] # contains string
    return max(dirs, key=os.path.getmtime) + "/"

data_path = '../diagnosis_predictor_data/reports/evaluate_models_on_feature_subsets/'

assessment_item_counts = {"ARI_P": 7, "ASSQ": 27, "CBCL": 121, "SCQ": 40, "SDQ": 33, "SRS": 65, "SWAN": 18, "SympChck": 126}

# Load AUCs when using all assessments
newest_all_assessments_dir = get_newest_non_empty_dir_in_dir_containing_string("../diagnosis_predictor_data/reports/evaluate_models_on_feature_subsets/", "first_dropped_assessment")
print(newest_all_assessments_dir)
all_assessments_df = pd.read_csv(newest_all_assessments_dir + "auc-on-subsets-test-set-optimal-threshold.csv", index_col=0).iloc[::-1]
print(all_assessments_df)

aucs_using_one_assessment = {}

for assessment_name in assessment_item_counts.keys():

    aucs_using_one_assessment[assessment_name] = {}

    # Load performances-on-feature-subsets.joblib for current assessment
    assessment_dir = get_newest_non_empty_dir_in_dir_containing_string(data_path, assessment_name)
    print(assessment_dir)
    aucs_using_one_assessment[assessment_name] = pd.read_csv(assessment_dir + "auc-on-subsets-test-set-optimal-threshold.csv", index_col=0).iloc[::-1]

# Find best assessment for each diagnosis
best_assessment_per_diagnosis_and_score = {}

# Get AUCs from manual scoring
manual_scoring_df = pd.read_csv("../HBN-scripts/output/score_manually.csv")

diags = set(all_assessments_df.columns)
print(diags)

for diag in diags:

    print("\n\n\t", diag)

    ## 1 and 2
    print("\n")

    # Find the df with the highest AUC on all features 
    best_auc = 0
    best_assessment = ""
    for assessment_name, df in aucs_using_one_assessment.items():
        if df[diag].iloc[-1] > best_auc:
            best_auc = df[diag].iloc[-1]
            best_assessment = assessment_name
    
    # Store the best assessment for each diagnosis
    best_assessment_per_diagnosis_and_score[diag] = [best_assessment, best_auc]

    print(f'{best_assessment} has the highest AUC on all features with a value of {best_auc:.2f}')

    ## 3

    # Find the AUC on all assessments, on the number of features equal to number of features on the best assessment for the diagnosis

    # Get the number of features for the best assessment
    best_assessment_num_features = get_num_features_for_best_assessment(diag)

    # Get the AUC on all assessments, on the number of features equal to number of features on the best assessment for the diagnosis
    auc = all_assessments_df[diag][best_assessment_num_features]
    print(f'The AUC on all assessments on the number of features equal to number of features on the best assessment ({best_assessment}, {best_assessment_num_features}) for the diagnosis is {auc:.2f}')

    ## 4

    # Find the number of features where AUC on all assessments reaches the AUC on all features on the best assessment
    best_assessment, best_score = best_assessment_per_diagnosis_and_score[diag]

    # Get number of features where AUC on all assessments reaches the AUC on all features on the best assessment
    # Catch index error if the best score is not reached
    try:
        num_features = all_assessments_df[diag][all_assessments_df[diag] >= best_score].index[0]
    except IndexError:
        num_features = "not reached"

    print(f'The number of features where AUC on all assessments reaches the AUC on the best assessment ({best_assessment}, {best_score:.2f}) for the diagnosis is {num_features}')

    ## 5 and 6

    best_assessment, best_score = best_assessment_per_diagnosis_and_score[diag]

    # Get the number of features where AUC on the best assessment on reaches the AUC on the best assessment on all features - 0.01
    optimal_nb_features_of_best_assessement = get_optimal_nb_features(aucs_using_one_assessment[best_assessment], diag)
    print(f"The number of features where AUC on the best assessment ({best_assessment}) reaches the AUC on the best assessment on all features ({best_assessment_num_features}) - 0.01 ({(best_score - 0.01):.2f}) is {optimal_nb_features_of_best_assessement}")

    # Get number of features where AUC on all assessments reaches the value the AUC on the best assessment on all features - 0.01
    auc_on_optimal_nb_features_of_best_assessement = aucs_using_one_assessment[best_assessment][diag][optimal_nb_features_of_best_assessement]
    try:
        nb_features_same_auc_as_on_optimal_on_best_assessment = all_assessments_df[diag][all_assessments_df[diag] >= auc_on_optimal_nb_features_of_best_assessement].index[0]
    except IndexError:
        nb_features_same_auc_as_on_optimal_on_best_assessment = "not reached"
    print(f"The number of features where AUC on all assessments reaches the value the AUC on the best assessment on all features ({best_assessment_num_features}) - 0.01 ({(best_score - 0.01):.2f}) is {nb_features_same_auc_as_on_optimal_on_best_assessment}")

    ## 7
    manual_auc = manual_scoring_df["AUC"][manual_scoring_df["Diag"] == diag].iloc[-1]
    print(f"The AUC using manual scoring is {manual_auc:.2f}")

