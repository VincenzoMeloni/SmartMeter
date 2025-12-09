import os
from sensore.sensore import Sensore
from sensore.comunicatore import Comunicatore

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_path = os.path.join(base_dir, "../dataset/DATASET.csv")
    indice_path = os.path.join(base_dir, "../dataset/indice.csv")

    sensore = Sensore(csv_path=dataset_path, index_path=indice_path)
    comm = Comunicatore(sensore)

    print("Avvio comunicazione con il backend...")
    comm.start(intervallo=3)
