from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """select distinct (Country)
                    from go_retailers
                    order by Country asc """

        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailer(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_retailers r
                where r.Country=%s"""


        cursor.execute(query,(country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getArchi(r1,r2,anno,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """select gds1.Retailer_code,gds2.Retailer_code,count(distinct gds1.Product_number) as n
                from go_daily_sales gds1 , go_daily_sales gds2
                where gds1.Retailer_code=%s and gds2.Retailer_code=%s 
                and gds1.Product_number=gds2.Product_number
                and year(gds1.Date)=year(gds2.Date) and year(gds2.Date)=%s
                group by gds1.Retailer_code,gds2.Retailer_code
                """

        cursor.execute(query,(r1,r2,anno))

        for row in cursor:
            result.append((idMap[row[0]],idMap[row[1]],row[2]))


        cursor.close()
        conn.close()
        return result