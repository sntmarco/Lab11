from database.DB_connect import DBConnect
from model.connessioni_rifugi import Connessioni
from model.rifugi import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def get_rifugi(year):
        cnx = DBConnect.get_connection()
        lista_rifugi = []

        if cnx is None:
            print("❌ Errore di connessione al database")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT DISTINCT r.*
                    FROM rifugio r, connessione c
                    WHERE r.id = c.id_rifugio1 OR r.id = c.id_rifugio2 AND anno < %s
                    ORDER BY nome ASC
                """
        try:
            cursor.execute(query, (year,))
            for row in cursor:
                rifugi = Rifugio(
                    id=row["id"],
                    nome=row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                    aperto=row["aperto"],
                )
                lista_rifugi.append(rifugi)
        except Exception as e:
            print(f"Errore durante la query get_rifugi: {e}")
            lista_rifugi = None
        finally:
            cursor.close()
            cnx.close()

        return lista_rifugi

    @staticmethod
    def get_connessione_rifugi(year):
        cnx = DBConnect.get_connection()
        lista_connessioni = []

        if cnx is None:
            print("❌ Errore di connessione al database")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
                    FROM connessione
                    WHERE anno < %s """
        try:
            cursor.execute(query, (year,))
            for row in cursor:
                hub = Connessioni(
                    id=row["id"],
                    id_rifugio1=row["id_rifugio1"],
                    id_rifugio2=row["id_rifugio2"],
                    distanza=row["distanza"],
                    difficolta=row["difficolta"],
                    durata=row["durata"],
                    anno=row["anno"],
                )
                lista_connessioni.append(hub)
        except Exception as e:
            print(f"Errore durante la query get_connessione_rifugi: {e}")
            lista_connessioni = None
        finally:
            cursor.close()
            cnx.close()

        return lista_connessioni