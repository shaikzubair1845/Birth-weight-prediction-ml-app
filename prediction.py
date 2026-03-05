from flask import Blueprint,jsonify,request,render_template
import pandas as pd
import pickle
from extensions import cache
predict_bp=Blueprint("prediction",__name__)
with open("pickle_model.pkl","rb") as f:
        model=pickle.load(f)
def cleaned_data(form_data):
   gestation=float(form_data["gestation"])
   parity=int(form_data["parity"])
   age=float(form_data["age"])
   height=float(form_data["height"])
   weight=float(form_data["weight"])
   smoke=float(form_data["smoke"])
   data={"gestation":gestation,
          "parity":parity,
          "age":age,
          "height":height,
          "weight":weight,
          "smoke":smoke
         }
   return data
@predict_bp.route("/",methods=["get"])
def page():
    return render_template("index.html")

@predict_bp.route("/home",methods=["get"])
def hello():
    return jsonify({"msg":"hello world"})
@predict_bp.route("/predict",methods=["POST"])
@cache.cached(timeout=30,query_string=True)
def get_prediction():
    baby_data = request.form.to_dict()
    if not baby_data:
      return jsonify({"error":"no input data provided"}),400
    cleaned=cleaned_data(baby_data)
    baby_df=pd.DataFrame([cleaned])
    prediction=model.predict(baby_df)
    prediction=float(prediction[0])
    response={"prediction":prediction}
    return render_template("index.html", prediction=prediction)
     
