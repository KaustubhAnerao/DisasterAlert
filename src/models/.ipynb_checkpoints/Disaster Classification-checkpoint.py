{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 162,
   "id": "4c6e6093-3ae7-46ab-9f14-1e7967599865",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import re\n",
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.tokenize import word_tokenize\n",
    "from nltk.stem import PorterStemmer\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.model_selection import train_test_split\n",
    "from imblearn.over_sampling import RandomOverSampler\n",
    "import collections\n",
    "import nltk\n",
    "from sklearn.ensemble import RandomForestClassifier\n",
    "from sklearn.model_selection import RandomizedSearchCV\n",
    "from sklearn.metrics import accuracy_score, classification_report"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "id": "0b9459ff-a897-46ce-9ba4-cc504b71162b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load dataset\n",
    "df = pd.read_csv(r\"C:\\Users\\ADMIN\\Documents\\Disaster Alert\\src\\datasets\\tweets.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "id": "87a8c505-f415-406a-b974-9e0fd1ab4e01",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     C:\\Users\\ADMIN\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package stopwords is already up-to-date!\n",
      "[nltk_data] Downloading package punkt to\n",
      "[nltk_data]     C:\\Users\\ADMIN\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package punkt is already up-to-date!\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 166,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Download NLTK resources\n",
    "nltk.download('stopwords')\n",
    "nltk.download('punkt')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 168,
   "id": "803f8635-2191-4ab0-8010-97708a1afe52",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "target\n",
      "0    9256\n",
      "1    2114\n",
      "Name: count, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(df['target'].value_counts())\n",
    "# Data is imbalance with 9256 non-disaster tweets and 2114 disaster tweets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "id": "91af795b-6f56-4fbb-a129-0b1b960b2d50",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to preprocess text\n",
    "def preprocess_text(text):\n",
    "    text = text.lower()  # Convert to lowercase\n",
    "    text = re.sub(r'http\\S+|www\\S+', '', text)  # Remove URLs\n",
    "    text = re.sub(r'\\@\\w+|\\#\\w+', '', text)  # Remove mentions and hashtags\n",
    "    text = re.sub(r'[^A-Za-z\\s]', '', text)  # Remove special characters\n",
    "    tokens = word_tokenize(text)  # Tokenization\n",
    "    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords\n",
    "    stemmer = PorterStemmer()\n",
    "    tokens = [stemmer.stem(word) for word in tokens]  # Stemming\n",
    "    return \" \".join(tokens)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "id": "e5e70bbc-6672-4660-86ba-c1aa04e1b138",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Apply preprocessing\n",
    "df[\"clean_text\"] = df[\"text\"].apply(lambda x: preprocess_text(str(x)) if pd.notnull(x) else \"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "id": "ac447b09-68db-4626-94c2-491cedf6ee27",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Index(['id', 'keyword', 'location', 'text', 'target', 'clean_text'], dtype='object')\n"
     ]
    }
   ],
   "source": [
    "# Check if 'clean_text' exists now\n",
    "print(df.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "id": "7e1b792f-2790-4424-a592-56790502db04",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert text into numerical features using TF-IDF\n",
    "vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)\n",
    "X = vectorizer.fit_transform(df[\"clean_text\"])  # Convert tweets into vectors\n",
    "y = df[\"target\"]  # Labels (0 or 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 175,
   "id": "ec3161fb-defb-4b7a-98d3-57372d3e7022",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Shape of X: (11370, 10000)\n"
     ]
    }
   ],
   "source": [
    "# Print shape to confirm success\n",
    "print(\"Shape of X:\", X.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 176,
   "id": "34604d25-1e13-452d-8ac7-1262baa49412",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Splitting the data into training and testing sets\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 177,
   "id": "a9e7a7ea-3f93-4715-b97a-6ebc7033553f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Define hyperparameter grid\n",
    "param_grid = {\n",
    "    'n_estimators': [100, 200, 300],\n",
    "    'max_depth': [10, 20, None],\n",
    "    'min_samples_split': [2, 5, 10],\n",
    "    'min_samples_leaf': [1, 2, 5],\n",
    "    'max_features': ['sqrt', 'log2']\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 181,
   "id": "5aaa7e29-d5db-4cfc-8aff-4fb1704179b8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initialize Random Forest\n",
    "rf = RandomForestClassifier(random_state=42, class_weight='balanced')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "id": "8814307e-a7e6-4563-a9c3-a76635a36617",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fitting 3 folds for each of 20 candidates, totalling 60 fits\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-6 {color: black;background-color: white;}#sk-container-id-6 pre{padding: 0;}#sk-container-id-6 div.sk-toggleable {background-color: white;}#sk-container-id-6 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-6 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-6 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-6 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-6 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-6 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-6 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-6 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-6 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-6 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-6 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-6 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-6 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-6 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-6 div.sk-item {position: relative;z-index: 1;}#sk-container-id-6 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-6 div.sk-item::before, #sk-container-id-6 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-6 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-6 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-6 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-6 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-6 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-6 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-6 div.sk-label-container {text-align: center;}#sk-container-id-6 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-6 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-6\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>RandomizedSearchCV(cv=3,\n",
       "                   estimator=RandomForestClassifier(class_weight=&#x27;balanced&#x27;,\n",
       "                                                    random_state=42),\n",
       "                   n_iter=20, n_jobs=-1,\n",
       "                   param_distributions={&#x27;max_depth&#x27;: [10, 20, None],\n",
       "                                        &#x27;max_features&#x27;: [&#x27;sqrt&#x27;, &#x27;log2&#x27;],\n",
       "                                        &#x27;min_samples_leaf&#x27;: [1, 2, 5],\n",
       "                                        &#x27;min_samples_split&#x27;: [2, 5, 10],\n",
       "                                        &#x27;n_estimators&#x27;: [100, 200, 300]},\n",
       "                   random_state=42, scoring=&#x27;f1_macro&#x27;, verbose=2)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-6\" type=\"checkbox\" ><label for=\"sk-estimator-id-6\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">RandomizedSearchCV</label><div class=\"sk-toggleable__content\"><pre>RandomizedSearchCV(cv=3,\n",
       "                   estimator=RandomForestClassifier(class_weight=&#x27;balanced&#x27;,\n",
       "                                                    random_state=42),\n",
       "                   n_iter=20, n_jobs=-1,\n",
       "                   param_distributions={&#x27;max_depth&#x27;: [10, 20, None],\n",
       "                                        &#x27;max_features&#x27;: [&#x27;sqrt&#x27;, &#x27;log2&#x27;],\n",
       "                                        &#x27;min_samples_leaf&#x27;: [1, 2, 5],\n",
       "                                        &#x27;min_samples_split&#x27;: [2, 5, 10],\n",
       "                                        &#x27;n_estimators&#x27;: [100, 200, 300]},\n",
       "                   random_state=42, scoring=&#x27;f1_macro&#x27;, verbose=2)</pre></div></div></div><div class=\"sk-parallel\"><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-7\" type=\"checkbox\" ><label for=\"sk-estimator-id-7\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">estimator: RandomForestClassifier</label><div class=\"sk-toggleable__content\"><pre>RandomForestClassifier(class_weight=&#x27;balanced&#x27;, random_state=42)</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-8\" type=\"checkbox\" ><label for=\"sk-estimator-id-8\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">RandomForestClassifier</label><div class=\"sk-toggleable__content\"><pre>RandomForestClassifier(class_weight=&#x27;balanced&#x27;, random_state=42)</pre></div></div></div></div></div></div></div></div></div></div>"
      ],
      "text/plain": [
       "RandomizedSearchCV(cv=3,\n",
       "                   estimator=RandomForestClassifier(class_weight='balanced',\n",
       "                                                    random_state=42),\n",
       "                   n_iter=20, n_jobs=-1,\n",
       "                   param_distributions={'max_depth': [10, 20, None],\n",
       "                                        'max_features': ['sqrt', 'log2'],\n",
       "                                        'min_samples_leaf': [1, 2, 5],\n",
       "                                        'min_samples_split': [2, 5, 10],\n",
       "                                        'n_estimators': [100, 200, 300]},\n",
       "                   random_state=42, scoring='f1_macro', verbose=2)"
      ]
     },
     "execution_count": 183,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Perform Randomized Search\n",
    "rf_search = RandomizedSearchCV(rf, param_grid, n_iter=20, cv=3, scoring='f1_macro', n_jobs=-1, verbose=2, random_state=42)\n",
    "rf_search.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 185,
   "id": "342d17e4-c357-4915-b492-09bf43d109ce",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Parameters: {'n_estimators': 100, 'min_samples_split': 2, 'min_samples_leaf': 2, 'max_features': 'log2', 'max_depth': None}\n"
     ]
    }
   ],
   "source": [
    "# Best parameters\n",
    "print(\"Best Parameters:\", rf_search.best_params_)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 187,
   "id": "66680c96-9bec-4138-a90d-51e887aedbe3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Train best model\n",
    "best_rf = rf_search.best_estimator_\n",
    "y_pred = best_rf.predict(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 190,
   "id": "faa814fd-6699-4058-b7d0-a78e939317b5",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.8970976253298153\n",
      "Classification Report:\n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "           0       0.93      0.95      0.94      1878\n",
      "           1       0.73      0.65      0.69       396\n",
      "\n",
      "    accuracy                           0.90      2274\n",
      "   macro avg       0.83      0.80      0.81      2274\n",
      "weighted avg       0.89      0.90      0.89      2274\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Evaluate model\n",
    "from sklearn.metrics import classification_report, accuracy_score\n",
    "print(\"Accuracy:\", accuracy_score(y_test, y_pred))\n",
    "print(\"Classification Report:\\n\", classification_report(y_test, y_pred))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
