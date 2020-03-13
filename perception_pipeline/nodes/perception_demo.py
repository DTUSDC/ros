#!/usr/bin/env python

# Perception pipeline for DTUSDC

from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
from collections import Counter
import rospy
import sys
import numpy as np
from sklearn.cluster import DBSCAN

import roslib
roslib.load_manifest('perception_pipeline')


class image_converter:
    def __init__(self):
        self.image_pub = rospy.Publisher(
            "camera/rgb/image_raw", Image, queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(
            "/usb_cam/image_raw", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        frame = cv_image
        print(cv_image.shape)
        og = cv2.resize(frame, (640, 480))
        # cv2.imshow("OG", og)
        of = ROI(perspective_transform(cal_undistort2(og)))
        og = processImageOld(og)
        og = cal_undistort2(og)
        # cv2.imshow("UnDisort", og)
        og = perspective_transform(og)
        # cv2.imshow("PerpTrans", og)
        og = ROI(og)

        indices = np.where(og > [80])
        coordinates = zip(indices[0], indices[1])
        coords = list(coordinates)
        coords = np.reshape(coords, [-1, 2])

        # change from here 0

        dbscan = DBSCAN(eps=10, min_samples=20,
                        algorithm='auto', metric='euclidean')
        dbscan.fit(coords)
        labels = list(dbscan.labels_)

        cl = zip(labels, coords)
        cl = list(cl)

        largest_cl = largest_cluster(cl)

        left_coords, right_coords = left_right_cluster(cl, largest_cl)
        left_coords, right_coords = correct_order(
            left_coords, right_coords)
        left_coords, right_coords = remove_redundance(
            left_coords, right_coords)
        left_coords = [(j, i) for i, j in left_coords]
        right_coords = [(j, i) for i, j in right_coords]
        cv2.polylines(of, np.int32([left_coords]), isClosed=False, color=(
            150, 150, 255), thickness=4)
        cv2.polylines(of, np.int32([right_coords]), isClosed=False, color=(
            255, 150, 150), thickness=4)
        len_left, len_right = len(left_coords), len(right_coords)

        # print(len_left, len_right)

        """
        cv2.polylines(of,[ptsLine3],True,(255,255,0), 1)
        cv2.polylines(of,[ptsLine4],True,(255,0,0), 1)
        cv2.polylines(of,[ptsLine6],True,(0,255,0), 1)
        cv2.polylines(of,[ptsLine5],True,(255,0,0), 1)
        cv2.polylines(of,[ptsLine7],True,(255,0,255), 1)
        cv2.polylines(of,[ptsLine10],True,(255,0,0), 1)
        cv2.polylines(of,[ptsLine11],True,(255,0,255), 1)
        cv2.polylines(of,[ptsLine16],True,(0,0,0), 1)
        cv2.polylines(of,[ptsLine17],True,(255,255,255), 1)
        """

        # im = draw(left_coords ,of , 0)
        # im = draw(right_coords ,of , 0)
        cv2.imshow("OUTPUT", of)
        # print(of.shape)
        # out.write(of)

        # Press q to quit
        cv2.waitKey(25)

        """
        cv2.destroyAllWindows()

        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)
        try:
            self.image_pub.publish(
                self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)
        """


def color_transfer(target, clip=True, preserve_paper=True):

    source = cv2.imread('green4.jpeg')
    source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    (l, a, b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    if preserve_paper:

        l = (lStdTar / lStdSrc) * l
        a = (aStdTar / aStdSrc) * a
        b = (bStdTar / bStdSrc) * b
    else:

        l = (lStdSrc / lStdTar) * l
        a = (aStdSrc / aStdTar) * a
        b = (bStdSrc / bStdTar) * b

    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

# clip/scale the pixel intensities to [0, 255] if they fall
# outside this range
    l = _scale_array(l, clip=clip)
    a = _scale_array(a, clip=clip)
    b = _scale_array(b, clip=clip)

# merge the channels together and convert back to the RGB color
# space, being sure to utilize the 8-bit unsigned integer data
# type
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

# return the color transferred image
    return transfer


def image_stats(image):

    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)


def _min_max_scale(arr, new_range=(0, 255)):

    # get array's current min and max
    mn = arr.min()
    mx = arr.max()

    # check if scaling needs to be done to be in new_range
    if mn < new_range[0] or mx > new_range[1]:
        # perform min-max scaling

        scaled = (new_range[1] - new_range[0]) * \
            (arr - mn) / (mx - mn) + new_range[0]
    else:
        # return array if already in range
        scaled = arr

    return scaled


def _scale_array(arr, clip=True):

    if clip:
        scaled = np.clip(arr, 0, 255)
    else:
        scale_range = (max([arr.min(), 0]), min([arr.max(), 255]))
        scaled = _min_max_scale(arr, new_range=scale_range)

    return scaled


def processImage5(im1):
    # def processImage5(im1 , im2 ) :
    # im2 = im1.copy()
    im1 = color_transfer(im1)

    im1 = np.array(255*(im1/255)**1.3, dtype='uint8')

    # im2 = np.array(255*(im2/255)**1.3,dtype='uint8')

    im1 = cv2.GaussianBlur(im1, (7, 7), 0)
    # im2 = cv2.GaussianBlur(im2, (7 , 7) , 0 )
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    v1 = im1[:, :, 2]
    v1 = cv2.bitwise_not(v1)
    # v2 = cv2.bitwise_not(v2)

    kernel = np.ones((3, 3), np.uint8)
    v1 = cv2.erode(v1, kernel, iterations=2)
    # v2 = cv2.erode(v2, kernel , iterations=2)

    v1 = cv2.GaussianBlur(v1, (5, 5), 0)
    # v2 = cv2.GaussianBlur(v2, (5 , 5) , 0)

    # v1 = cv2.adaptiveThreshold(v1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 97, 19)
    v1 = cv2.adaptiveThreshold(
        v1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 157, 19)
    # 157

    v1 = cv2.bitwise_not(v1)
    return v1


def processImageOld(im1):
    im1 = np.array(255*(im1/255)**1.3, dtype='uint8')
    im1 = cv2.GaussianBlur(im1, (7, 7), 0)
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
    v1 = im1[:, :, 2]
    v1 = cv2.bitwise_not(v1)
    kernel = np.ones((3, 3), np.uint8)
    v1 = cv2.erode(v1, kernel, iterations=2)
    v1 = cv2.GaussianBlur(v1, (11, 11), 0)
    v1 = cv2.adaptiveThreshold(v1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 157, 19)
    v1 = cv2.bitwise_not(v1)
    kernel = np.ones((3, 3), np.uint8)
    v1 = cv2.erode(v1, kernel, iterations=2)
    return v1


def perspective_transform(img):
    pix = 250
    src = np.array([[0, 0], [640, 0], [640, 480], [0, 480]], dtype="float32")
    dst = np.array([[0, 0], [640 - 1, 0], [640 - pix, 480 - 1],
                    [pix, 480 - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(src, dst)
    img_size = (img.shape[1], img.shape[0])
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    ptsLine1 = np.array([(195, 255), (195, 0)], np.int32)
    ptsLine2 = np.array([(60, 255), (60, 0)], np.int32)
    return warped


def cal_undistort2(img):
    dist = np.array([-0.361749, 0.104000, -0.003157, 0.000011, 0.000000])
    mtx = np.array([[453.097111, 0.000000, 320.636246], [
        0.000000, 458.793546, 242.712218], [0.000000, 0.000000, 1.000000]])
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv2.initUndistortRectifyMap(
        mtx, dist, None, newcameramtx, (w, h), 5)
    undst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    return undst


def ROI(img):
    src = np.array([[167, 250], [473, 250], [473, 480],
                    [167, 480]], dtype="float32")
    dst = np.array([[0, 0], [640, 0], [640, 480], [0, 480]], dtype="float32")
    M = cv2.getPerspectiveTransform(src, dst)
    img_size = (img.shape[1], img.shape[0])
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    return warped


def draw(coords, ima, col):
    # im = np.zeros((480,640))
    for i in range(len(coords)):
        ima[coords[i][0]][coords[i][1]] = col
    return ima


def draw_cluster(coords, n, ime):
    # im = np.zeros((480,640))
    one = n[0]
    two = n[1]

    for i in range(len(coords)):
        if coords[i][0] == one:
            ime[coords[i][1][0]][coords[i][1][1]] = 0
    for j in range(len(coords)):
        if coords[j][0] == two:
            ime[coords[j][1][0]][coords[j][1][1]] = 255
    return ime


def largest_cluster(cl):
    ls = []
    for i in range(len(cl)):
        ls.append(cl[i][0])
    count = Counter(ls)
    mc = count.most_common(2)
    mg = []
    for j in range(len(mc)):
        mg.append(mc[j][0])
    return mg


def left_right_cluster(coords, n):
    one = n[0]
    two = n[1]
    left = []
    right = []
    for i in range(len(coords)):
        if coords[i][0] == one:
            left.append(coords[i][1])
    for j in range(len(coords)):
        if coords[j][0] == two:
            right.append(coords[j][1])
    return left, right


def remove_redundance(l_cl, r_cl):
    l = []
    last_l = len(l_cl)
    for i in range(last_l-1):
        if l_cl[i][0] != l_cl[i+1][0]:
            l.append(l_cl[i])
    l.append(l_cl[last_l-1])

    r = []
    last_r = len(r_cl)
    for i in range(last_r-1, 0, -1):
        if r_cl[i][0] != r_cl[i-1][0]:
            r.append(r_cl[i])
    r.append(r_cl[0])
    r.reverse()
    return l, r


def correct_order(l, r):
    if l[-1][1] < r[-1][1]:
        return l, r
    else:
        return r, l


##################################################################################
'''x = 160
y = 320
# a=222
# b=419
a=55
b=470
c=252
ptsLine3 = np.array([(0, x) , (640, x)] , np.int32)
ptsLine4 = np.array([(0, y) , (640, y)] , np.int32)
ptsLine5 = np.array([(a, 0) , (a, 640)] , np.int32)
ptsLine6 = np.array([(b, 0) , (b, 640)] , np.int32)
ptsLine7 = np.array([(c, 0) , (c, 640)] , np.int32)

e = 293
t = 208
ptsLine10 = np.array([(0, e) , (640, e)] , np.int32)
ptsLine11 = np.array([(0, t) , (640, t)] , np.int32)

w = 350
q = 438

ptsLine16 = np.array([(w, 0) , (w, 640)] , np.int32)
ptsLine17 = np.array([(q, 0) , (q, 640)] , np.int32)
'''
####################################################
# bottom
# reg1 - 455,336 verticle
# reg1 - 379,476 H

# reg2 - 208,298 v
# reg2 - 350,438 h
###################################################################################


def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
