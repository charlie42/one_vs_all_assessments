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
# 1. For each assessment name, save the diagnosis with the highest AUC on 50 features. 
# 2. From output of 1, extract best assessment for each diagnosis.
# 3. For each diagnosis, print:
#   - the assessment with the highest AUC on 50 features
#   - the AUC on 50 features using the best assessment
#   - the AUC using all assessments, on the number of features where AUC of the best assessments stops increasing
#   - the number of features where AUC on all assessments reaches the AUC on 50 features on the best assessment
#   - the number of features where AUC on the best assessment on reaches the AUC on the best assessment on 50 features, rounded to 2 decimal places
#   - the number where AUC on all assessments reaches the value the AUC on the best assessment on 50 features, rounded to 2 decimal places

import joblib
import os

# Load all_assessments_test.joblib
all_assessments = joblib.load('all_assessments_test.joblib')

best_assessment_per_diagnosis = {}
for assessment_name in os.listdir():
    # Skip all_assessments_test.joblib
    if assessment_name == 'all_assessments_test.joblib':
        continue

    # Load performances-on-feature-subsets.joblib for current assessment
    single_assessment = joblib.load(os.path.join(assessment_name, 'reports', 'evaluate_models_on_feature_subsets', 'performances-on-feature-subsets.joblib'))

    # Find the diagnosis with the highest AUC on 50 features for current assessment
    best_diagnosis = None
    best_auc = 0
    for diagnosis, aucs in single_assessment.items():
        if 50 in aucs and aucs[50] > best_auc:
            best_diagnosis = diagnosis
            best_auc = aucs[50]

    # Store the best assessment for each diagnosis
    best_assessment_per_diagnosis[diagnosis] = assessment_name

    print(f'For diagnosis {diagnosis}, {assessment_name} has the highest AUC on 50 features with a value of {best_auc:.2f}')