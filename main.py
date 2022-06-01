from Controller import DataStoreController

def main():
    ip = [
        "192.168.1.28",
        "192.168.1.29",
        "192.168.1.30",
        "192.168.1.230",
    ]
    controller = DataStoreController(ip)

    controller.run()


if __name__ == "__main__" :
    main()