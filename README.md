# 🩺 HemoPredict: Streamlit App Using ABC-Optimized XGBoost for Hemodialysis Complication Prediction

![image](https://github.com/user-attachments/assets/19513b40-ab71-452a-9b67-c170039f289a)

**HemoPredict** is a powerful Streamlit-based machine learning web application developed to predict **hemodialysis complications**, such as **hypotension**, **hypertension**, and **intestinal disorders**. This system leverages the predictive power of **XGBoost** optimized by the **Artificial Bee Colony (ABC)** algorithm to improve accuracy and performance.

Designed with both functionality and usability in mind, the app integrates a real-time database, supports various input methods, and is deployed online for immediate access.

---

## 🚀 Features

- 🎯 **High Accuracy Predictions** – Detect complications like hypotension, hypertension, and intestinal issues
- 🧠 **ABC-Optimized XGBoost Model** – Combines advanced ensemble learning with swarm intelligence
- 💻 **User-Friendly Streamlit Interface** – Clean and responsive web interface for medical professionals
- 🔒 **User Authentication System** – Secure login for personalized prediction management
- 📝 **Two Input Modes**:
  - Manual input for single records
  - Upload from **CSV or Excel** files for batch predictions
- 🕒 **Time & User Logging** – Each prediction is timestamped and tied to the logged-in user
- 💾 **Customizable Save Option** – Users can choose whether or not to save prediction results
- 📥 **Downloadable Reports** – Export prediction results in CSV format
- 🗃️ **Online MySQL Integration** – Real-time connection to a hosted MySQL database for storing user data and prediction history
- 🌐 **Fully Online Application** – Deployed and ready for use without local setup

---

## 🧪 Experiments and Evaluation

A total of **72 models** were evaluated using five different testing strategies with both **unbalanced** and **balanced datasets**:

- **Train-Test Splits**: 75:25 and 80:20
- **K-Fold Cross-Validation**: K = 3, 5, 7, 10
- Each scenario was repeated **5 times** to ensure robustness

### ✅ Results With ABC Optimization

#### 🔹 Split Cross Validation

| Test | Split        | Unbalanced Accuracy (%) | Time (min) | Balanced Accuracy (%) | Time (min) |
|------|--------------|--------------------------|------------|------------------------|------------|
| 1    | 75% : 25%    | 90                       | 11         | 95                     | 9          |
| 2    |              | 89                       | 27         | 93                     | 20         |
| 3    |              | 87                       | 65         | 94                     | 69         |
| 4    |              | 89                       | 11         | 91                     | 17         |
| 5    |              | 89                       | 18         | 94                     | 19         |
| 1    | 80% : 20%    | 91                       | 6          | 93                     | 10         |
| 2    |              | 89                       | 12         | 93                     | 39         |
| 3    |              | 89                       | 52         | 94                     | 104        |
| 4    |              | 89                       | 10         | 92                     | 37         |
| 5    |              | 87                       | 21         | 91                     | 71         |

#### 🔹 K-Fold Cross Validation

| Test | K | Unbalanced Accuracy (%) | Time (min) | Balanced Accuracy (%) | Time (min) |
|------|---|--------------------------|------------|------------------------|------------|
| 1    | 3 | 84                       | 9          | 85                     | 8          |
| 2    |   | 85                       | 15         | 84                     | 16         |
| 3    |   | 87                       | 55         | 84                     | 46         |
| 4    |   | 85                       | 11         | 84                     | 16         |
| 5    |   | 85                       | 30         | 85                     | 31         |
| 1    | 5 | 84                       | 10         | 87                     | 10         |
| 2    |   | 86                       | 13         | 86                     | 12         |
| 3    |   | 84                       | 50         | 87                     | 49         |
| 4    |   | 87                       | 8          | 86                     | 9          |
| 5    |   | 86                       | 20         | 87                     | 20         |
| 1    | 7 | 84                       | 9          | 84                     | 8          |
| 2    |   | 84                       | 17         | 84                     | 18         |
| 3    |   | 85                       | 60         | 85                     | 62         |
| 4    |   | 85                       | 15         | 85                     | 16         |
| 5    |   | 85                       | 38         | 84                     | 33         |
| 1    |10 | 79                       | 11         | 82                     | 11         |
| 2    |   | 82                       | 20         | 82                     | 18         |
| 3    |   | 82                       | 102        | 82                     | 100        |
| 4    |   | 82                       | 18         | 82                     | 27         |
| 5    |   | 82                       | 33         | 82                     | 24         |

---

### ❌ Baseline (Without ABC Optimization)

| Testing Scheme | Accuracy (Unbalanced) | Accuracy (Balanced) |
|----------------|------------------------|----------------------|
| 80:20 Split     | 91%                    | 94%                  |
| 75:25 Split     | 87%                    | 93%                  |
| K = 3           | 84%                    | 84%                  |
| K = 5           | 84%                    | 84%                  |
| K = 7           | 83%                    | 83%                  |
| K = 10          | 79%                    | 79%                  |

📌 **Insight**: The ABC optimization consistently improves accuracy across most test schemes and enhances performance, especially on imbalanced datasets.

---
### Demo Website 
![image](https://github.com/user-attachments/assets/9666567b-3c59-4f18-97e5-d73b172e3e05)

![image](https://github.com/user-attachments/assets/9cf2ab70-f959-4bfb-9b64-67c53a399736)

![image](https://github.com/user-attachments/assets/7bc5aba5-7369-4a30-b41f-127067d22555)

![image](https://github.com/user-attachments/assets/6e0ea4c6-41d6-455e-a2e4-ba3ebc3170d2)

![image](https://github.com/user-attachments/assets/21c9697c-ee71-42e9-b874-602c0a2fb39e)

![image](https://github.com/user-attachments/assets/527890a5-4015-4eb4-95bb-39c47fc66e30)

