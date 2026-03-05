from flask import Flask,request,jsonify,render_template
from extensions import cache
from routes.prediction import predict_bp

app=Flask(__name__)

app.config["CACHE_TYPE"]="SimpleCache"
cache.init_app(app)
app.register_blueprint(predict_bp)
if __name__=='__main__':
    app.run(debug=True)