def add_missing_values(row):
    if "Long" in row and "video.parler.com" in row.get("Long"):
        row["Domain"] = "parler.com"
    return row