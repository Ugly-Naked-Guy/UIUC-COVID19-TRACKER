import os
import copy
import numpy as np
import pandas as pd

import hashdate as hd


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from myModel import Logistic_Regression, sigmoid, find_location_weight
from myPlot import draw_barchar, draw_barchar_address, pie_char,user_draw_barchar, user_draw_barchar_address, user_pie_char


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.secret_key = 'many random bytes'


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '951205'
app.config['MYSQL_DB'] = 'crud'


mysql = MySQL(app)

login_user = False
login_admin = False
username_global = ""

search_dept = 'all_dept'
search_form={'department':'','address':'','healthState':''}
@app.route('/')
def Index():
    print(login_user,login_admin)
    if not (login_user or login_admin):
        return redirect(url_for('login'))
    elif login_user:
        cur = mysql.connection.cursor()
        exe_str = ("SELECT  * FROM user u WHERE " + "userName = "+"'"+username_global+ "'")
        cur.execute(exe_str)
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('user_homepage.html',username = username_global,user=data)
    else:
        cur = mysql.connection.cursor()
        exe_str = "SELECT  * FROM user u "
        if search_form!={'department':'','address':'','healthState':''}:
            exe_str+= 'WHERE '
        if len(search_form['department'])!=0:
            if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
            exe_str += 'u.department = '+"'"+search_form['department']+"'"
        if len(search_form['address'])!=0:
            if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
            exe_str += 'u.address = '+"'"+search_form['address']+"'"
        if len(search_form['healthState'])!=0:
            if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
            exe_str += 'u.healthState = '+"'"+search_form['healthState']+"'"
        
        cur.execute(exe_str)
        
        data = cur.fetchall()
        cur.close()
        return render_template('index2.html', user=data )

@app.route('/login')
def login():
    return render_template('login.html' )


@app.route('/verify_account', methods = ['POST'])
def verify_account():
    username = request.form['username']
    password = request.form['password']
    
    print(username)
    print(password)
    if username == 'admin':
        global login_admin
        login_admin = True
        return redirect(url_for('Index'))
    # Else: Verify the username and password
    cur = mysql.connection.cursor()
    exe_str = ("SELECT  * FROM user u WHERE " + "userName = "+"'"+username+ "'"+ " and password = " 
                + "'"+password+"'")
    cur.execute(exe_str)
    data = cur.fetchall()
    cur.close()
    if len(data)!= 0:
        global login_user
        login_user = True
        global username_global
        username_global = username
        return redirect(url_for('Index')) 
    flash("Account and password do not match")
    return render_template('login.html' )


@app.route('/create_account')
def create_account():

    return render_template('create_account.html' )

@app.route('/verify_create_account', methods = ['POST'])
def verify_create_account():
    if request.method == "POST":
        flash("Create account successfully")
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        department = request.form['department']
        address = request.form['address']
        print(address)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user ( userName, password, gender,department,address) VALUES ( %s, %s, %s,%s, %s)", (username, password,gender,department,address))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    global login_admin
    login_admin = False
    global login_user
    login_user = False
    return redirect(url_for('Index'))



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        # userid = request.form['userid']
        #userid = request.form['id']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        department = request.form['department']
        address = request.form['address']
        healthstate = request.form['healthstate']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user ( userName, password, gender,department,address,healthState) VALUES ( %s, %s, %s,%s, %s, %s)", (username, password,gender,department,address,healthstate))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    #print('##################id_date is',type(id_data))
    cur.execute("DELETE FROM user WHERE userID=%s", [id_data])
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        department = request.form['department']
        address = request.form['address']
        healthstate = request.form['healthstate']
        cur = mysql.connection.cursor()
        print(request.form)
        cur.execute("""
               UPDATE user
               SET userName=%s, password=%s,gender=%s, department=%s, address=%s, healthstate=%s
               WHERE userID=%s
            """, ( username, password, gender, department,address,healthstate,userid))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))




# @app.route('/search/<string:department>',methods=['POST','GET'])
# def search(department):
#     global search_dept
#     search_dept = department
#     print(search_dept)
#     # userid = request.form['userid']
#     # username = request.form['username']
#     # password = request.form['password']
#     # department = request.form['department']
#     # address = request.form['address']
#     # healthstate = request.form['healthstate']
#     # cur = mysql.connection.cursor()
#     # cur.execute("""
#     #            UPDATE user
#     #            SET userID=%s, userName=%s, password=%s, department=%s, address=%s, healthstate=%s
#     #            WHERE userID=%s
#     #         """, (userid, username, password, department,address,healthstate,userid))
#     # flash("Data Updated Successfully")
#     # mysql.connection.commit()
#     return redirect(url_for('Index'))

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'POST':
        global search_dept
        search_dept = request.form['department']
        global search_form 
        search_form = copy.deepcopy(request.form)

        return redirect(url_for('Index'))
    # global search_dept
    # search_dept = department
    # print(search_dept)
    # # userid = request.form['userid']
    # # username = request.form['username']
    # # password = request.form['password']
    # # department = request.form['department']
    # # address = request.form['address']
    # # healthstate = request.form['healthstate']
    # # cur = mysql.connection.cursor()
    # # cur.execute("""
    # #            UPDATE user
    # #            SET userID=%s, userName=%s, password=%s, department=%s, address=%s, healthstate=%s
    # #            WHERE userID=%s
    # #         """, (userid, username, password, department,address,healthstate,userid))
    # # flash("Data Updated Successfully")
    # # mysql.connection.commit()
    # return redirect(url_for('Index'))


@app.route('/plot', methods = ['GET','POST'])
def plot():

    draw_barchar(mysql)
    pie_char(mysql)
    draw_barchar_address(mysql)
    return render_template('plot_page.html')

@app.route('/plot_admin', methods = ['GET','POST'])
def plot_admin():

    draw_barchar(mysql)
    pie_char(mysql)
    draw_barchar_address(mysql)
    user_draw_barchar(mysql)
    user_pie_char(mysql)
    user_draw_barchar_address(mysql)
    return render_template('plot_page_admin.html')


@app.route('/predict', methods = ['GET','POST'])
def predict():
    return render_template('predict.html')


@app.route('/predict_admin', methods=['GET', 'POST'])
def predict_admin():

    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM reported ORDER BY userID")
    data = cur.fetchall()
    cur.close()

    return render_template('predict_admin.html', students=data)

@app.route('/predict_result', methods = ['GET','POST'])
def predict_result():
    if request.method == "POST":
        # get userID
        print(username_global)
        cur = mysql.connection.cursor()
        cur.execute("SELECT userID, gender FROM user WHERE userName = %s", [username_global])
        data = cur.fetchone()
        # print(data[0])
        userid = str(data[0])
        gender = data[1]
        date = request.form['timerange']
        age = request.form['Age']
        temp = str(request.form['Temperaure'])
        place = request.form['place']
        TestResult = request.form['TestResult']

        cur.execute("SELECT * FROM reported WHERE userID = %s AND reportDate = %s", (userid, date))

        if(cur.fetchone()):
            flash("You have already reported today, please come later! ")
            return render_template('predict.html')

        isMale = 0
        if gender == 'Male':
            isMale = 1

        d = {'age': [int(age)], 'temperature': [float(temp)], 'Cough': [], 'Headache': [], 'Diarrhea': [], 'Fatigue': [],
             'SOB': [], 'Chills': [], 'conj': [], 'ST': [], 'CP': [], 'male': [isMale],
             'Grainger Library': [0], 'Illini Union': [0],'ECE building': [0], 'Illini Hall': [0], 'BookStore': [0], 'Altgeld Hall': [0]}

        d[place][0] = 1
        location_input =[]
        location_input.append(d['Grainger Library'][0])
        location_input.append(d['Illini Union'][0])
        location_input.append(d['ECE building'][0])
        location_input.append(d['Illini Hall'][0])
        location_input.append(d['BookStore'][0])
        location_input.append(d['Altgeld Hall'][0])


        date_int = int(date)

        location_output = find_location_weight(location_input, date_int)

        # print(location_output)

        d['Grainger Library'][0] = location_output[0]
        d['Illini Union'][0] = location_output[1]
        d['ECE building'][0] = location_output[2]
        d['Illini Hall'][0] = location_output[3]
        d['BookStore'][0] = location_output[4]
        d['Altgeld Hall'][0] = location_output[5]

        symptoms = ''
        if request.form.get('if_Cough'):
            symptoms = symptoms + request.form['if_Cough'] +','
            d['Cough'].append(1)
        else:
            d['Cough'].append(0)

        if request.form.get('if_headache'):
            symptoms = symptoms + request.form['if_headache'] + ','
            d['Headache'].append(1)
        else:
            d['Headache'].append(0)

        if request.form.get('if_SOB'):
            symptoms = symptoms + request.form['if_SOB'] + ','
            d['SOB'].append(1)
        else:
            d['SOB'].append(0)

        if request.form.get('if_Diarrhea'):
            symptoms = symptoms + request.form['if_Diarrhea'] + ','
            d['Diarrhea'].append(1)
        else:
            d['Diarrhea'].append(0)

        if request.form.get('if_Fatigue'):
            symptoms = symptoms + request.form['if_Fatigue'] + ','
            d['Fatigue'].append(1)
        else:
            d['Fatigue'].append(0)

        if request.form.get('if_Chills'):
            symptoms = symptoms + request.form['if_Chills'] + ','
            d['Chills'].append(1)
        else:
            d['Chills'].append(0)

        if request.form.get('if_conjunctivitis'):
            symptoms = symptoms + request.form['if_conjunctivitis'] + ','
            d['conj'].append(1)
        else:
            d['conj'].append(0)

        if request.form.get('if_ST'):
            symptoms = symptoms + request.form['if_ST'] + ','
            d['ST'].append(1)
        else:
            d['ST'].append(0)

        if request.form.get('if_CP'):
            symptoms = symptoms + request.form['if_CP'] + ','
            d['CP'].append(1)
        else:
            d['CP'].append(0)
        print(symptoms)

         # first report
        cur.execute(
            "INSERT INTO reported ( userID, temperature, placesVisited, testResult,symptoms,reportDate) VALUES ( %s, %s, %s, %s, %s, %s)",
            (userid, temp, place, TestResult, symptoms, date))
        mysql.connection.commit()

        # then predict
        user_to_predict = pd.DataFrame(d)
        print(user_to_predict)

        abspath = os.path.dirname(os.path.abspath(__file__))
        input_file = open(abspath + '/static/df_training_weights.csv')
        df_training_weights = pd.read_csv(input_file)
        X = df_training_weights.drop(['userID', 'reportDate', 'Positive', 'Unnamed: 0', 'Unnamed: 0.1'], axis=1)
        y = df_training_weights['Positive'].values.reshape(-1, 1)
        optimal_pars = Logistic_Regression(X, y)
        optimal_w, optimal_b = optimal_pars['w'], optimal_pars['b']

        # print(optimal_w)
        # print(optimal_b)

        prob = sigmoid(np.dot(user_to_predict, optimal_w) + optimal_b)[0][0]
        print(prob)


        age = int(age)
        gender = gender.lower()
        prob_perc = Density(age, gender)
        print(prob_perc)


        final_prob = float(prob) *0.2 +  float(prob_perc) *0.8
        # final_prob = 1 / (1 + np.exp(-final_prob))
        print(final_prob)

        final_prob = final_prob *100


        if final_prob<50 :
            risk_level = 'Low'
            color_class = "success"
        elif final_prob>=50 and final_prob<70:
            risk_level = 'Median'
            color_class = "warning"
        else :
            risk_level = 'High'
            color_class = "danger"

        return render_template('predict_result.html',color_class = color_class,prob=str(round(final_prob,2))+"%",risk_level=risk_level)

    # return render_template('predict.html')

@app.route('/reset_dept', methods = ['GET'])
def reset_dept():
    global search_form
    search_form={'department':'','address':'','healthState':''}
    return redirect(url_for('Index'))

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


def Density(age, gender):
    # age = int(dict_input['Age'])
    # gender = (dict_input['Gender']).lower()
    cur = mysql.connection.cursor()
    cur.execute("""
               SELECT SUM(1)
               FROM confirmed
            """)
    total_num =  cur.fetchall()[0][0]

    ###### Density factor for age
    cur = mysql.connection.cursor()
    cur.execute("""
               SELECT age,COUNT(*)
               FROM confirmed
               GROUP BY age
            """)
    data = dict(cur.fetchall())
    searched_key = str(age//10*10)+'-'+str(age//10*10+9)
    density_age = data[searched_key]/(total_num/len(data))
    #print(density_age)
    # mysql.connection.commit()

    ###### Density factor for gender
    cur = mysql.connection.cursor()
    cur.execute("""
               SELECT gender,COUNT(*)
               FROM confirmed
               GROUP BY gender
            """)
    data = dict(cur.fetchall())
    searched_key = gender
    density_gender = data[searched_key]/(total_num/len(data))
    #print(density_gender)


    ###### Seed density factor for Temperature

    density = (density_age*density_gender)
    density = 1/(1 + np.exp(-density))
    return density 

@app.route('/hotspot', methods = ['GET','POST'])
def hotspot():

    cur = mysql.connection.cursor()
    area = ['Grainger','Illini Union','ECE building','Illini Hall','BookStore','Altgeld Hall']
    exe_str = "SELECT reportDate,userID FROM reported r "
    data = []
    table = []
    out = []
    thash=[]
    for i in range(0, len(area)):
        lp_str = exe_str + 'WHERE r.placesVisited = ' + "'" + area[i] + "'"    
        cur.execute(lp_str)
        temp = cur.fetchall()
        data.append(temp)
    cur.close()    
    for j in range(0,len(data)):
        thash.append(hd.hashdate(366,20200101))
        for k in range(0,len(data[j])):
            print(type(data[j][k][0]))
            thash[j].insert(data[j][k][0],data[j][k][1])
            
    
    for i in range(0,len(thash)):
       # print('i=',i)
       # print('outlen=',len(out))
       # print('thashlen=',len(thash))
        out.append( thash[i].search(20200101,20201231))
       
        '''
    if search_form!={'department':'','address':'','healthState':''}:
        exe_str+= 'WHERE '
    if len(search_form['department'])!=0:
        if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
        exe_str += 'u.department = '+"'"+search_form['department']+"'"
    if len(search_form['address'])!=0:
        if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
        exe_str += 'u.address = '+"'"+search_form['address']+"'"
    if len(search_form['healthState'])!=0:
        if exe_str!="SELECT  * FROM user u WHERE ":exe_str+=" and "
        exe_str += 'u.healthState = '+"'"+search_form['healthState']+"'"
    
    cur.execute(exe_str)
    data = cur.fetchall()
    '''
    #area = ['Grainger','Illini Union','ECE building','Illini Hall','BookStore','Altgeld Hall']
    #data = []
    #data.append(ah.outn)
    
    show=[];
    for i in range(0,len(area)):
        show.append([area[i],out[i]])
    
    return render_template('hotspot.html',user =show)

@app.route('/search_area', methods = ['GET','POST'])
def search_area():
    if request.method == 'POST':
        global search_dept
        search_dept = request.form['department']
        global search_form 
        search_form = copy.deepcopy(request.form)

        return redirect(url_for('hotspot'))

@app.route('/hotspot_reset_dept', methods = ['GET'])
def hotspot_reset_dept():
    global search_form
    search_form={'department':'','address':'','healthState':''}
    return redirect(url_for('hotspot'))


if __name__ == "__main__":
    app.run(debug=True)




