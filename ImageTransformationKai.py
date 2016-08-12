import argparse, os
import numpy as np
import scipy.misc
import skimage
from PIL import Image, ImageDraw

from Queue import Queue
from threading import Thread

def main(args):
    input_img = [f for f in os.listdir(args.image_dir) if os.path.isfile(os.path.join(args.image_dir, f)) and (f.endswith('.jpg') or f.endswith('.png'))]

    if not os.path.exists(args.output_image_dir):
        os.makedirs(args.output_image_dir)

    if args.max_images > 0:
        input_img = input_img[:args.max_images]

    q = Queue()

    for i, f in enumerate(input_img):
        q.put((i, f))

    def worker():
        alpha = args.const_alpha
        beta = args.const_beta
        while True:
            i, f = q.get()
            fname = os.path.splitext(f)[0]
            if args.transformation < 3:
                img = Image.open(os.path.join(args.image_dir, f))
                out_file = os.path.join(args.output_image_dir, fname + '.' + args.output_type)
                if args.transformation == 1:
                    ow, oh = img.size
                    if alpha >= 0:
                        xs = 0
                        xe = oh - alpha
                    else:
                        xs = -alpha
                        xe = oh
                    if beta >= 0:
                        ys = 0
                        ye = ow - beta
                    else:
                        ys = -beta
                        ye = ow
                    box = (ys, xs, ye, xe)
                    img2 = img.crop(box)
                    img = img.point(lambda i : 0)
                    img.paste(img2, (ys + beta, xs + alpha, ye + beta, xe + alpha))
                elif args.transformation == 2:
                    img = img.rotate(float(alpha), expand=True)
                img.save(out_file)
            else:
                img = scipy.misc.imread(os.path.join(args.image_dir, f)).astype(dtype=np.float32) / 255 * 2 - 1
                times = beta
                if args.transformation == 3:
                    for i in range(1, times + 1):
                        out_file = os.path.join(args.output_image_dir, fname + '_' + str(i) + '.' + args.output_type)
                        img2 = (skimage.util.random_noise(img, mode='gaussian', clip=True, var=(float(alpha) / 255) ** 2) + 1) / 2 * 255
                        scipy.misc.imsave(out_file, img2.astype(dtype=np.int))
                elif args.transformation == 4:
                    for i in range(1, times + 1):
                        out_file = os.path.join(args.output_image_dir, fname + '_' + str(i) + '.' + args.output_type)
                        noise = np.random.uniform(-float(alpha) / 255, float(alpha)/255, size=img.shape)
                        img2 = ((img + noise) + 1) / 2 * 255
                        scipy.misc.imsave(out_file, img2.astype(dtype=np.int))
            if i % 100 == 0:
                print 'Writing image %d / %d' % (i, len(input_img))

            q.task_done()

    numw = min(q.qsize(), args.num_workers)
    for i in xrange(numw):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    q.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Input Settings
    parser.add_argument('--image_dir', help='Directory containing all images')

    parser.add_argument('--transformation', default=0, help='0 = none, 1 = shift, 2 = rotation, 3 = random Gaussian, 4 = random Uniform', type=int)
    parser.add_argument('--const_alpha', default=0, help='Degree for rotation, dx for shift, std dev for gaussian, +- range for random uniform', type=int)
    parser.add_argument('--const_beta', default=0, help='dy for shift, number of trails for random', type=int)

    #Output Settings
    parser.add_argument('--output_image_dir', help='Directory to output transformed images')
    parser.add_argument('--output_type', default='jpg', help='File type to output')

    #Option Settings
    parser.add_argument('--num_workers', default=10, help='Number of threads', type=int)
    parser.add_argument('--max_images', default=-1, help='Total number of images to process', type=int)
    args = parser.parse_args()
    main(args)