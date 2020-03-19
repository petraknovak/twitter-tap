import json
import datetime
import os
import errno
import os.path
import time
import gzip

class filer:

    def __init__(self, dataDir, N=10000):
        if not os.path.exists(dataDir):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dataDir)
        self.dataDir = dataDir
        self.data = []
        self.N = N

    def emit(self, dictEntry):
        self.data.append(dictEntry)
        if len(self.data) >= self.N:   # add condition  "if new day"
            self.toDisc()

    def toDisc(self):
        #generate directory name & create it if id does not exist UTC!
        now = datetime.datetime.utcnow()
        directory = os.path.join(self.dataDir, now.strftime("%Y/%m/%d"))
        os.makedirs(directory, mode=0o777, exist_ok=True)  # don't raise an error if the directory already exists

        #generate filename
        fileName = now.strftime("%Y-%m-%d_%H-%M-%S")+".json"
        print(fileName)

        #put tweets to gzipped json file
        with gzip.GzipFile(os.path.join(directory, fileName + ".gz"), 'w') as outfile:
            outfile.write(json.dumps(self.data).encode('utf-8'))

        #reset the data variable to []
        self.data = []

    #def __del__(self):
    #    print(len(self.data))
     #   self.toDisc()


if __name__ == '__main__':
    f = filer("./data", N=100)
    f.emit({"First" : 1} )
    time.sleep(1)
    f.emit({"Second": 2,  "this": 77 })
    time.sleep(1)
    f.emit({"Third": 3, 33: 77})
    time.sleep(1)
    f.emit({"Fourth": 4, 44: 77})
    time.sleep(1)
    f.emit({"Fifth": 5, 55: 77})
    time.sleep(1)
    f.emit({"Sixth": 6, 66: 77})
    time.sleep(1)
    f.emit({"Seventh": 7, 777: 77})

    f.toDisc()              # to save on disc the remaining


