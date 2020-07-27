##########################
# only for testing stage #
##########################

from flask import Flask
from flask import request
from flask import jsonify
import datetime
import hashlib
import sys
import numpy as np
import pandas as pd

sys.path.append('/bert_classification')

# from client_SVM import createCls, isLaunderingWithBert

app = Flask(__name__)
####### PUT YOUR INFORMATION HERE #######
CAPTAIN_EMAIL = 'kaoweitse220@gmail.com'          #
SALT = 'ai-samurai'                        #
#########################################

# myCls = createCls() # fit
@app.route("/")
def hello():
    return "Hello Flask!"

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8081, debug=True)

