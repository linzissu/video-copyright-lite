import argparse
from ast import arg
import enum
import cv2 as cv
import numpy as np
from extractor import Extractor
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, default='./data/img1.jpeg')
args = parser.parse_args()

pts = []
name = 'image'
img = cv.imread(args.i)
img_cp = img.copy()

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pts.append([x,y])
        cv.circle(img_cp, (x, y), 5, (0, 0, 255), thickness=-1)
        cv.circle(img_cp, (x, y), 6, (0, 255, 0), thickness=2)
        cv.putText(img_cp, '[{},{}]'.format(x,y), (x, y), cv.FONT_HERSHEY_PLAIN,
                    1.0, (255, 0, 0), thickness=1)
    cv.imshow(name, img_cp)


if __name__ == "__main__":
    extractor = Extractor(640, 480) 

    # click to gain the points
    cv.namedWindow(name)
    cv.setMouseCallback(name, on_EVENT_LBUTTONDOWN)
    cv.imshow(name, img)
    cv.waitKey(0)
    pts = extractor.order_points(np.array(pts))
    print('ordered points: \n', pts)


    # draw lines on the image
    extractor.drawPtsLine(img_cp, pts=pts)
    extractor.cv_show('Draw Line', img_cp)
    cv.imwrite('./data/demo_pts.png', img_cp)


    # ! warp image  [*]
    H = extractor.findHomography(pts)
    warp_img = extractor.warpImage(img, H)
    extractor.cv_show('warped image', warp_img)
    cv.imwrite('./data/demo_warp.png', warp_img)

    # ! extractor to 4 part   [*]
    sub_ims = extractor.extract(warp_img)
    for i, sub in enumerate(sub_ims):
        extractor.cv_show('subsequence of image', sub)
        cv.imwrite('./data/demo_sub{}.png'.format(i), sub)

    # ! merge 4 part to 1     [*]
    rec_img = extractor.merge(sub_ims)
    extractor.cv_show('recovered image', rec_img)
    cv.imwrite('./data/demo_merge.png', rec_img)
