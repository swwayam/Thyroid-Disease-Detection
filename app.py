import os
import csv
import zipfile
from createPdf import createPdf
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from predictFromModel import prediction
from dbOperations import dbUpload
app = Flask(__name__)

app.config["csv_file"] = "Prediction_Output_File/"
app.config["sample_file"] = "Prediction_SampleFile/"


@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/return_sample_file/')
@cross_origin()
def return_sample_file():
    sample_file = os.listdir("Prediction_SampleFile/")[0]
    return send_from_directory(app.config["sample_file"], sample_file)


@app.route('/download/<filename>')
def download(filename):
    # Construct the path to the PDF file
    file_path = os.path.join('output', filename)
    
    # Return the file as a download
    return send_file(file_path, as_attachment=True)




@app.route('/result')
@cross_origin()
def result():
    # Upload to db
    dbUpload()
    # Creating the pdf's
    createPdf()
    # Get a list of all PDF files in the folder
    output = [f for f in os.listdir('output') if f.endswith('.pdf')]
    
    # Render the template with the list of PDF files
    return render_template('result.html', output=output)



@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        
        try:
            
            if 'csvfile' not in request.files:
                return render_template("invalid.html")
            
            file = request.files['csvfile']
            
            df = pd.read_csv(file, index_col=[0])             
            
            path = 'Prediction_InputFileFromUser/'
            
            #if os.path.isfile('Prediction_InputFileFromUser/InputFile.csv'):
                #os.remove('Prediction_InputFileFromUser/InputFile.csv')

            df.to_csv('Prediction_InputFileFromUser/InputFile.csv')
            
            pred = prediction() #object initialization
   
            pred.predictionFromModel()
            
            
        except Exception as e:
            return render_template("invalid.html")



    return redirect(url_for('result'))


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

