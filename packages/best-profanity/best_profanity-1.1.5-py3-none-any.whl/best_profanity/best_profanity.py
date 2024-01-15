"""best-profanity exposed methods"""

import pkg_resources
import numpy as np
import joblib


vectorizer_tag = joblib.load(
    pkg_resources.resource_filename("best_profanity", "data/tagalog-vectorizer.joblib")
)
model_tag = joblib.load(
    pkg_resources.resource_filename("best_profanity", "data/tagalog-model.joblib")
)
vectorizer_eng = joblib.load(
    pkg_resources.resource_filename("best_profanity", "data/english-vectorizer.joblib")
)
model_eng = joblib.load(
    pkg_resources.resource_filename("best_profanity", "data/english-model.joblib")
)


def _get_profane_prob(prob):
    return prob[1]


def predict(texts):
    en_pred = model_eng.predict(vectorizer_eng.transform(texts))
    tl_pred = model_tag.predict(vectorizer_tag.transform(texts))

    return en_pred | tl_pred


def predict_prob(texts):
    en_pred_prob = np.apply_along_axis(
        _get_profane_prob, 1, model_eng.predict_proba(vectorizer_eng.transform(texts))
    )
    tl_pred_prob = np.apply_along_axis(
        _get_profane_prob, 1, model_tag.predict_proba(vectorizer_tag.transform(texts))
    )

    return en_pred_prob, tl_pred_prob


# define text for prediction
# texts_to_predict = [
#     "gag0 ka ba ang bah mo k4nina ka pa",
#     "gago you are so ugly",
#     "fuck y0u",
#     "i h4te you tanga",
#     "tangina nagjjoke lang ako",
# ]

# # use predict function
# predictions = predict(texts_to_predict)
# print("Predictions:", predictions)
