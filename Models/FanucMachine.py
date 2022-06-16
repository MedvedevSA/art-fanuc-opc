import ctypes
import os
import re

libpath = os.path.join(
    os.path.dirname(__file__),  
    "../Fwlib32/Fwlib32.dll"
)
focas = ctypes.cdll.LoadLibrary(libpath)

class statinfo_ODBST(ctypes.Structure):
    _fields_ = [    ("hdck", ctypes.c_short) ,                   #/* Status of manual handle re-trace */
                    ("tmmode", ctypes.c_short) ,                 #/* T/M mode selection              */
                    ("aut", ctypes.c_short) ,                    #/* AUTOMATIC/MANUAL mode selection */
                    ("run", ctypes.c_short) ,                    #/* Status of automatic operation   */
                    ("motion", ctypes.c_short) ,                 #/* Status of axis movement,dwell   */
                    ("mstb", ctypes.c_short) ,                   #/* Status of M,S,T,B function      */
                    ("emergency", ctypes.c_short) ,              #/* Status of emergency             */
                    ("alarm", ctypes.c_short) ,                  #/* Status of alarm                 */
                    ("edit", ctypes.c_short) ]                   #/* Status of program editing       */


class FanucMachine():
    def __init__(self, ip, port = 8193, timeout=2) -> None:
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.libh = ctypes.c_ushort(0)

    def connect(self):
        ret = focas.cnc_allclibhndl3(
            self.ip.encode(),
            self.port,
            self.timeout,
            ctypes.byref(self.libh),
        )
        if ret != 0:
            raise ConnectionError(f"Failed to connect to cnc! ({ret})")

    def disconnect(self):
        ret = focas.cnc_freelibhndl(self.libh)
        if ret != 0:
            raise Exception(f"Failed to free library handle! ({ret})")

    def get_run_status(self):

        try:
            return int((self.get_status())['run'])
        except:
            return -1

    def get_status(self):

        self.connect()

        try:
            statinfo = statinfo_ODBST()
            res = focas.cnc_statinfo(self.libh ,ctypes.byref(statinfo))

            stat_dict = dict()
            for field, _ in statinfo._fields_:
                stat_dict[field] = getattr(statinfo, field)

            if res != 0:
                raise ConnectionError(f"Failed to read cnc id! ({res})")

            return stat_dict

        except Exception as e:
            return res

        finally:
            self.disconnect()           