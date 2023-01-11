# First switch to single-assessment-as-input branch of diagnosis-predictor, then run:

python -W ignore src/data/make_dataset.py 0 ICU_P

python -W ignore src/models/train_models.py 0.02 0 0 ARI_P
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 ASSQ
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 CBCL
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 SCQ
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 SDQ
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 SRS
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 SWAN
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

python -W ignore src/models/train_models.py 0.02 0 0 SympChck
python -W ignore src/models/identify_feature_subsets.py 126 0
python -W ignore src/models/evaluate_models_on_feature_subsets.py 0

