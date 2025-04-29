# BlinkPay - Customer Segmentation Project

This project implements a customer segmentation system using machine learning techniques. It includes a Flask web application for predicting customer segments based on input features.

## 📂 Project Structure

```
your-project/
│
├── src/
│   ├── app.py                  # Flask app
│   ├── customer_segmentation.py # Training script
│   ├── sqlserver_connection.py  # Database connection
│   └── templates/              # Flask HTML templates
│
├── models/
│   ├── kmeans_model.pkl
│   ├── pca.pkl
│   ├── scaler.pkl
│
├── data/
│   └── (data files or scripts)
│
├── notebooks/
│   └── (Jupyter notebooks for exploration)
│
├── docs/
│   └── (project documentation)
│
├── requirements.txt            # Python dependencies
├── README.md                  # Project overview
├── .gitignore                 # Git ignore rules
```

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Run the Flask app:

```
python -m src.app
```

## Description

- `src/app.py`: Flask application for serving the prediction API and web interface.
- `src/customer_segmentation.py`: Script for training the segmentation model.
- `src/sqlserver_connection.py`: Database connection utilities.
- `models/`: Contains saved model files.
- `data/`: Data files or scripts.
- `notebooks/`: Jupyter notebooks for data exploration.
- `docs/`: Documentation files.
