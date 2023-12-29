#!/usr/local/bin/python3
#_*_coding:UTF_8_*_
from flask import Flask, render_template, request,redirect, url_for, request, session, flash, redirect, url_for, jsonify
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import io
import sys
import base64
import tempfile
import pandas as pd
import os
import datetime
import matplotlib as mpl
from matplotlib import font_manager, rc
from matplotlib import font_manager as fm
from matplotlib import rc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from flask import jsonify
import shutil




application = Flask(__name__)
application.secret_key='secret_key'
PASSWORD = 'sd@4366'  # Replace with your actual password
mpl.rcParams['axes.unicode_minus'] = False
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf';
#fontprop = fm.FontProperties(fname=font_path)

# 폰트 매니저 재구성
fm._rebuild()

# 폰트 패밀리 설정
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

application.config['JSON_AS_ASCII'] = False

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html', error=None)



@application.route('/')
def home():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    return render_template("home.html")

@application.route("/analyze")
def analyze():
    return render_template("analyze.html")

userlist_folder='/workspace/INBODY/userlist'


@application.route("/userlist")
def userlist():
    user_names = []
    for user_folder in os.listdir(userlist_folder):
        user_folder_path = os.path.join(userlist_folder, user_folder)
        if os.path.isdir(user_folder_path):
            user_names.append(user_folder)

    
    return render_template("userlist.html", user_names=user_names)



@application.route('/set_session')
def set_session():
    # Get the 'name' parameter from the query string
    name = request.args.get('name')

    # Set the 'NAME' session variable
    session['NAME'] = name

    return jsonify({'message': 'Session variable NAME set successfully'})

@application.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        user_name_to_delete = request.form.get('user_name')

        if user_name_to_delete:
            user_folder_path = os.path.join("userlist", user_name_to_delete)

            if os.path.exists(user_folder_path) and os.path.isdir(user_folder_path):
                shutil.rmtree(user_folder_path)  # 사용자 폴더를 삭제합니다.
                return jsonify({"message": "User deleted successfully"})

    return jsonify({"error": "Failed to delete user"})

@application.route("/dataresult", methods=["POST"])
def dataresult():
    if request.method == "POST":
        NAME = request.form.get('name')
        GENDER = request.form.get('user_gender')
        AGE = int(request.form.get('age'))
        HEIGHT = float(request.form.get('height'))
        WEIGHT = float(request.form.get("weight"))
        WHR = float(request.form.get("whr"))
        
    current_datetime=datetime.datetime.now()
    current_date=current_datetime.date()
    current_time=current_datetime.time()
    DATE=current_datetime

    BMI = WEIGHT / (HEIGHT * 0.01) ** 2    

    if GENDER == 'Female':
        FFM = (1.07 * WEIGHT) - (128 * ((WEIGHT ** 2) / (HEIGHT ** 2)))-5.4
    else:
        FFM = (1.10 * WEIGHT) - (128 * ((WEIGHT ** 2) / (HEIGHT ** 2)))

    ABF=WEIGHT-FFM     
    PBF=ABF/WEIGHT*100
    
  


    
    if GENDER == 'Female':
        BMR = 655.0955 + 9.5634 * WEIGHT + 1.8496 * HEIGHT - AGE * 4.6756
    else:
        BMR = 66.4736 + 13.7516 * WEIGHT + 5.0033 * HEIGHT - AGE * 6.7556



    if GENDER=='Female':
        if AGE<=29:
            standard_pbf_min=0.189
            standard_pbf_max=0.26
        elif 30<=AGE<=34:
            standard_pbf_min=0.189
            standard_pbf_max=0.271
        elif 35<=AGE<=39:
            standard_pbf_min=0.189
            standard_pbf_max=0.278
        elif 40<=AGE<=44:
            standard_pbf_min=0.198
            standard_pbf_max=0.287
        elif 45<=AGE<=49:
            standard_pbf_min=0.20
            standard_pbf_max=0.288
        elif 50<=AGE<=54:
            standard_pbf_min=0.22
            standard_pbf_max=0.302
        elif 55<=AGE<=59:
            standard_pbf_min=0.231
            standard_pbf_max=0.306
        else :
            standard_pbf_min=0.23
            standard_pbf_max=0.326
    else:
        if AGE<=24:
            standard_pbf_min=0.093
            standard_pbf_max=0.233
        elif 25<=AGE<=29:
            standard_pbf_min=0.102
            standard_pbf_max=0.244
        elif 30<=AGE<=34:
            standard_pbf_min=0.123
            standard_pbf_max=0.252
        elif 35<=AGE<=39:
            standard_pbf_min=0.129
            standard_pbf_max=0.261
        elif 40<=AGE<=44:
            standard_pbf_min=0.132
            standard_pbf_max=0.269
        elif 45<=AGE<=49:
            standard_pbf_min=0.135
            standard_pbf_max=0.276
        elif 50<=AGE<=54:
            standard_pbf_min=0.198
            standard_pbf_max=0.287
        elif 55<=AGE<=59:
            standard_pbf_min=0.202
            standard_pbf_max=0.293
        else :
            standard_pbf_min=0.203
            standard_pbf_max=0.298


    if standard_pbf_min<= PBF<=standard_pbf_max:
        y0=20
        remainder_y=(standard_pbf_max-standard_pbf_min)/20
        y1=(PBF-standard_pbf_min)/remainder_y

        y=y0+y1


    elif PBF>standard_pbf_max:
        y0=20
        y1=20
        remainder_y=(PBF-standard_pbf_max)/4
        y2=(PBF-standard_pbf_max)/remainder_y
    
        y=y0+y1+y2

    else:
        remainder_y=PBF/20
        y=PBF/remainder_y

    #체질량지수
    if BMI<18.5:
        remainder_x=BMI/20
        x=BMI/remainder_x
    elif 18.5<=BMI<=22.9:
        x0=20
        remainder_x=(22.9-18.5)/15
        x1=(BMI-18.5)/remainder_x
        x=x0+x1
    else:
        x0=20
        x1=20
        remainder_x=(BMI-22.9)/8


        x2=(BMI-22.9)/remainder_x

        x=x0+x1+x2




    # 데이터와 라벨을 정의합니다.
    N = 3
    ind = np.arange(N)
    i = (0, 0, 20)
    h = (0, 20, 0)
    g = (20, 0, 0)
    f = (0, 0, 20)
    e = (0, 20, 0)
    d = (20, 0, 0)
    c = (0, 0, 20)
    b = (0, 20, 0)
    a = (20, 0, 0)

    fig, ax = plt.subplots(figsize=(2, 2))

    # 그래프를 그립니다.
    plt.xlim(0, 60)
    plt.bar(10, a, color='aliceblue', width=20)
    plt.bar(30, b, color='lightsteelblue', width=20)
    plt.bar(50, c, color='slategrey', width=20)
    plt.bar(10, d, color='antiquewhite', bottom=a, width=20)
    plt.bar(30, e, color='wheat', bottom=b, width=20)
    plt.bar(50, f, color='tan', bottom=c, width=20)
    plt.bar(10, g, color='gainsboro', bottom=np.add(a, d), width=20)
    plt.bar(30, h, color='silver', bottom=np.add(b, e), width=20)
    plt.bar(50, i, color='darkgrey', bottom=np.add(c, f), width=20)

    # 그래프 스타일 설정
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    # 폰트 설정

    # 그래프에 텍스트 표시
    plt.text(5, 50, '마른비만', fontsize=6)
    plt.text(6, 29, '저체중', fontsize=6)
    plt.text(6, 8, '저지방\n저체중', fontsize=6)

    plt.text(27, 50, '과지방', fontsize=6)
    plt.text(25, 29, '표준체형', fontsize=6)
    plt.text(26, 8, '저지방\n근육형', fontsize=6)

    plt.text(48, 50, '비만', fontsize=6)
    plt.text(46, 29, '근육형\n과체중', fontsize=6)
    plt.text(47, 8, '운동\n부족형', fontsize=6)

    # 각 막대 위에 점 그리기
    for x, y in zip([x], [y]):
        plt.annotate('v', (x, y), color='red', fontsize=10, ha='center', va='center')






    # 그래프를 이미지로 저장
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', dpi=200)
    img_stream.seek(0)
    img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    img_tag = f'<img src="data:image/png;base64,{img_data}" alt="Graph">'
    plt.close()
    

    if GENDER == 'Female':
        BMR = 655.0955 + 9.5634 * WEIGHT + 1.8496 * HEIGHT - AGE * 4.6756
    else:
        BMR = 66.4736 + 13.7516 * WEIGHT + 5.0033 * HEIGHT - AGE * 6.7556


 

    #체지방량 최대최소
    abf_min=WEIGHT*standard_pbf_min*0.01
    abf_max=WEIGHT*standard_pbf_max*0.01

    # 표준체중
    if GENDER == 'Female':
        standard_weight_min = 17.8 * ((HEIGHT * 0.01) ** 2)
        standard_weight_max = 23.1 * ((HEIGHT * 0.01) ** 2)
    else:
        standard_weight_min = 19.8 * (HEIGHT * 0.01) ** 2
        standard_weight_max = 24.2 * (HEIGHT * 0.01) ** 2

    standard_weight = (standard_weight_min + standard_weight_max) / 2

    # 체질량지수
    if 18.5 <= BMI <= 22.9:
        a20 = 8
        a2 = 18.5
        b2 = BMI - 18.5
        c2 = 0
        d2 = 22.9 - BMI

        remainder = (22.9 - 18.5) / 10
        b20 = b2 / remainder
        d20 = d2 / remainder
        c20=c2/remainder

    elif BMI > 22.9:
        a20 = 8
        a2 = 18.5
        b2 = 22.9 - 18.5
        c2 = (BMI - 22.9)/2
        d2 = 0

        remainder = (22.9 - 18.5) / 10

        b20 = b2 / remainder
        d20 = 0
        c20=c2/remainder

    else:
        a2 = BMI
        remainder=BMI/8
        a20=a2/remainder
        b2 = 0
        c2 = 0
        d2 = 0

        b20 = 0
        d20 = 0
        c20=0

    #체지방률
    if 100*standard_pbf_min<= PBF<=standard_pbf_max*100:
        a30=8
        a3=standard_pbf_min*100
        b3=PBF-(standard_pbf_min*100)
        c3=0
        c30=0
        d3=(standard_pbf_max*100)-PBF

        remainder=(b3+d3)/10
        b30=b3/remainder
        d30=d3/remainder


    elif PBF>standard_pbf_max*100:
        a30=8
        a3=standard_pbf_min
        b3=standard_pbf_max-standard_pbf_min
        c3=(PBF-standard_pbf_max)/10
        d3=0

        d30=0
        remainder=b3/10
        b30=b3/remainder
        c30=c3/remainder

    else:
        a3=PBF
        remainder=PBF/8
        a30=a3/remainder
        b3=0
        c3=0
        d3=0

        b30=0
        d30=0
        c30=0


    #표준체중
    if GENDER=='Female':
        standard_weight_min=17.8*(HEIGHT*0.01)**2
        standard_weight_max=23*(HEIGHT*0.01)**2
    else:
        standard_weight_min=19.8*(HEIGHT*0.01)**2
        standard_weight_max=24.2*(HEIGHT*0.01)**2

    standard_weight=(standard_weight_min+standard_weight_max)/2




    if standard_weight_min<= WEIGHT<=standard_weight_max:
        a10=8
        a1=standard_weight_min
        b1=WEIGHT-standard_weight_min
        c1=0
        d1=standard_weight_max-WEIGHT

        remainder=((standard_weight_max)-(standard_weight_min))/10
        b10=b1/remainder
        d10=d1/remainder
        c10=0


    elif WEIGHT>standard_weight_max:
        a10=8
        a1=standard_weight_min
        b1=standard_weight_max-standard_weight_min
        c1=(WEIGHT-standard_weight_max)/2
        d1=0

        remainder=((standard_weight_max)-(standard_weight_min))/10
        b10=b1/remainder
        d10=0
        c10=c1/remainder


    else:
        a1=WEIGHT
        remainder=WEIGHT/8
        a10=a1/remainder
        b1=0
        c1=0
        d1=0

        b10=0
        d10=0
        c10=0
        
        
    def calculate_MM(GENDER,FFM):
    # 근육비율 계산****************************************************
        if GENDER == 'Female':
        #muscle_ratio = ((HEIGHT - 105) * 0.9 * 0.45 + WEIGHT * 0.45) / 2
            MM=FFM*0.9195
        else:
        #muscle_ratio = ((HEIGHT - 100) * 0.9 * 0.45 + WEIGHT * 0.45) / 2
            MM=FFM*0.92
        return MM
    MM = calculate_MM(GENDER, FFM)
        
    def calculate_mm_min(GENDER, AGE, WEIGHT):
     #근육량 최대최소*********************여자 근육량 최대 최소 계산 조정
        if GENDER=='Female':
            if AGE <= 30:
                mm_min=0.01*47.9*WEIGHT
            
            elif AGE>30:
                mm_min=0.01*56.1*WEIGHT
        else:
            mm_min=0.01*54*WEIGHT#53.185,60.1
        return mm_min
    mm_min = calculate_mm_min(GENDER, AGE, WEIGHT)
        
    def calculate_mm_max(GENDER, AGE, WEIGHT):
     #근육량 최대최소*********************여자 근육량 최대 최소 계산 조정
        if GENDER=='Female':
             if AGE <= 30:
                mm_max=0.01*53.86*WEIGHT
            
             elif AGE >30:
                mm_max=0.01*64.4*WEIGHT
        else:
            mm_max=0.01*63.973*WEIGHT#56.5637,63.973
        return mm_max
    mm_max = calculate_mm_max(GENDER, AGE, WEIGHT)
       

    if GENDER == 'Female':
        if MM < mm_min:
            a4 = MM
            remainder=MM/8
            a40=a4/remainder
            b40=0
            c4=0
            c40=0
            d40=0

        elif mm_min <=MM <= mm_max:
            a40 = 8
            b4 = (MM) - mm_min
            d4=mm_max-MM
            remainder =(mm_max-mm_min)/ 10

            b40 = b4 / remainder
            
            d40 = d4 / remainder
            c4=0
            c40=0
        else:
            a40 = 8
            b40 = 10
            c4 = (MM) - mm_max
            d40 = 0
            remainder =MM/ 10
            c40=c4/remainder

    else:
        if MM < mm_max:
            a4 =MM
            remainder=MM/8
            c4=0

            a40=a4/remainder
            b40=0
            c40=0
            d40=0

        elif mm_min<= MM<= mm_max:
            a40 = 8
            b4 = (MM) - mm_min
            d4=mm_max-MM
            remainder = (mm_max-mm_min) / 10
            c4=0
            b40 = b4 / remainder
 
            d40 = d4 / remainder
            c40=0
        else:
            a40 = 8
            b40 = 10
            c4 = (MM) - mm_max
            d40 = 0
            remainder =MM/ 10
            c40=c4/remainder


    # 결과 출력
    data = {
        '항목': ['근육량', '체지방률', '체질량지수', '체중'],
        '이하': [a40, a30, a20, a10],
        '적정': [b40, b30, b20, b10],
        '적정max-체중': [d40, d30, d20, d10],
        '이상': [c4/2, c3/1.5, c2*2.6, c1],
        '적정범위': [10, 10, 10, 10]
    }

    df = pd.DataFrame(data)
    df.index = ['근육량', '체지방률', '체질량지수', '체중']


    x_weight=a10+b10+c1+d10+1
    x_bmi=a20+b20+c2*2.6+d20+1
    x_pbf=a30+b30+c3/1.5+d30+1
    x_mm=a40+b40+(c4/2)+d40+1

    fig, ax = plt.subplots(figsize=(4,1.4))

    df.plot.barh(stacked=True,width=0.1, color=('black', 'grey', 'darkgrey', 'steelblue', 'white'), ax=ax).get_legend().remove()
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)

    plt.annotate(WEIGHT,(x_weight,2.9),fontsize=6)
    plt.annotate(f"  {standard_weight_min:.2f}"+' '+'~ '+f"{standard_weight_max:.2f}",(35,2.8),fontsize=5)


    plt.annotate(f"{BMI :.2f}",(x_bmi,1.9),fontsize=6)
    plt.text(35,1.95,'  18.5 ~ 22.9',fontsize=5)


    plt.annotate(f"{PBF:.2f}",(x_pbf,0.9),fontsize=6)
    plt.annotate(f"  {standard_pbf_min*100:.2f}"+' ''~ '+f"{standard_pbf_max*100:.2f}",(35,0.95),fontsize=5)
    plt.annotate(f"{MM:.2f}",(x_mm,-0.1),fontsize=6)
    plt.annotate(f"  {mm_min:.2f}"+' '+'~'+' '+f"{mm_max:.2f}",(35,-0.1),fontsize=5)
    plt.axvline(8,0,3,color='lightgrey',linestyle='--')
    plt.axvline(18,0,3,color='lightgrey',linestyle='--')
    plt.axvline(34,0,3,color='grey',linestyle='--')
    plt.hlines(0.5,0,47,color='lightgrey',linestyle='solid')
    plt.hlines(1.5,0,47,color='lightgrey',linestyle='solid')
    plt.hlines(2.5,0,47,color='lightgrey',linestyle='solid')



    plt.yticks(fontsize=5)    

    
    img_stream1 = io.BytesIO()
    plt.savefig(img_stream1, format='png', dpi=200)
    img_stream1.seek(0)
    img_data1 = base64.b64encode(img_stream1.read()).decode('utf-8')
    img_tag1 = f'<img src="data:image/png;base64,{img_data1}" alt="Graph">'
    plt.close()
    
###############################################################
#체성분분석

    if GENDER=='Female':
        BMR=655.0955+9.5634*WEIGHT+1.8496*HEIGHT-AGE*4.6756
    else:
         BMR=66.4736 + 13.7516*WEIGHT + 5.0033*HEIGHT - AGE*6.7556



    #BFM=WEIGHT*ABF*0.01

    FFM=WEIGHT-ABF

    M=FFM-MM

    TBW=(WEIGHT-ABF)*0.72

    P=MM-TBW
    #표준체중
    if GENDER=='Female':
        standard_weight_min=17.8*(HEIGHT*0.01)**2
        standard_weight_max=21.6*(HEIGHT*0.01)**2
    else:
        standard_weight_min=19.8*(HEIGHT*0.01)**2
        standard_weight_max=24.2*(HEIGHT*0.01)**2

    standard_weight=(standard_weight_min+standard_weight_max)/2


    # 데이터와 라벨을 정의합니다.
    N = 4
    ind = np.arange(N)

    d = (80, 60, 40, 20)
    c = (0, 20, 20, 20)
    b = (0, 0, 20, 20)
    a = (0, 0, 0, 20)
   

    fig, ax = plt.subplots(figsize=(2.5,2))
     # 그래프를 그립니다.
    plt.bar(ind, a, color='olive')
    plt.bar(ind, b, color='darkkhaki', bottom=a)
    plt.bar(ind, c, color='khaki', bottom=np.add(a, b))
    plt.bar(ind, d, color='lemonchiffon', bottom=np.add(np.add(a, b), c))
    
     # 그래프 스타일 설정
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

     # 그래프에 텍스트 표시
    plt.text(-0.15, 60, '체중',fontsize=6)
    plt.text(-0.35, 40, '표준체중',fontsize=6)

    plt.text(0.65, 60, '제지방량',fontsize=6)
    plt.text(0.65, 10, '체지방량',fontsize=6)

    plt.text(1.75, 60, '근육량',fontsize=6)
    plt.text(1.75, 30, '무기질',fontsize=6)
    plt.text(1.65, 10, '체지방량',fontsize=6)

    plt.text(2.65, 70, '체수분량',fontsize=6)
    plt.text(2.75, 50, '단백질',fontsize=6)
    plt.text(2.75, 30, '무기질',fontsize=6)
    plt.text(2.65, 10, '체지방량',fontsize=6)

    plt.annotate(WEIGHT,(-0.15,52),fontsize=5)
    plt.annotate(f"{standard_weight:.2f}",(-0.25,33),fontsize=5)
    plt.annotate(f"{(WEIGHT-ABF):.2f}",(0.82,54),fontsize=5)
    plt.annotate(f"{ABF:.2f}",(0.8,4),fontsize=5)
    plt.annotate(f"{MM:.2f}",(1.85,53),fontsize=5)
    plt.annotate(f"{M:.2f}",(1.8,23),fontsize=5)
    plt.annotate(f"{ABF:.2f}",(1.8,4),fontsize=5)
    plt.annotate(f"{TBW:.2f}",(2.8,63),fontsize=5)
    plt.annotate(f"{P:.2f}",(2.85,43),fontsize=5)
    plt.annotate(f"{M:.2f}",(2.85,23),fontsize=5)
    plt.annotate(f"{ABF:.2f}",(2.8,4),fontsize=5)
    
    img_stream2 = io.BytesIO()
    plt.savefig(img_stream2, format='png', dpi=200)
    img_stream2.seek(0)
    img_data2 = base64.b64encode(img_stream2.read()).decode('utf-8')
    img_tag2 = f'<img src="data:image/png;base64,{img_data2}" alt="Graph">'
    plt.close()
    
    ratio=[TBW,P,M,ABF]
    labels=['체수분량','단백질','무기질','체지방량']
    colors = ['lightsteelblue', 'darkkhaki', 'slategrey', 'beige']
    wedgeprops={'width': 0.7, 'edgecolor': 'white', 'linewidth': 5}

    explode = [0, 0.10, 0, 0.10]

    plt.pie(ratio, labels=labels, colors=colors,autopct='%.1f%%', startangle=260,wedgeprops=wedgeprops, counterclock=False, explode=explode, textprops={'fontsize': 16})
    
    img_stream4 = io.BytesIO()
    plt.savefig(img_stream4, format='png', dpi=200)
    img_stream4.seek(0)
    img_data4 = base64.b64encode(img_stream4.read()).decode('utf-8')
    img_tag4= f'<img src="data:image/png;base64,{img_data4}" alt="Graph">'
    plt.close()
#인바디 점수
#80점을 기준으로 근육량과 지방량이 +-1에 따라 +-점씩 변화
#90점이상이면 매우강함, 80-90이면 강함, 70-80보통, 70미만 약함
    BODY_AGE=0
  


    #복부비만율
    if GENDER=='Female':
        whr_min=0.70
        whr_max=0.85
    else:
        whr_min=0.75
        whr_max=0.90
      
    if (whr_min)<= WHR <=(whr_max):
        whr_0=0.3
        whr_a=whr_min
        whr_b=WHR-whr_min
        whr_c=0
        whr_A=0.2
        remainder=(whr_max-whr_min)/0.25
        whr_B=whr_b/remainder
        whr_C=0
        whr_D=0.25-whr_B
    elif WHR>whr_max:
        whr_0=0.3
        whr_a=whr_min
        whr_b=whr_max
        whr_c=WHR-whr_max
        whr_A=0.25
        remainder=(whr_max-whr_min)/0.25
        whr_B=(whr_max-whr_min)/remainder
        whr_C=whr_c/remainder
        whr_D=0
    else :
        whr_0
        remainder=(whr_min-WHR)/0.2
        whr_A=WHR/remainder
        whr_B=0
        whr_C=0
        whr_D=0
    
    
    DCV=standard_weight*33


    
    
    cal_data = {'항목': ['신체연령','1일필요열량', '기초대사량', '복부비만율'],
                '범례': [0,0,0,whr_0],
                '이하': [0,0, 0, whr_A],
                '적정': [0,0, 0, whr_B],
                ' ': [0,0, 0, whr_D],
                '이상': [0,0, 0, whr_C]}

    df_cal = pd.DataFrame(cal_data)
    #df_cal.index = ['신체\n연령','1일   \n필요열량', '기초\n대사량', '복부\n비만율']
    fig, ax = plt.subplots(figsize=(6,4))
    df_cal.plot.barh(stacked=True,width=0.2,color=('white','black', 'grey', 'gainsboro','blue'), ax=ax).get_legend().remove()
    plt.yticks([])
     # 그래프 주석 추가
    f = "{:.2f}"
    whr_x = (whr_A + whr_B + whr_C+whr_D)+0.15
  
    ax.annotate(f.format(BODY_AGE), (0.35, -0.1), fontsize=14)
    ax.annotate(f.format(DCV), (0.35, 0.9), fontsize=14)
    ax.annotate(f.format(BMR), (0.35, 1.95), fontsize=14)
    ax.annotate(f.format(WHR), (whr_x+0.2, 2.95), fontsize=14)
    ax.annotate(f.format(whr_min), (0.3+0.18, 3.2), fontsize=10)
    ax.annotate(f.format(whr_max), (0.3+0.2+0.22, 3.2), fontsize=10)######################################################
    ax.text(0.55, 1.9, 'kcal',fontsize=12)
    ax.text(0.55, 0.9, 'kcal',fontsize=12)
    ax.text(0.55, -0.1, '세',fontsize=12)
    ax.text(0.05, -0.1, '신체연령',fontsize=14)
    ax.text(0.05, 0.9, '1일필요열량',fontsize=14)
    ax.text(0.05, 1.9, '기초대사량',fontsize=14)
    ax.text(0.05, 2.9, '복부비만율',fontsize=14)
    ax.legend(loc='lower right')
    ax.set_xlim(0, 1)
    plt.yticks(fontsize=11)
 
      # 그래프 스타일 설정
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(True)


  

    plt.hlines(0.5,0,45,color='lightgrey',linestyle='solid')
    plt.hlines(1.5,0,45,color='lightgrey',linestyle='solid')
    plt.hlines(2.5,0,45,color='lightgrey',linestyle='solid')

    img_stream3 = io.BytesIO()
    plt.savefig(img_stream3, format='png', dpi=200)
    img_stream3.seek(0)
    img_data3 = base64.b64encode(img_stream3.read()).decode('utf-8')
    img_tag3 = f'<img src="data:image/png;base64,{img_data3}" alt="Graph">'
    plt.close()
    

    session['DATE'] =DATE
    session['NAME'] = NAME
    session['BMI'] = BMI
    session['MM'] = MM
    session['WEIGHT'] =WEIGHT
    session['TBW'] = TBW
    
    return render_template("dataresult.html", DATE=DATE,GENDER=GENDER, NAME=NAME, HEIGHT=HEIGHT, AGE=AGE, WEIGHT=WEIGHT,graph=img_tag, graph1=img_tag1, graph2=img_tag2, graph3=img_tag3, graph4=img_tag4)

@application.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        NAME = session.get('NAME')  # 사용자 이름 입력 받기
        DATE = session.get('DATE')
        BMI = session.get('BMI')
        MM = session.get('MM')
        WEIGHT = session.get('WEIGHT')
        TBW = session.get('TBW')
    
        if NAME:
            user_folder = os.path.join("userlist", NAME)
            os.makedirs(user_folder, exist_ok=True)

            # 데이터 저장
            date_now = datetime.datetime.now()
            user_data_path = os.path.join(user_folder, "data.csv")
            if os.path.exists(user_data_path):
                user_data = pd.read_csv(user_data_path)
            else:
                user_data = pd.DataFrame(columns=["날짜", "체중", "체질량지수", "근육량", "체수분량"])

            new_row = {
                "날짜": DATE,
                "체중": WEIGHT,
                "체질량지수": BMI,
                "근육량": MM,
                "체수분량": TBW
            }
            user_data = user_data.append(new_row, ignore_index=True)
            user_data.to_csv(user_data_path, index=False)
            return jsonify({"message": "Data added successfully"})

    return jsonify({"error": "Something went wrong"})



    
    
@application.route('/create_graph', methods=['GET', 'POST'])
def create_graph():
    # 사용자 이름 가져오기
    NAME = session.get('NAME')
    
    if NAME:
        # 사용자 데이터 가져오기
        user_data = get_user_data(NAME)

        if len(user_data) >= 2:
            
            df=pd.DataFrame(user_data)
                        # Convert the '날짜' column to datetime
            df['날짜'] = pd.to_datetime(df['날짜'])

            # Calculate the difference between the last and second-to-last rows
            last_weight = df.iloc[-1]['체중']
            previous_weight = df.iloc[-2]['체중']
            weight_difference =  last_weight - previous_weight 
            # 체중 그래프 생성
            weight_fig = px.line(user_data, x='날짜', y='체중', title=f'체중 변화-----Weight Difference: {weight_difference:.2f} kg')
            weight_fig.update_traces(mode='lines+markers+text')
            weight_fig.update_xaxes(title_text='날짜')
            weight_fig.update_yaxes(title_text='체중 (kg)')
            weight_fig.update_layout(width=700,height=300)
            for i, row in user_data.iterrows():
                weight_fig.add_trace(go.Scatter(x=[row['날짜']], y=[row['체중']], text=[row['체중']],textfont=dict(size=16, color='red'),mode='text',showlegend=False))
            img_stream00 = io.BytesIO()
            weight_fig.write_image(img_stream00, format='png')
            img_stream00.seek(0)
            img_data00 = base64.b64encode(img_stream00.read()).decode('utf-8')
            img_tag00 = f'<img src="data:image/png;base64,{img_data00}" alt="Graph">'

            # 체질량지수 그래프 생성
            last_bmi = df.iloc[-1]['체질량지수']
            previous_bmi = df.iloc[-2]['체질량지수']
            bmi_difference =   last_bmi - previous_bmi 

            bmi_fig = px.line(user_data, x='날짜', y='체질량지수', title=f'체질량지수 변화 -----BMI Difference: {bmi_difference:.2f}')
            bmi_fig.update_traces(mode='lines+markers')
            bmi_fig.update_xaxes(title_text='날짜')
            bmi_fig.update_yaxes(title_text='체질량지수')
            bmi_fig.update_layout(width=700,height=300)
            for i, row in user_data.iterrows():
                bmi_fig.add_trace(go.Scatter(x=[row['날짜']], y=[row['체질량지수']], text=[f'{row["체질량지수"]:.2f}'],textfont=dict(size=16, color='red'),mode='text',showlegend=False))
            img_stream01 = io.BytesIO()
            bmi_fig.write_image(img_stream01, format='png')
            img_stream01.seek(0)
            img_data01 = base64.b64encode(img_stream01.read()).decode('utf-8')
            img_tag01 = f'<img src="data:image/png;base64,{img_data01}" alt="Graph">'

            # 근육량 그래프 생성
            last_mm = df.iloc[-1]['근육량']
            previous_mm = df.iloc[-2]['근육량']
            mm_difference = last_mm - previous_mm  
          
            mm_fig = px.line(user_data, x='날짜', y='근육량', title=f'근육량 변화-----MM Difference: {mm_difference:.2f}')
            mm_fig.update_traces(mode='lines+markers')
            mm_fig.update_xaxes(title_text='날짜')
            mm_fig.update_yaxes(title_text='근육량')
            mm_fig.update_layout(width=700,height=300)
            for i, row in user_data.iterrows():
                mm_fig.add_trace(go.Scatter(x=[row['날짜']], y=[row['근육량']],  text=[f'{row["근육량"]:.2f}'],textfont=dict(size=16, color='red'),mode='text',showlegend=False))
            img_stream02 = io.BytesIO()
            mm_fig.write_image(img_stream02, format='png')
            img_stream02.seek(0)
            img_data02 = base64.b64encode(img_stream02.read()).decode('utf-8')
            img_tag02 = f'<img src="data:image/png;base64,{img_data02}" alt="Graph">'

            # 체수분량 그래프 생성
            last_tbw = df.iloc[-1]['체수분량']
            previous_tbw = df.iloc[-2]['체수분량']
            tbw_difference =  last_tbw - previous_tbw  
            
            tbw_fig = px.line(user_data, x='날짜', y='체수분량', title=f'체수분량 변화-----TBW Difference: {tbw_difference:.2f}')
            tbw_fig.update_traces(mode='lines+markers')
            tbw_fig.update_xaxes(title_text='날짜')
            tbw_fig.update_yaxes(title_text='체수분량')
            tbw_fig.update_layout(width=700,height=300)
            for i, row in user_data.iterrows():
                tbw_fig.add_trace(go.Scatter(x=[row['날짜']], y=[row['체수분량']],  text=[f'{row["체수분량"]:.2f}'],textfont=dict(size=16, color='red'),mode='text',showlegend=False))
            img_stream03 = io.BytesIO()
            tbw_fig.write_image(img_stream03, format='png')
            img_stream03.seek(0)
            img_data03 = base64.b64encode(img_stream03.read()).decode('utf-8')
            img_tag03 = f'<img src="data:image/png;base64,{img_data03}" alt="Graph">'

            return render_template('create_graph.html', graph00=img_tag00, graph01=img_tag01, graph02=img_tag02, graph03=img_tag03)
    return "User data does not have enough rows for generating graphs"


####캐싱 사용해서 속도 증가시키기
# 사용자 데이터를 가져오는 함수 (이미 이전에 정의한 함수입니다)
def get_user_data(user_name):
    # 사용자 데이터를 저장하는 디렉터리 경로 설정
    user_folder = os.path.join("userlist", user_name)

    # 데이터 파일 경로
    user_data_path = os.path.join(user_folder, "data.csv")

    # 데이터 파일이 존재하는 경우 데이터를 읽어옴
    if os.path.exists(user_data_path):
        user_data = pd.read_csv(user_data_path)
    else:
        user_data = pd.DataFrame(columns=["날짜", "체중", "체질량지수", "근육량", "체수분량"])

    return user_data

if __name__ == '__main__':
    application.run(host='0.0.0.0',debug=False)



