# Your Project

This project contains time series forecasting using SARIMAX model with a Flask web application for predictions.

## Project Structure

- `src/` - Python source code including training and evaluation scripts
- `data/` - Scripts to download data (optional)
- `notebooks/` - Jupyter notebooks
- `models/` - Saved trained models
- `docs/` - Documentation (optional)
- `requirements.txt` - Python package dependencies
- `README.md` - Project documentation
- `.gitignore` - Files and folders to ignore in git

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Run the Flask app:

```
python src/app.py
```

## Notes

- The SARIMAX model is saved in the `models/` directory.
- Templates are located inside `src/templates/`.
