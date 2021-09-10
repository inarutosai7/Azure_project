# import my SQL
#MySQL configure data usr name & host info.. etc
import mySQL_Config
# import python  my SQL packages
import pymysql
import  random
import  re



global connSQL, cursor, usrInput, idNO, cusNO, usrName, Budget, cost, SpendDateTime, Catalog

# Initial MySQL
def Connect():
    # 建立連線
    print('Connect to SQL')
    # get MySQL Connect
    connSQL = pymysql.connect(host=mySQL_Config.host, port=mySQL_Config.port, user=mySQL_Config.user, passwd=mySQL_Config.passwd, db=mySQL_Config.db, charset=mySQL_Config.charset)
    cursor = connSQL.cursor()
    print('Successfully Connected!')

def DisConnect():
    print('Close Connection MySQL')
    connSQL.close()

def InsertData(idNO, cusNO, usrName, Budget, cost, SpendDateTime, Catalog):

    sql ="""INSERT INTO userdata (INDEXNO, CUSTOMERNO, CNAME, MAXLIMIT, COST, DATATIME,CATEGORY)
            VALUES ('04','01' ,'JOHN', '3000', '45','2020-04-24 14:59:57',' ');
         """
    cursor.execute(sql)


def GrabResultTxt(Resultxt):
    print('extract Cost numbers  from string')
    cost = re.findall(r'\b\d+\b', Resultxt)
    print('you spend:  \n ',cost)


    # pass
