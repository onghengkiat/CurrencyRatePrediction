from app import app
from flask import request, jsonify
from app.util import cors_allow, missing_param_handler
import pandas as pd
from constants import DATA_FILENAME

@app.route("/dashboard")
@cors_allow
@missing_param_handler
def get_dashboard():
    try: 
        df = pd.read_csv(DATA_FILENAME, index_col=0)
        # First column is date
        currency_codes = df.columns[1:]
        data = []
        prev_data = {}
        for i, row in df.iterrows():
            for currency_code in currency_codes:
                
                rate_changed_to_myr = 0
                rate_is_increased_to_myr = True
                rate_changed_from_myr = 0
                rate_is_increased_from_myr = True
                
                to_myr = row[currency_code]
                from_myr = round(1.0/to_myr, 4)
                if prev_data.get(currency_code, None) is not None:
                    rate_changed_to_myr = round( ((to_myr - prev_data[currency_code]["to_myr"])/prev_data[currency_code]["to_myr"]) * 100, 4)
                    if rate_changed_to_myr < 0:
                        rate_is_increased_to_myr = False
                        rate_changed_to_myr = round(-1.0 * rate_changed_to_myr, 4)

                    rate_changed_from_myr = round( ((from_myr - prev_data[currency_code]["from_myr"])/prev_data[currency_code]["from_myr"]) * 100, 4)
                    if rate_changed_from_myr < 0:
                        rate_is_increased_from_myr = False
                        rate_changed_from_myr = round(-1.0 * rate_changed_from_myr, 4)

                cur_data = {
                    "date": row['date'],
                    "currency_code": currency_code,
                    "to_myr": to_myr,
                    "from_myr": from_myr,
                    "rate_changed_to_myr": rate_changed_to_myr,
                    "rate_is_increased_to_myr": rate_is_increased_to_myr,
                    "rate_changed_from_myr": rate_changed_from_myr,
                    "rate_is_increased_from_myr": rate_is_increased_from_myr,
                }
                prev_data[currency_code] = cur_data

                data.append(cur_data)
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception:
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400
