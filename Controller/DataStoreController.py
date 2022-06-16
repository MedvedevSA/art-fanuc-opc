from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from Models import FanucMachine
from Models import StatusLog



class DataStoreController():
    def __init__(self, ip_list : list) -> None:

        self.setup_sql_config()

        self.client_ip_list = ip_list
    
    def setup_sql_config(self):
        self.db_engine = create_engine('sqlite:///database.db', echo = False)

        Session = sessionmaker(bind = self.db_engine )
        self.db_session = Session()


    def get_clients_status(self):

        response = list()       

        for clien_ip in self.client_ip_list:

            cur_client = FanucMachine(clien_ip)

            status = cur_client.get_run_status()
            """
                Status of automatic operation
                -1	:	DISCONNECTED
                0	:	STOP
                1	:	HOLD
                2	:	STaRT
                3	:	MSTR(jog mdi)
            """

            cur_time = datetime.now()

            response.append(
                ( clien_ip, str(cur_time), status)
            )

        return response

    def control_emissions_db(self):
        """
            Если статус работы станка изменился меньше чем на минуту убирает запись о изменении состояния

        #Из последних двух записей получить объекты datetime
        """
        for client_ip in self.client_ip_list:

            db_rows : List[StatusLog] = (
                self.db_session.query(StatusLog)
                .order_by(StatusLog.log_time.desc())
                .filter(StatusLog.client_ip == client_ip)
                .limit(2)
            )

            db_rows = [row for row in db_rows]

            if len(db_rows) != 2 :
                continue

            cur ,prev = db_rows

            #Если статус одинаковый подряд
            if cur.client_status == prev.client_status :
                self.db_session.delete(cur)

                continue

            cur_time, prev_time = list(
                map(
                    lambda string : datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f'),
                    [row.log_time for row in db_rows]
                )
            )
        
            if (cur_time - prev_time).seconds < 60:
                self.db_session.delete( prev )
                continue
        
        self.db_session.commit()


    def is_status_changed(self, cur_status : int, last_status : int):
        """
        Проверочная функция

        return True - Если последний статус отличается от текущего

        return False - Если изменений нету
        """

        if last_status == None:
            return True

        if cur_status == last_status.client_status:
            return False
        else:
            return True


    def get_last_status_log(self, client_ip) -> int:
        #Получить последние 2 записи client_ip из БД
        return (
            self.db_session.query(StatusLog)
            .order_by(StatusLog.log_time.desc())
            .filter(StatusLog.client_ip == client_ip)
            .first()
        )   



    def append_status_to_db(self, data):

        for client_ip, log_time, status in data:
            
            last_status_log = self.get_last_status_log(client_ip)

            if self.is_status_changed(status, last_status_log):

            
                self.db_session.add(
                    StatusLog(
                        client_ip=client_ip,
                        log_time=log_time,
                        client_status=int(status)
                    )
                )

            else:
                continue



        self.db_session.commit()

        return


    def run(self):
        self.lasttime = datetime.now()

        while True:
            time_ago = datetime.now() - self.lasttime

            if time_ago.seconds > 5 :
                self.lasttime = datetime.now()

                data = self.get_clients_status()

                self.append_status_to_db(data)
                
                self.control_emissions_db()

                print("tik tak "  + str(self.lasttime))
