import pandas as pd

# The csv should be in format datetime ,open,high,low,close. volume is optional 

def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at {filepath}")
    
    required_columns = ["datetime","open","high","low","close"]

    column_names = data.columns.tolist()

    if "datetime" not in column_names:
        raise ValueError("'datetime' column not present in csv")
    elif "open" not in column_names:
        raise ValueError("'open' column not present in csv")
    elif "high" not in column_names:
        raise ValueError("'high' column not present in csv")
    elif "low" not in column_names:
        raise ValueError("'low' column not present in csv")
    elif "close" not in column_names:
        raise ValueError("'close' column not present in csv")

    try:
        data["datetime"] = pd.to_datetime(data["datetime"])
    except(ValueError,TypeError):
        raise ValueError("Invalid datetime values in CSV")

    if data[required_columns].isna().any().any():
        raise ValueError("Required Columns contains empty cells")

    for column in ["open","high","low","close"]:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"'{column}' does not contain numeric value(float or int)")


    return data