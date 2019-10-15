from flask import Flask, render_template, redirect, url_for, request, json, session, flash, jsonify
import datetime
import pymysql
import random
import mysql.connector
from mysql.connector import Error
from db import databaseCMS
import requests
#from PIL import Image
import json


app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'ms1'

class RequestLaporan:
   
    def __init__(self):
        self.req_id = ''
        self.org_id = ''
        self.ktgri_id = ''
        self.req_kodeLaporan = ''
        self.req_judul = ''
        self.req_deskripsi = ''
        self.req_tujuan = ''
        self.req_tampilan = ''
        self.req_periode = ''
        self.req_deadline = ''
        self.req_file = ''
        self.req_PIC = ''
        self.req_penerima = ''
        self.sch_id = ''
        self.report_id = ''
        self.query_id = ''
        self.reqSch_hari = ''
        self.reqSch_bulan = ''
        self.reqSch_tanggal = ''
        self.reqSch_groupBy = ''
        self.reqSch_reportPIC = ''
        self.reqSch_orgNama = ''
        self.reqSch_ktgriNama = ''
        self.reqSch_lastUpdate = ''
        self.reqSch_aktifYN = ''
        self.reqSch_reportPenerima = ''
        
       
        

    #BUAT GENERATE REQUESTID SECARA OTOMATIS
    @app.route('/getNumberId', methods = ['POST','GET'])
    def get_numberID():
        try: 
            db = databaseCMS.db_request()
            

            cursor = db.cursor()
     
            cursor.execute('select count(req_id) from t_request where month(req_date) = month(now())')
            
            record = cursor.fetchall()
            # clear = str(record).replace('(','').replace(',)','')

            numbId = []

            for x in record:
                nDict = {
                'numberId' : x[0]
                }
                numbId.append(nDict)

            numberId = json.dumps(numbId)
            
            return numberId
            # return int(clear)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
        
    @app.route('/generateRequestId', methods = ['POST','GET'])
    def generateRequestID():
        
        now  = datetime.datetime.now()

        try: 
            db = databaseCMS.db_request()
            

            cursor = db.cursor()
     
            cursor.execute('select count(req_id) from t_request where month(req_date) = month(now())')
            
            record = cursor.fetchone()
            clear = str(record).replace('(','').replace(',)','')

            reqId = []

            
            #requestId = 'REQ_'+str(now.strftime('%Y%m'))+str(clear).zfill(5)

            for x in record:
                reqIdDict = {
                'requestId' : 'REQ_'+str(now.strftime('%Y%m'))+str(clear).zfill(5)
                }
                reqId.append(reqIdDict)

            reqIdFin = json.dumps(reqId)
            
            return reqIdFin

            

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")


        return reqIdFin

    @app.route('/getEmail/<uId>', methods=['POST','GET'])
    def getEmail(uId):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()

            cursor.execute('SELECT user_email FROM m_user WHERE user_id = "'+uId+'" ')

            resultEmail = cursor.fetchall()
            
            return json.dumps(resultEmail)
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/getNamaOrg/<idOrg>', methods=['POST','GET'])
    def getNamaOrg(idOrg):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()

            cursor.execute('SELECT org_nama from m_organisasi WHERE org_id ="'+idOrg+'"')

            org = cursor.fetchall()
            # clear = str(org).replace("('",'').replace("',)","")
            orgList = []
            for i in org:
                orgDict = {
                'org_name' : i[0]
                }
                orgList.append(orgDict)

            namaOrg = json.dumps(orgList)


            return namaOrg

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    @app.route('/getNamaKat/<idKat>', methods=['POST','GET'])
    def getNamaKat(idKat):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()

            cursor.execute('SELECT ktgri_nama from m_kategori WHERE ktgri_id ="'+idKat+'"')

            kategori = cursor.fetchall()

            katList = []
            for i in kategori:
                katDict = {
                'kat_name' : i[0]
                }
                katList.append(katDict)

            namaKat = json.dumps(katList)


            return namaKat
            
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


    @app.route('/namaOrganisasi', methods=['POST','GET'])
    #BUAT MENDAPATKAN ORGANISASI DARI MYSQL
    def namaOrganisasi():
        
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
        
            cursor.execute('select org_id, org_nama from m_organisasi where org_aktifYN = "Y" order by org_id')
            resultOrg = cursor.fetchall()
            

            orgList = []
            for row in resultOrg:
                orgDict = {
                    'Id': row[0],
                    'Name': row[1]}

                orgList.append(orgDict)

            orgResult=json.dumps(orgList)

            print("=== [ namaOrganisasi ] ===")
            print(orgResult)
            print("=========================")
            return orgResult         

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
                    
    #BUAT MENDAPATKAN KATEGORI DARI MYSQL
    @app.route('/namaDept', methods=['POST','GET'])
    def namaDept():
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute('select ktgri_id, ktgri_nama from m_kategori where ktgri_aktifYN = "Y" Order by ktgri_id')
            
            resultDept = cursor.fetchall()

            deptList = []
            for row in resultDept:
                deptDict = {
                'Id' : row[0],
                'Name' : row[1]
                }
                deptList.append(deptDict)
            deptResult = json.dumps(deptList)
            
            return deptResult
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    #BUAT MENAMPILKAN LIST PIC DARI MYSQL
    @app.route('/namaPIC', methods=['POST','GET'])
    def namaPIC():
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute(''.join(['select user_id, user_name, user_email from m_user where user_flag = "User" ']))
            
            resultPIC = cursor.fetchall()

            picList = []
            for row in resultPIC:
                picDict = {
                'Id' : row[0],
                'Name' : row[1],
                'Email' : row[2]
                }
                picList.append(picDict)
            picResult = json.dumps(picList)
             
            abc = json.loads(picResult)

            print(abc)
            return picResult
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/namaPenerima', methods=['POST','GET'])                    
    def namaPenerima():
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute(''.join(['select user_id, user_name, user_email from m_user where user_flag = "User" ']))
            
            resultPen = cursor.fetchall()

            penList = []

            for row in resultPen:
                penDict = {
                'Id' : row[0],
                'Name' : row[1],
                'Email' : row[2]
                }
                penList.append(penDict)
            penResult = json.dumps(penList)
            


            return penResult
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
    
    @app.route('/updateDataPassword/<data>', methods = ['POST', 'GET'])
    def updateDataPassword(data):
        if request.method == 'POST':
            requestData = json.loads(data)

            for x in requestData:
                uId = requestData['uId']
                old_pass = requestData['passLama']
                new_pass = requestData['passBaru']
                conf_pass = requestData['konfPass']

            try: 
                db = databaseCMS.db_request()

                cursor = db.cursor()
                cursor.execute(' UPDATE m_user SET user_password = "'+conf_pass+'" WHERE user_id = "'+uId+'" AND user_password = "'+old_pass+'" ')
                db.commit()

            except Error as e:
                print("Error while connecting file MySQL", e)
                flash('Error,', e)

            finally:
                    #Closing DB Connection.
                        if(db.is_connected()):
                            cursor.close()
                            db.close()
                        print("MySQL connection is closed")


    @app.route('/testId', methods = ['POST','GET'])
    def testId():
        r = requests.get('http://127.0.0.1:5001/generateRequestId')


        r2 = json.dumps(r.json())
        rId = json.loads(r2)
        for x in rId:
            req_id = x['requestId']

        return r2

    @app.route('/addNewRequest/<data>', methods=['POST','GET'])
    def addNewRequest(data):

        if request.method == 'POST':
            
            

            r = requests.get('http://127.0.0.1:5001/generateRequestId')
            r2 = json.dumps(r.json())
            rId = json.loads(r2)
            for x in rId:
                req_id = x['requestId']



            reqSch_aktifYN = 'Y'
            reqSch_groupBy = 'Dr. Andre Lembong' 
            req_dateAccept = None
            req_endDate=None
            req_status='Waiting'
            req_prioritas='1'
            reqSch_lastUpdate = datetime.datetime.now()
            req_date = datetime.datetime.now()

            requestData = json.loads(data)

            for x in requestData:
                reqSch_bulan = requestData['Bulan']
                req_deadline = requestData['Deadline']
                req_deskripsi = requestData['Deskripsi']
                req_file = requestData['File']
                reqSch_hari = requestData['Hari']
                req_judul = requestData['Judul']
                ktgri_id = requestData['KtgriId']
                org_id = requestData['OrgId']
                req_PIC = requestData['PIC']
                req_periode = requestData['Periode']
                prog_id = requestData['ProgId']
                req_tampilan = requestData['Tampilan']
                reqSch_tanggal = requestData['Tanggal']
                req_tujuan = requestData['Tujuan']
                user_id = requestData['UserId']
                req_kodeLaporan = requestData['kodLap']
                reqSch_ktgri = requestData['schKtgri']
                reqSch_lastUpdate = requestData['schLastUpdate']
                reqSch_org = requestData['schOrg']
                reqSch_reportPIC = requestData['schPIC']
                reqSch_penerima = requestData['schPenerima']
                

            print(requestData)
            print(req_deskripsi)
            print(req_id)
            


            try: 
                db = databaseCMS.db_request()

                cursor = db.cursor()
                cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (req_id, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                               req_tujuan, req_tampilan, req_periode, req_deadline, req_file, req_date,
                                req_dateAccept, req_endDate, req_status, req_PIC, req_prioritas))
                db.commit()

            

                cursor.execute('INSERT INTO t_reqSchedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (req_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy, reqSch_reportPIC, reqSch_org, reqSch_ktgri, reqSch_lastUpdate, reqSch_aktifYN,
                                reqSch_penerima))
                db.commit()

            
            #     

            except Error as e :
                print("Error while connecting file MySQL", e)
                flash('Error,', e)
            finally:
                    #Closing DB Connection.
                        if(db.is_connected()):
                            cursor.close()
                            db.close()
                        print("MySQL connection is closed")
            



        

    #BUAT MENAMPILKAN LIST REQUEST PADA MENU
    @app.route('/listRequestUser/<uId>', methods = ['POST','GET'])
    def listRequestUser(uId):

        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute  (''.join(['SELECT req_id ,IFNULL(req_judul,""), IFNULL(req_date,""),IFNULL(req_deadline,""), IFNULL(req_status,""), IFNULL(req_PIC,""), IFNULL(req_kodelaporan, "") from t_request WHERE req_status IN ("On Process" , "Waiting")  AND user_id="'+uId+'" ORDER BY req_id desc']))
            resultReqUser = cursor.fetchall()

            reqUserList = []

            for row in resultReqUser:
                reqUserDict = {
                'RequestId' : row[0],
                'RequestJudul' : row[1],
                'RequestDate' : row[2],
                'RequestDeadline' : row[3],
                'RequestStatus' : row[4],
                'RequestPIC' : row[5],
                'RequestKodeLaporan' : row[6]
                }
                reqUserList.append(reqUserDict)
            reqUserResult = json.dumps(reqUserList)

            print(reqUserResult)
            return reqUserResult
        
        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
        

    #BUAT MENAMPILKAN REQUEST YANG UDAH KELAR
    @app.route('/listFinished/<uId>', methods = ['POST','GET'])
    def listFinished(uId):


        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['SELECT req_kodeLaporan, req_judul, req_date, req_PIC, req_endDate, b.req_id, rating FROM t_request a LEFT JOIN m_rating b ON a.req_id = b.req_id WHERE req_status = "Finished" and user_id="'+uId+'" ORDER BY req_date desc']))
            resultFinished = cursor.fetchall()

            finishedList = []

            for row in resultFinished:
                finishedDict = {
                'RequestKodeLaporan' : row[0],
                'RequestJudul' : row[1],
                'RequestDate' : str(row[2]),
                'RequestPIC' : row[3],
                'RequestEndDate' : str(row[4]),
                'RequestId' : row[5],
                'RequestRating' : row[6]
                }
                finishedList.append(finishedDict)
            finishedResult = json.dumps(finishedList)

            print(finishedResult)
            return finishedResult

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")







    
             
    #BUAT NAMPILIN GAMBAR DI DETAIL TASK
    # def showImage(self, request_id):
    #     try: 
    #         connection = mysql.connector.connect(
    #         host='localhost',
    #         database='cms_request',
    #         user='root',
    #         password='qwerty')
    #         if connection.is_connected():
    #             db_Info= connection.get_server_info()
    #         print("Connected to MySQL database...",db_Info)

    #         cursor = connection.cursor()
    #         cursor.execute('SELECT req_file from t_request where req_id = "'+request_id+'"')
    #         connection.commit()

    #         record = cursor.fetchone()[0]
    #         return record
    #         print ("Your connected...",record)

    #     except Error as e :
    #         print("Error while connecting file MySQL", e)
    #         flash('Error,', e)
    #     finally:
    #             #Closing DB Connection.
    #                 if(connection.is_connected()):
    #                     cursor.close()
    #                     connection.close()
    #                 print("MySQL connection is closed")

    #BUAT GET REPORT ID SESUAI USER YANG REQUEST
    @app.route('/getReportIdEdit/<uId>', methods=['POST','GET'])
    def getReportIdEdit(uId):
        try: 

            db = databaseCMS.db_template()
            cursor = db.cursor()
            
            cursor.execute(' select distinct report_id from cms_template.m_report a left join cms_request.t_request b on a.report_id = b.req_kodelaporan where user_id = "'+uId+'" ')
            # cursor.execute('select report_id from m_report')
            
            listKodeEditReport = cursor.fetchall()

            listKodeEdit = []

            for row in listKodeEditReport:
                listDict = {
                'ReportId' : row[0]
                }
                listKodeEdit.append(listDict)

            resultListKode = json.dumps(listKodeEdit)
            
            return resultListKode

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")   

    #BUAT INSERT REQUEST EDIT 

    @app.route('/editRequest/<editData>', methods=['POST','GET'])
    def editRequest(editData):
        if request.method == 'POST':
            loadEditData = json.loads(editData)
            
            r = requests.get('http://127.0.0.1:5001/generateRequestId')
            r2 = json.dumps(r.json())
            rId = json.loads(r2)
            for x in rId:
                req_id = x['requestId']



            reqSch_aktifYN = 'Y'
            reqSch_groupBy = 'Dr. Andre Lembong' 
            req_dateAccept = None
            req_endDate=None
            req_status='Waiting'
            req_prioritas='1'
            reqSch_lastUpdate = datetime.datetime.now()
            req_date = datetime.datetime.now()

            
        
            reqSch_bulan = loadEditData['Bulan']
            req_deadline = loadEditData['Deadline']
            req_deskripsi = loadEditData['Deskripsi']
            req_file = loadEditData['File']
            reqSch_hari = loadEditData['Hari']
            req_judul = loadEditData['Judul']
            ktgri_id = loadEditData['KtgriId']
            org_id = loadEditData['OrgId']
            req_PIC = loadEditData['PIC']
            req_periode = loadEditData['Periode']
            prog_id = loadEditData['ProgId']
            req_tampilan = loadEditData['Tampilan']
            reqSch_tanggal = loadEditData['Tanggal']
            req_tujuan = loadEditData['Tujuan']
            user_id = loadEditData['UserId']
            req_kodeLaporan = loadEditData['kodLap']
            reqSch_ktgri = loadEditData['schKtgri']
            reqSch_lastUpdate = loadEditData['schLastUpdate']
            reqSch_org = loadEditData['schOrg']
            reqSch_reportPIC = loadEditData['schPIC']
            reqSch_penerima = loadEditData['schPenerima']




        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (req_id, prog_id, user_id,org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode, req_deadline, req_file, req_date,
                            req_dateAccept, req_endDate, req_status, req_PIC, req_prioritas))
            db.commit()

            

            cursor.execute('INSERT INTO t_reqSchedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (req_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy, reqSch_reportPIC, reqSch_org, reqSch_ktgri, reqSch_lastUpdate, reqSch_aktifYN,
                            reqSch_penerima))
            db.commit()

            
            print ("Edit Request Sent")

        except Error as e :
            print("Error while connecting file MySQL", e)
            flash('Error,', e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")




    #BUAT UPDATE STATUS CANCEL PADA REQUEST
    @app.route('/cancR/<data>', methods=['POST','GET'])
    def cancR(data):
        
        a = json.loads(data)

        
        request_id = a['request_id']


        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute('UPDATE t_request SET req_status = "Cancel"  WHERE req_id = "'+request_id+'" ')            
            
            db.commit()
           
            
            print('REQUEST CANCELEEEED')

            
          
            return 'OK'
        except Error as e : 
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
    
    @app.route('/reject/<data>', methods = ['POST','GET'])
    def rejectRequest(data):
        loadData = json.loads(data)

        uName = loadData['userName']
        request_id = loadData['request_id']



        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()
            cursor.execute('UPDATE t_request SET req_status = "Rejected by '+uName+'" WHERE req_id = "'+request_id+'" ')

            db.commit()
            
        except Error as e : 
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
    ##################################################################################################
    

    #BUAT LIST AVAILABLE TASK

    @app.route('/availableTask', methods=['POST','GET'])
    def availableTask():
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('''SELECT req_id, req_judul, user_name, ktgri_nama,
                                        req_date, req_deadline, req_prioritas, user_posisi, org_nama
                                        FROM t_request a
                                        LEFT JOIN m_user b
                                            ON  a.user_id = b.user_id
                                        LEFT JOIN m_kategori c
                                            ON  a.ktgri_id = c.ktgri_id
                                        LEFT JOIN m_organisasi d
                                            ON a.org_id = d.org_id
                                        WHERE req_status LIKE 'Waiting%' ORDER BY req_deadline asc''')
            resultAvail = cursor.fetchall()

            availTask = []

            for row in resultAvail:
                availDict = {
                'requestId' : row[0],
                'requestJudul' : row[1],
                'userNama' : row[2],
                'requestKategori' : row[3],
                'requestTanggal' : str(row[4]),
                'requestDeadline' : str(row[5]),
                'requestPrioritas' : row[6],
                'userPosisi' : row[7],
                'requestOrganisasi' : row[8]
                }
                availTask.append(availDict)
            listAvailTask = json.dumps(availTask)

            return listAvailTask
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT LIST TASK PROGRAMMER
    @app.route('/listTask/<uId>', methods=['POST','GET'])
    def listTask(uId):


        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            #listTask = cursor.execute(''.join(['SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_deadline, req_prioritas FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_PIC = "'+session['username']+'" ORDER BY req_id']))
            cursor.execute('SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_deadline, req_prioritas, req_status, prog_id FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_status = "On Process" and prog_id = "'+uId+'" ORDER BY req_id desc')
            resultTask = cursor.fetchall()

            taskProg = []

            for row in resultTask:
                taskDict = {
                'requestId' : row[0],
                'requestJudul' : row[1],
                'userName' : row[2],
                'requestKategori' : row[3],
                'requestTanggal' : str(row[4]),
                'requestDeadline' : str(row[5]),
                'requestPrioritas' : row[6],
                'requestStatus' : row[7],
                'progId' : row[8]
                }
                taskProg.append(taskDict)
            listTask = json.dumps(taskProg)
            
            return listTask

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")


    @app.route('/historyTask/<uName>')
    def historyTask(uName):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            
            cursor.execute('SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_endDate, req_kodelaporan FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_status = "Finished" and req_PIC = "'+uName+'" ORDER BY req_id desc')
            resultHist = cursor.fetchall()
            
            histList = []

            for row in resultHist:

                histDict = {
                'requestId' : row[0],
                'requestJudul' : row[1],
                'userName' : row[2],
                'requestKategori' : row[3],
                'requestTanggal' : str(row[4]),
                'requestEndDate' : str(row[5]),
                'requestKodeLaporan' : row[6]
                }

                histList.append(histDict)
            historyTask = json.dumps(histList)



            return historyTask

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT DETAIL TASK SAAT TEKAN TOMBOL SELECT

    @app.route('/getDetailTask/<request_id>')
    def getDetailTask(request_id):
        
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['SELECT a.req_id, req_judul, req_deskripsi, org_nama, ktgri_nama, req_tampilan, req_periode, req_deadline, req_file, reqSch_tanggal, reqSch_bulan, reqSch_hari, req_kodeLaporan, req_tujuan  FROM t_request a LEFT JOIN m_organisasi b ON a.org_id = b.org_id LEFT JOIN m_kategori c ON a.ktgri_id = c.ktgri_id LEFT JOIN t_reqSchedule d ON a.req_id = d.req_id  WHERE a.req_id = "'+request_id+'"']))            
           
            resultDetail = cursor.fetchall()

            detailTaskList = []

            for row in resultDetail:
                detailDict = {
                'requestId' : row[0],
                'requestJudul' : row[1],
                'requestDeskripsi' : row[2],
                'requestOrganisasi' : row[3],
                'requestKategori' : row[4],
                'requestTampilan' : row[5],
                'requestPeriode' : row[6],
                'requestDeadline' : str(row[7]),
                'requestFile' : str(row[8]),
                'reqSchTanggal' : row[9],
                'reqSchBulan' : row[10],
                'reqSchHari' : row[11],
                'requestKodeLaporan' : row[12],
                'requestTujuan' : row[13]
                }
                detailTaskList.append(detailDict)

            detail_task = json.dumps(detailTaskList)


            
            return detail_task

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")


    @app.route('/accRequest/<detail>', methods=['POST','GET'])
    def accRequest(detail):
        accReq = datetime.datetime.now()

        detailR = json.loads(detail)

        for x in detailR:
            request_id = detailR['request_id']
            uId = detailR['uId']
            uName = detailR['uName']


        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('update t_request set req_dateAccept = "'+str(accReq)+'",req_status = "On Process", req_PIC = "'+uName+'", prog_id = "'+uId+'" where req_id = "'+request_id+'"')

            db.commit()
            

            print ("Record Updated successfully ")
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")




    #BUAT UPDATE STATUS REQUEST 
    def confirmRequest(self, request_id):
        self.confirm_request =''
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_status = "Confirmed"  WHERE req_id = "'+request_id+'"']))            
            
            db.commit()
            
            confirm_request = cursor.fetchone()
         
            return confirm_request
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

        

    #BUAT PROGRAMMER TELAH SELESAI MENGERJAKAN REQUEST DAN 
    #MENGINPUT KODE LAPORAN UNTUK REQUEST TERSEBUT 
    def listKodeLaporan(self):
        try:
            db = databaseCMS.db_template()

            cursor = db.cursor()
            cursor.execute('SELECT report_id from m_report')

            listKodeLap = cursor.fetchall()

            return listKodeLap
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed") 



    @app.route('/finishRating/<data>', methods=['POST','GET'])
    def finishRating(data):

        i = json.loads(data)
        
        rating = i['rating']
        keterangan = i['keterangan']
        request_id = i['request_id']

        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()
            cursor.execute(' UPDATE m_rating SET rating = "'+rating+'" , keterangan ="'+keterangan+'" WHERE req_id = "'+request_id+'"    ')

            db.commit()

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed") 


    #BUAT TOMBOL FINISH CONNECT TO DB TO GET STATUS GINISHED
    @app.route('/finReq/<kode>', methods=['POST','GET'])
    def finReq(kode):
        
        loadKode = json.loads(kode)
        endDate = datetime.datetime.now()

        for i in loadKode:
            request_id = loadKode['request_id']
            kodLap = loadKode['kode_laporan']

        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_status = "Finished"  WHERE req_id = "'+request_id+'"']))            
            db.commit()
            

            cursor.execute('INSERT INTO m_rating VALUES (%s,%s,%s)',(request_id,'0',''))
            db.commit()


            cursor.execute(''.join(['UPDATE t_request SET req_endDate = "'+str(endDate)+'", req_kodeLaporan = "'+kodLap+'"  WHERE req_id = "'+request_id+'"']))            
            db.commit()
            

            print('Report Finished')
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")    

    #BUAT TOMBOL FINISH UNTUK INPUT KODE REPORT DI TASK PROGRAMMER
    def inputKodeFinish(self, request_id, kodLap):
        self.endDate = datetime.datetime.now()
        
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_endDate = "'+str(self.endDate)+'", req_kodeLaporan = "'+kodLap+'"  WHERE req_id = "'+request_id+'"']))            
            
            db.commit()

            # kode_finish = cursor.fetchone()

            # return kode_finish
            
            print(request_id, kodLap)
         
            
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    def availableTaskSPV(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            listAvailTaskSPV = cursor.execute('''SELECT user_name, user_posisi, req_id, req_judul, ktgri_nama, org_nama, req_date, 
                                            req_deadline, req_prioritas
                                            FROM    m_user a
                                            LEFT JOIN   t_request b
                                            ON  a.user_id = b.user_id
                                            LEFT JOIN m_kategori c
                                            ON  b.ktgri_id = c.ktgri_id
                                            LEFT JOIN   m_organisasi d
                                            ON  b.org_id = d.org_id
                                            WHERE req_status LIKE 'Waiting%' ORDER BY req_deadline asc ''')
            listAvailTaskSPV = cursor.fetchall()

            for taskSPV in listAvailTaskSPV:
                uName = taskSPV[0]
                posisi = taskSPV[1]
                reqId = taskSPV[2]
                reqJud = taskSPV[3]
                ktgri = taskSPV[4]
                org = taskSPV[5]
                rDate = taskSPV[6]            
                rDead = taskSPV[7]
                rPrio = taskSPV[8]
                

                return listAvailTaskSPV
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")


    @app.route('/onProgressTask', methods=['POST','GET'])
    def onProgressTask():
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('''SELECT user_name, req_id, req_judul, ktgri_nama, org_nama, req_date, 
                            req_dateAccept, req_PIC, req_deadline
                            FROM m_user a
                            LEFT JOIN t_request b
                            ON a.user_id = b.user_id
                            LEFT JOIN m_kategori c
                            ON b.ktgri_id = c.ktgri_id
                            LEFT JOIN m_organisasi d
                            ON b.org_id = d.org_id
                            WHERE req_status = "On Process" ''')

            onProgTask = cursor.fetchall()

            onProg = []

            for x in onProgTask:
                onProgDict= {
                'onNama' : x[0],
                'onId' : x[1],
                'onJud' : x[2],
                'onKat' : x[3],
                'onOrg' : x[4],
                'onDate' : str(x[5]),
                'onDateAccept' : str(x[6]),
                'onPIC' : x[7],
                'onDeadline' : str(x[8])
                }
                onProg.append(onProgDict)

                
            onProgress = json.dumps(onProg)

            return onProgress

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")



#===========================[ TEMPLATE LAPORAN ] ======================================

class TemplateLaporan:
    def __init__(self):
        self.kode_laporan = ''

#BUAT GET DATA REPORT_ID
    @app.route('/getReportId', methods=['POST','GET'])
    def getReportID():
        try: 

            db = databaseCMS.db_template()
            cursor = db.cursor()
     
            # cursor.execute(' select report_id from cms_template.m_report a left join cms_request.t_request b on a.report_id = b.req_kodelaporan where user_id = "'+uId+'" ')
            cursor.execute('select report_id from m_report')
            
            listKodeReport = cursor.fetchall()

            listKode = []

            for row in listKodeReport:
                listDict = {
                'ReportId' : row[0]
                }
                listKode.append(listDict)

            resultListKode = json.dumps(listKode)
            
            return resultListKode

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")     

#BUAT NAMPILIN KOLOM BERDASARKAN REPORT_ID YANG DIPILIH        
    def viewReportID(self, kodeLaporan):
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
        
            cursor.execute(''.join(['SELECT report_tampilan FROM m_report WHERE report_id = "'+kodeLaporan+'"']))

            connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
    
    @app.route('/getDataReport/<report_id>', methods=['POST','GET'])
    def getDataReport(report_id):
       

        try: 
            db = databaseCMS.db_template()

            cursor = db.cursor()
     
            cursor.execute(''.join(['select report_id ,report_judul, report_tujuan, org_id, ktgri_id from m_report where report_id = "'+report_id+'"']))
            
            record = cursor.fetchall()
            
            data = []

            for row in record:
                dataDict = {
                'reportId' : row[0],
                'reportJudul' : row[1],
                'reportTujuan' : row[2],
                'reportOrg' : row[3],
                'reportKtgri' : row[4]
                }
                data.append(dataDict)

            dataReport = json.dumps(data)
            
            return dataReport

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")







    @app.route('/getCurrentDisplay/<report_id>', methods=['POST','GET'])
    def getCurrentDisplay(report_id):

        try: 
            db = databaseCMS.db_template()
          

            cursor = db.cursor()
     
            cursor.execute(''.join(['select nama_kolom from m_detailH where report_id = "'+report_id+'"']))
            
            record = cursor.fetchall()
            clear = str(record).replace("('",'').replace("',)",'').replace('[','').replace(']','')

            clearResult = json.dumps(clear)
            print(clearResult)

            return clearResult

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")






    def getRevisiDisplay(self, request_id):
        self.revisi_display=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            #cursor.execute(''.join(['select req_id, req_tampilan from t_request where req_id = "'+request_id+'"']))
            cursor.execute('select req_id, req_tampilan from t_request where req_id = "'+request_id+'"')
            record = cursor.fetchall()
            #clear = str(record).replace("('",'').replace("',)",'')
            return record

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def updateStatusCancel(self, request_id):
        self.cancel=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()

            cursor.execute('update t_request set req_status = "Cancelled" where req_id = "'+request_id+'"')

            connection.commit()
            record = cursor.fetchone()
            return record
            print ("Record Updated successfully ")
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")


if __name__ == "__main__":
    app.run(debug=True, port='5001')