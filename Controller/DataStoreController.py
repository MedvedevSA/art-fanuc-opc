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
        self.db_engine = create_engine('sqlite:///database.db', echo = True)

        Session = sessionmaker(bind = self.db_engine )
        self.db_session = Session()


    def get_clients_status(self):

        response = list()       

        for clien_ip in self.client_ip_list:
            cur_client = FanucMachine(clien_ip)

            status = cur_client.get_status()
            cur_time = datetime.now()

            response.append(
                ( clien_ip, str(cur_time), status)
            )

        return response

    def save_status_to_db(self, data):

        for client_ip, log_time, status in data:

            last_saved_log = (
                self.db_session.query(StatusLog)
                .order_by(StatusLog.id.desc())
                .filter(StatusLog.client_ip == client_ip)
                .first()
            )   

            if last_saved_log != None:
                if status['run'] == last_saved_log.client_status:
                    continue

            self.db_session.add(
                StatusLog(
                    client_ip=client_ip,
                    log_time=log_time,
                    client_status=int(status['run'])
                )
            )


        self.db_session.commit()

        return


    def run(self):
        self.lasttime = datetime.now()

        while True:
            time_ago = datetime.now() - self.lasttime

            if time_ago.seconds > 5 :
                self.lasttime = datetime.now()

                data = self.get_clients_status()

                self.save_status_to_db(data)

                print("tik tak "  + str(self.lasttime))
