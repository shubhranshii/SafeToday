import librosa
import joblib 
import numpy as np
import os
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC



# In[ ]:


def extract_features(file_name, mfcc, chroma, mel):
    X, sample_rate= librosa.load(os.path.join(file_name), res_type= 'kaiser_fast')
    if chroma:
        stft= np.abs(librosa.stft(X))
    result= np.array([])
    if mfcc:
        mfcc= np.mean(librosa.feature.mfcc(y=X, sr= sample_rate, n_mfcc= 40).T, axis=0)
        result= np.hstack((result, mfcc))
    if chroma:
        chroma= np.mean(librosa.feature.chroma_stft(S= stft, sr= sample_rate).T, axis=0)
        result= np.hstack((result, chroma))
    if mel:
        mel= np.mean(librosa.feature.melspectrogram(y=X, sr= sample_rate).T, axis=0)
        result= np.hstack((result, mel))
    result= result.reshape(1, 180)
    mplc_pred= mplc.predict_proba(result)
    random_forest_pred = random_forest_model.predict_proba(result)
    final_pred= random_forest_pred+ mplc_pred

    final_label= np.argmax(final_pred, axis=1)
    if final_label==2:
        return True
    else:
        return False


# In[ ]:
model_DIR= ""

mplc= joblib.load('MPLC.h5')
random_forest_model = joblib.load('random_forest_model.pkl')