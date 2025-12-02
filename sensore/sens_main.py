from sensore import Sensore
from comunicatore import Comunicatore

if __name__ == "__main__":
    sensore = Sensore(csv_path="../dataset/DATASET.csv",index_path="../dataset/indice.csv")
    comm = Comunicatore(sensore)

    print("Avvio comunicazione con il backend...")
    comm.start(intervallo=3)
