from scapy.all import *
import scipy.io
from scapy2dict import to_dict
import numpy as np
import os.path
from sys import argv

def remove_none(obj):

    if isinstance(obj, (list, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, tuple):
      obj = 0
      return obj
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
            for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj


def main():

    # Read pcap file
    in_file = argv[1]
    if not os.path.isfile(in_file):
        raise Exception("file_name is not there")

    packets = rdpcap(in_file)

    dataset = len(packets)
    res = np.empty((1, dataset), dtype=object)

    # Iterate over packets
    for idx, pkt in enumerate(packets):
        data = dict(to_dict(pkt))
        clearedData = remove_none(data)
        clearedData.update({"time": pkt.time})
        npRes = np.array(clearedData)
        res[0, idx] = npRes

    # Output to file
    out_file = os.path.splitext(in_file)[0]
    print('Writing to ' + out_file + '.mat')
    scipy.io.savemat(out_file, {"res": res})

if __name__ == "__main__":
    main()
