import pandas as pd
import os
from config.settings import EXCEL_ENGINE, EXCEL_SHEET_NAME

def write_to_excel(data_list, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    all_keys = set()
    for d in data_list:
        all_keys.update(d.keys())
    cleaned_data = []
    for d in data_list:
        cleaned_data.append({k: (d.get(k, "") or "").strip() for k in all_keys})
    df = pd.DataFrame(cleaned_data)
    # Debug: print DataFrame head to terminal
    print("DataFrame to be written to Excel:")
    print(df.head())
    # Warn if DataFrame is empty
    if df.empty:
        print("WARNING: DataFrame is empty. No data will be written to Excel.")
    # Smart sort: prioritize by Client Name, then by Date (if present), then by Invoice No, then by ID (if present)
    sort_cols = []
    for col in ["Client Name", "Name", "Date", "Invoice No", "ID"]:
        if col in df.columns:
            sort_cols.append(col)
    if sort_cols:
        df = df.sort_values(by=sort_cols)
    try:
        with pd.ExcelWriter(output_path, engine=EXCEL_ENGINE) as writer:
            # Only write the note if there are columns other than just Filename and Error
            error_cols = set(["Filename", "Error"])
            if not df.empty and set(df.columns) - error_cols:
                note = "The Scarping Data from the pdf"
                worksheet_name = EXCEL_SHEET_NAME
                # Write the note
                pd.DataFrame([[note] + [""] * (len(df.columns)-1)], columns=df.columns).to_excel(
                    writer, index=False, sheet_name=worksheet_name, header=False, startrow=0
                )
                # Write the data with headers, starting from row 1
                df.to_excel(writer, index=False, sheet_name=worksheet_name, startrow=1)
            else:
                # Only errors or empty: just write the DataFrame
                df.to_excel(writer, index=False, sheet_name=EXCEL_SHEET_NAME)
    except PermissionError:
        print(f"ERROR: Cannot write to {output_path}. Please close the file if it is open in Excel and try again.")
        raise
    except Exception as e:
        print(f"ERROR: Failed to write Excel file: {e}")
        raise
