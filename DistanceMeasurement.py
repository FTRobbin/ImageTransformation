import argparse, os
import numpy
import scipy.misc
import math

from Queue import Queue
from threading import Thread

def report(list, name):
    print '%s Avg/Mean/Stddev : %.4f %.4f %.4f' % (name, numpy.average(list), numpy.median(list), math.sqrt(numpy.var(list)))

def main(args):
    input_imgA = [f for f in os.listdir(args.input_dirA) if os.path.isfile(os.path.join(args.input_dirA, f)) and
                  (f.endswith('.jpg') or f.endswith('.png'))]
    input_imgA_id = [os.path.splitext(f)[0] for f in input_imgA]
    input_imgB = [f for f in os.listdir(args.input_dirB) if os.path.isfile(os.path.join(args.input_dirB, f)) and
                  (f.endswith('.jpg') or f.endswith('.png')) and os.path.splitext(f)[0] in input_imgA_id]
    if args.max_images > 0:
        input_imgB = input_imgB[:args.max_images]
    input_imgB_id = [os.path.splitext(f)[0] for f in input_imgB]

    q = Queue()
    tot = []
    L0 = []
    L1 = []
    L2 = []
    Linf = []

    for i, f in enumerate(input_imgB):
        q.put((i, f, input_imgA[input_imgA_id.index(input_imgB_id[i])]))

    def worker():
        while True:
            i, fB, fA = q.get()
            imgA = scipy.misc.imread(os.path.join(args.input_dirA, fA)).astype(dtype=numpy.int)
            imgB = scipy.misc.imread(os.path.join(args.input_dirB, fB)).astype(dtype=numpy.int)
            delta = numpy.absolute(numpy.subtract(imgA, imgB))
            tot.append(delta.size)
            n = float(delta.size)
            L0.append(numpy.count_nonzero(delta) / n)
            L1.append(numpy.sum(delta) / n)
            L2.append(math.sqrt(numpy.sum(numpy.power(delta, 2)) / n))
            Linf.append(numpy.max(delta))
            if i % 100 == 0:
                print 'Processing image %d / %d' % (i, len(input_imgB))

            q.task_done()

    numw = min(q.qsize(), args.num_workers)
    for i in xrange(numw):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    q.join()

    report(tot, 'Size')
    if args.distance_norm & 1:
        report(L0, 'L0')
    if args.distance_norm & 2:
        report(L1, 'L1')
    if args.distance_norm & 4:
        report(L2, 'L2')
    if args.distance_norm & 8:
        report(Linf, 'Linf')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Input Settings
    parser.add_argument('--input_dirA', help='Directory containing all images of set A')
    parser.add_argument('--input_dirB', help='Directory containing all images of set B')

    #Output Settings
    parser.add_argument('--distance_norm', default=15,
                        help='An integer that describes which norms to measure, 1-L0 2-L1 4-L2 8-Linf. Default is 15(all)'
                        , type=int)

    #Option Settings
    parser.add_argument('--num_workers', default=5, help='Number of threads', type=int)
    parser.add_argument('--max_images', default=-1, help='Total number of images to process', type=int)
    args = parser.parse_args()
    main(args)
