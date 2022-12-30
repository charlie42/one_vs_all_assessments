# Expected folder structure:
#   - all_assessments_test.joblib
#   - [Assessment name]
#       - reports
#           - evaluate_models_on_feature_subsets
#               - performances-on-feature-subsets.joblib

# all_assessments_test.joblib is a two-level dictionary where the first level keys are diganoses, the second level keys are numbers of features, 
#   and the values are the AUC for each diagnosis on each number of features using ALL assessments
# performances-on-feature-subsets.joblib is a two-level dictionary where the first level keys are diganoses, the second level keys are numbers of features, 
#   and the values are an array of metrics for each diagnosis on each number of features using a single assessment, the assessment name is the folder name
#   ([Assessment name]). AUC is the first value of the array

# Output: 
# For each diagnosis, print:
#   1/ the assessment with the highest AUC on all features
#   2/ the AUC on all features using the best assessment
#   3/ the AUC using all assessments, on the number of features equal to number of features on the best assessment for the diagnosis
#   4/ the number of features where AUC on all assessments reaches the AUC on all features on the best assessment
#   5/ the number of features where AUC on the best assessment on reaches the AUC on the best assessment on all features - 0.01
#   6/ the number where AUC on all assessments reaches the value the AUC on the best assessment on all features - 0.01

import joblib
import os
import pandas as pd

assessment_item_counts = {"ARI_P": 7, "ASSQ": 27, "CBCL": 121, "SCQ": 40, "SDQ": 33, "SRS": 65, "SWAN": 18, "SympChck": 126}

def make_table_from_auc_dict(auc_dict):
    auc_on_subsets = pd.DataFrame.from_dict(auc_dict)
    auc_on_subsets.index = range(1, len(auc_on_subsets)+1)
    auc_on_subsets = auc_on_subsets.rename(columns={"index": "Diagnosis"})
    auc_on_subsets = auc_on_subsets.apply(lambda x: x.str[0])
    return auc_on_subsets

def get_num_features_for_best_assessment(diag):
    # Get the number of features for the best assessment
    best_assessment, _ = best_assessment_per_diagnosis_and_score[diag]
    return assessment_item_counts[best_assessment]

def get_optimal_nb_features(auc_table, diag):
    max_score = auc_table[diag].max()
    optimal_score = max_score - 0.01
    # Get index of the first row with a score >= optimal_score
    return auc_table[diag][auc_table[diag] >= optimal_score].index[0]

# Load all_assessments_test.joblib
all_assessments = joblib.load('data/performances-on-feature-subsets.joblib')
# Make df from all_assessments_test.joblib
all_assessments_df = make_table_from_auc_dict(all_assessments)

aucs_using_one_assessment = {}
data_path = './data/'
for assessment_name in os.listdir(data_path):

    if (not os.path.isdir(data_path+assessment_name)) or assessment_name.startswith('.'):
        continue

    #if assessment_name in ["CBCL", "SympChck", "SRS"]: # DEBUG
    #    continue

    aucs_using_one_assessment[assessment_name] = {}
    
    # Load performances-on-feature-subsets.joblib for current assessment
    single_assessment = joblib.load(os.path.join('data', assessment_name, 'reports', 'evaluate_models_on_feature_subsets', 'performances-on-feature-subsets.joblib'))
    subset_auc_df = make_table_from_auc_dict(single_assessment)
    
    aucs_using_one_assessment[assessment_name] = subset_auc_df

# Find best assessment for each diagnosis
best_assessment_per_diagnosis_and_score = {}
diags = list(all_assessments.keys())
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
    best_assessment_num_features = get_num_features_for_best_assessment(diag)
    best_assessment, best_score = best_assessment_per_diagnosis_and_score[diag]

    # Get number of features where AUC on all assessments reaches the AUC on all features on the best assessment
    num_features = all_assessments_df[diag][all_assessments_df[diag] >= best_score].index[0]

    print(f'The number of features where AUC on all assessments reaches the AUC on the best assessment ({best_assessment}, {best_score:.2f}) for the diagnosis is {num_features}')

    ## 5 and 6

    best_assessment, best_score = best_assessment_per_diagnosis_and_score[diag]

    # Get the number of features where AUC on the best assessment on reaches the AUC on the best assessment on all features - 0.01
    optimal_nb_features_of_best_assessement = get_optimal_nb_features(aucs_using_one_assessment[best_assessment], diag)
    print(f"The number of features where AUC on the best assessment ({best_assessment}) reaches the AUC on the best assessment on all features ({best_assessment_num_features}) - 0.01 ({(best_score - 0.01):.2f}) is {optimal_nb_features_of_best_assessement}")

    # Get number of features where AUC on all assessments reaches the value the AUC on the best assessment on all features - 0.01
    auc_on_optimal_nb_features_of_best_assessement = aucs_using_one_assessment[best_assessment][diag][optimal_nb_features_of_best_assessement]
    nb_features_same_auc_as_on_optimal_on_best_assessment = all_assessments_df[diag][all_assessments_df[diag] >= auc_on_optimal_nb_features_of_best_assessement].index[0]
    print(f"The number of features where AUC on all assessments reaches the value the AUC on the best assessment on all features ({best_assessment_num_features}) - 0.01 ({(best_score - 0.01):.2f}) is {nb_features_same_auc_as_on_optimal_on_best_assessment}")


