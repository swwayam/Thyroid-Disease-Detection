import os
from pathlib import Path
import pandas as pd
from weasyprint import HTML,CSS
from helper import getRange


def createPdf():

    data_file = Path("./Prediction_Output_File/Predictions.csv")
    df = pd.read_csv(data_file)


    records = df.to_dict(orient="records")


    for i in range(len(records)):


        report = {

        }

        report["age"] = records[i]["age"]
        report["T4U"] = records[i]["T4U"]
        report["TSH"] = records[i]["TSH"]
        report["T3"] = records[i]["T3"]
        report["result"] = records[i]["result"]
        report["range"] = getRange(records[i]["result"])
    

        with open("template.html", 'r') as file:
            html_template = file.read()

        htm1 = html_template.format(**report)
        HTML(string = htm1).write_pdf(f"./output/Patient-{i}.pdf")