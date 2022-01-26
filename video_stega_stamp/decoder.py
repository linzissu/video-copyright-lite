import bchlib
import numpy as np
import tensorflow as tf
import argparse
import cv2 as cv
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import signature_constants
BCH_POLYNOMIAL = 137
BCH_BITS = 5


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,default='saved_models/stegastamp_pretrained')
parser.add_argument('--video', type=str, default='./out/out.avi')
args = parser.parse_args()


sess = tf.compat.v1.InteractiveSession(graph=tf.compat.v1.Graph())

model = tf.compat.v1.saved_model.loader.load(sess, [tag_constants.SERVING], args.model)

input_image_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['image'].name
input_image = tf.compat.v1.get_default_graph().get_tensor_by_name(input_image_name)

output_secret_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['decoded'].name
output_secret = tf.compat.v1.get_default_graph().get_tensor_by_name(output_secret_name)

def main():
    cap = cv.VideoCapture(args.video)
    decode_secret = str()
    while cap.isOpened():
        # if frame is read correctly ret is True
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        width = 400
        height = 400
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        H, W, _ = image.shape
        scale_percent = max(height / H, width / W)
        image = cv.resize(image, (int(W * scale_percent), int(H * scale_percent)))
        image = image[0:height, 0:width, :].astype(np.float32)
        image /= 255.  # 归一化

        feed_dict = {input_image:[image]}

        secret = sess.run([output_secret],feed_dict=feed_dict)[0][0]

        packet_binary = "".join([str(int(bit)) for bit in secret[:96]])
        packet = bytes(int(packet_binary[i : i + 8], 2) for i in range(0, len(packet_binary), 8))
        packet = bytearray(packet)

        bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
        data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

        bitflips = bch.decode_inplace(data, ecc)
        frame_num = int(cap.get(cv.CAP_PROP_POS_FRAMES))
        if bitflips != -1:
            try:
                code = data.decode("utf-8")
                print(frame_num, code)
                decode_secret += code
                continue
            except:
                continue
        print(frame_num, 'Failed to decode')

    print(decode_secret)

if __name__ == "__main__":
    main()