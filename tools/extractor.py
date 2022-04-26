import numpy as np
import cv2 as cv

class Extractor:
    ''' global consts '''
    def __init__(self, width = 800, height = 800):
        self.H, self.W = height, width

    ''' show image '''
    def cv_show(self,name:str,img:np.ndarray)->None:
        cv.imshow(name,img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    ''' order the points '''
    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype=np.float32)
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # np.vstack((rect, np.array()))
        return rect

    ''' draw line on the image '''
    def drawPtsLine(self, img, pts, color = (100,100,250)):
        # pts.append(pts[0:])
        cv.polylines(img, np.int32([pts]), thickness=4, color=color, isClosed=True)        

    '''     find Homography matrix '''
    def findHomography(self,pts_src):
        pts_dst = np.array([[0,0],[self.W,0],[self.W,self.H],[0,self.H]])
        H, _ = cv.findHomography(pts_src, pts_dst)
        return H

    ''' warp '''
    def warpImage(self, img, H):
        warped_im = cv.warpPerspective(img, H, (self.W, self.H))
        return warped_im

    ''' extract sub images '''
    def extract(self, img):
        res = []
        img = cv.resize(img, (self.W, self.H))
        H, W, _ = img.shape
        for i in range(0, H, int(H/2)):
            for j in range(0, W, int(W/2)):
                res.append(img[i:int(i+H/2),j:int(j+W/2)].copy())
        return res

    ''' merge '''
    def merge(self, sub_ims):
        res = np.vstack((
            np.hstack((sub_ims[0], sub_ims[1])),
            np.hstack((sub_ims[2], sub_ims[3]))
        ))
        return res
