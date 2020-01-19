#!/usr/local/bin python
#-*-coding: utf-8-*-

from os import system, walk, path, environ
from configparser import ConfigParser as cp
import cx_Oracle as ora
import base64
from time import strftime, localtime, time
import random

environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

version = "1.0"

author = "Chenfei Jovany Rong"

def configCheck():
    print("***Config Check***\n")

    dd = dict()

    try:
        conf = cp()

        conf.read("conf/config.conf", encoding="utf-8-sig")

        dd["status"] = True
        dd["tns"] = conf.get("Database", "tns")
        dd["username"] = conf.get("Database", "username")
        dd["password"] = conf.get("Database", "password")
        #dd["omdb"] = conf.get("OMDB", "db")
        print("\tOK.\n")
    except:
        dd["status"] = False
        print("\tError.\n")

    return dd

def dirCheck():
    print("***Checking Input Directory***\n")

    if path.exists("Input/"):
        print("\tOK.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

        return True
        
    else:
        print("\tError.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

        return False

def fileDetect(suff):
    ct = 0

    print("***Detecting *%s Files***\n" % suff)
    
    res = list()

    for root, dirs, files in walk("Input/"):
        del root
        del dirs

        for file in files:
            if file.endswith(suff):
                ct += 1
                print("\t%s file %s: %s\n" % (suff, str(ct), file))

                res.append(file)
    
    return res
                
def omxCommit(omx, cr, db):
    with open("Input/" + omx, "r", encoding="utf-8") as f:
        temp = f.read()
        
    text = base64.b64decode(temp.encode("utf-8")).decode("utf-8")

    rowList = text.split("\n")

    dd = dict()
    
    for row in rowList:
        if " : " in row:
            tList = row.split(" : ")
            dd[tList[0].strip()] = tList[1].strip()

    sbsj = strftime('%Y-%m-%d',localtime(time()))

    score = dd["score"]
    sys_score = dd["sys_score"]
    db_score = dd["db_score"]
    tomcat_score = dd["tomcat_score"]
    province = dd["province"]
    city = dd["city"]
    district = dd["district"]
    checkdate = dd["date"]

    sql = """
    insert into ywjkmxb (ywjkmxid, sbsj, score, sys_score, db_score, tomcat_score, province, city, district, checkdate)
    values (
        sys_guid(), to_date('%s', 'yyyy-mm-dd'), '%s', '%s', '%s', '%s', '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd')
    )
    """ % (sbsj, score, sys_score, db_score, tomcat_score, province, city, district, checkdate)

    try:
        cr.execute(sql)
        db.commit()
        print("\tOK.\n")
    except Exception as e:
        print(e)
        print("SQL: %s\n" % sql)
        print("\tError.\n")

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''

    for i in range(num):
        salt += random.choice(H)

    return salt

def omyCommit(omy, cr, db):
    with open("Input/" + omy, "r", encoding="utf-8") as f:
        temp = f.read()

    text = base64.b64decode(temp.encode("utf-8")).decode("utf-8")

    eva = text.split("========")[0]
    tasks = text.split("========")[1]

    rowList = eva.split("\n")

    dd = dict()

    for row in rowList:
        if " : " in row:
            tList = row.split(" : ")
            dd[tList[0].strip()] = tList[1].strip()
    
    sbsj = strftime('%Y-%m-%d',localtime(time()))

    pmid = ranstr(20)

    name = dd["name"]
    score = dd["score"]
    month = dd["month"]
    organ = dd["organ"]
    team = dd["team"]

    syschk_score = dd["syschk_score"]
    dataedit_score = dd["dataedit_score"]
    reqtrck_score = dd["reqtrck_score"]
    prjmanchg_score = dd["prjmanchg_score"]
    otherwork_score = dd["otherwork_score"]
    tempowork_score = dd["tempowork_score"]

    sql = """
    insert into performance (
        pmid, name, score, month, organ, 
        team, syschk_score, dataedit_score, reqtrck_score, prjmanchg_score, 
        otherwork_score, tempowork_score, sbsj
    )
    values (
        '%s', '%s', %s, to_date('%s', 'yyyy-mm'), '%s', 
        '%s', %s, %s, %s, %s, 
        %s, %s, to_date('%s', 'yyyy-mm-dd')
    )
    """ % (pmid, name, score, month, organ, 
    team, syschk_score, dataedit_score, reqtrck_score, prjmanchg_score,
    otherwork_score, tempowork_score, sbsj)

    try:
        cr.execute(sql)
        db.commit()
        print("\tOK.\n")
    except Exception as e:
        print(e)
        print("SQL: %s\n" % sql)
        print("\tError.\n")

    del rowList
    del dd

    taskList = tasks.split("----")
    
    for task in taskList:
        if "task_name" not in task:
            continue
        
        rowList = task.split("\n")
        
        dd = dict()

        for row in rowList:
            if " : " in row:
                tList = row.split(" : ")
                dd[tList[0].strip()] = tList[1].strip()

        task_name = dd["task_name"]
        task_type = dd["task_type"]
        task_deli = dd["task_deli"]
        done_time = dd["done_time"]

        sql = """
        insert into performance_task (
            taskid, pmid, task_name, task_type, task_deli, done_time
        )
        values (
            sys_guid(), '%s', '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd hh24:mi:ss')
        )
        """ % (
            pmid, task_name, task_type, task_deli, done_time
        )

        try:
            cr.execute(sql)
            db.commit()
            print("\tOK.\n")
        except Exception as e:
            print(e)
            print("SQL: %s\n" % sql)
            print("\tError.\n")

def omzCommit(omz, cr, db):
    with open("Input/" + omz, "r", encoding="utf-8") as f:
        temp = f.read()

    text = base64.b64decode(temp.encode("utf-8")).decode("utf-8")

    #print(text)

    eva = text.split("========")[0]
    jbxxs = text.split("========")[1]
    warnings = text.split("========")[2]
    serverinfos = text.split("========")[3]
    tomcatinfos = text.split("========")[4]

    rowList = eva.split("\n")

    dd = dict()

    for row in rowList:
        if " : " in row:
            tList = row.split(" : ")
            dd[tList[0].strip()] = tList[1].strip()

    sbsj = strftime('%Y-%m-%d',localtime(time()))

    #checkDate = dd["date"]
    province = dd["province"]
    city = dd["city"]
    district = dd["district"]

    del dd
    del rowList

    jbxxList = jbxxs.split("\n")
    
    sql = """
        delete from om_jbxx t
        where t.province = '%s'
        and t.city = '%s'
        and t.district = '%s'
        """ % (
            province, city, district
        )

    try:
        cr.execute(sql)
        db.commit()
        print("\tOK.\n")
    except Exception as e:
        print(e)
        print("SQL: %s\n" % sql)
        print("\tError.\n")

    for jbxx in jbxxList:
        jbxx = jbxx.strip()
        if len(jbxx) == 0:
            continue

        

        sql = """
        insert into om_jbxx
        values (
            %s, '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd')
        )
        """ % (
            jbxx, province, city, district, sbsj
        )

        try:
            cr.execute(sql)
            db.commit()
            print("\tOK.\n")
        except Exception as e:
            print(e)
            print("SQL: %s\n" % sql)
            print("\tError.\n")
    
    warningList = warnings.split("\n")
    
    for warning in warningList:
        warning = warning.strip()
        if len(warning) == 0:
            continue

        sql = """
        insert into om_warning
        values (
            sys_guid(), %s, '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd')
        )
        """ % (
            warning, province, city, district, sbsj
        )

        try:
            cr.execute(sql)
            db.commit()
            print("\tOK.\n")
        except Exception as e:
            print(e)
            print("SQL: %s\n" % sql)
            print("\tError.\n")
    
    serverinfoList = serverinfos.split("----")

    for serverinfo in serverinfoList:
        if "alias" not in serverinfo:
            continue

        rowList = serverinfo.split("\n")

        dd = dict()

        for row in rowList:
            if " : " in row:
                tList = row.split(" : ")
                dd[tList[0].strip()] = tList[1].strip()

        checktime = dd["check_date"]
        alias = dd["alias"]
        max_cpu = dd["max_cpu"]
        avg_cpu = dd["avg_cpu"]
        max_memory = dd["max_memory"]
        avg_memory = dd["avg_memory"]
        max_disk = dd["max_disk"]
        avg_disk = dd["avg_disk"]

        sql = """
        insert into om_serverinfo
        values (
            sys_guid(), '%s', %s, %s, %s, %s, %s, %s, 
            '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd'), to_date('%s', 'yyyy-mm-dd')
        )
        """ % (
            alias, max_cpu, avg_cpu, max_memory, avg_memory, max_disk, avg_disk, 
            province, city, district, sbsj, checktime
        )

        try:
            cr.execute(sql)
            db.commit()
            print("\tOK.\n")
        except Exception as e:
            print(e)
            print("SQL: %s\n" % sql)
            print("\tError.\n")

    del dd
    del rowList

    tomcatinfoList = tomcatinfos.split("----")

    for tomcatinfo in tomcatinfoList:
        if "ip_port" not in tomcatinfo:
            continue

        rowList = tomcatinfo.split("\n")

        dd = dict()

        for row in rowList:
            if " : " in row:
                tList = row.split(" : ")
                dd[tList[0].strip()] = tList[1].strip()

        checktime = dd["check_date"]
        ip_port = dd["ip_port"]
        max_req = dd["max_req"]
        avg_req = dd["avg_req"]
        max_memory = dd["max_memory"]
        avg_memory = dd["avg_memory"]

        sql = """
        insert into om_tomcatinfo
        values (
            sys_guid(), '%s', %s, %s, %s, %s, 
            '%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd'), to_date('%s', 'yyyy-mm-dd')
        )
        """ % (
            ip_port, max_req, avg_req, max_memory, avg_memory, 
            province, city, district, sbsj, checktime
        )

        try:
            cr.execute(sql)
            db.commit()
            print("\tOK.\n")
        except Exception as e:
            print(e)
            print("SQL: %s\n" % sql)
            print("\tError.\n")

        
        


print("EasyOM Result Commit Tool\n")

print("Version: %s\t\tAuthor: %s\n" % (version, author))

print("Powered by Summer Moon Talk Studio, TQM, SEC, GTMAP.\n")

print("EasyOM Official Site: https://rongchenfei.com/EasyOM/\n")

print("@@@@@@@@\n\n@@@@@@@@\n")
        
system("pause")

print("***Tutorial***\n")

print("\t1. Check configs in conf/config.conf .\n")

print("\t2. Put all your omx files (*.omx) and omy files (*.omy) into Input directory.\n")

print("\t3. Press any key to commit into database automatically.\n")

print("@@@@@@@@\n\n@@@@@@@@\n")

system("pause")

config = configCheck()

print("@@@@@@@@\n\n@@@@@@@@\n")

system("pause")

isDir = False
omxList = []
omyList = []
omzList = []
isDb = False

if config["status"] == False:
    print("Press any key to EXIT ...")
else:
    isDir = dirCheck()

if isDir == False:
    pass
else:
    omxList = fileDetect(".omx")
    omyList = fileDetect(".omy")
    omzList = fileDetect(".omz")

    print("@@@@@@@@\n\n@@@@@@@@\n")

    system("pause")

if len(omxList) > 0 or len(omyList) > 0 or len(omzList) > 0:
    print("%s/%s@%s" % (config["username"], config["password"], config["tns"]))
    try:
        db = ora.connect("%s/%s@%s" % (config["username"], config["password"], config["tns"]))
        cr = db.cursor()
        isDb = True
    except Exception as e:
        print(e)

if isDb:
    for omx in omxList:
        print("***Committing %s\n***" % omx)

        omxCommit(omx, cr, db)

    for omy in omyList:
        print("***Committing %s\n***" % omy)

        omyCommit(omy, cr, db)

    for omz in omzList:
        print("***Committing %s\n***" % omz)

        omzCommit(omz, cr, db)

    cr.close()
    db.close()

    system("pause")