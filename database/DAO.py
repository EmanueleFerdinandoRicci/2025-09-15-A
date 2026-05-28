from database.DB_connect import DBConnect
from model.arco import Arco
from model.driver import Driver


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1,year2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
                    from drivers d, results r, races ra
                    where d.driverId = r.driverId and r.raceId = ra.raceId 
                    and ra.year between %s and %s
                    and r.`position` is not null
                    order by d.driverId """

        cursor.execute(query, (year1,year2,))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2, idMapD):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as id1, r2.driverId as id2, count(*) as peso
                    from results r1, results r2, races ra
                    where ra.raceId = r1.raceId and ra.raceId = r2.raceId 
                    and r1.constructorId = r2.constructorId 
                    and r1.driverId > r2.driverId 
                    and r1.`position` is not null and r2.`position` is not null
                    and ra.`year` between %s and %s
                    group by r1.driverId, r2.driverId
                    order by peso asc """

        cursor.execute(query, (year1,year2,))

        for row in cursor:
            results.append(Arco(idMapD[row["id1"]],idMapD[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results