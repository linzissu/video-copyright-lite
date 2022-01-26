import bchlib
import argparse
import cv2 as cv
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants, signature_constants

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='saved_models/stegastamp_pretrained')
parser.add_argument('--secret', type=str, default= 'this video belongs to lhm, anyone can not copy it,if result any problem.you will be charged and go to prison!!!')
parser.add_argument('--video', type=str, default='./video/car.mp4')
parser.add_argument('--save_dir', type=str, default='./out/')
arg = parser.parse_args()
cap = cv.VideoCapture(arg.video)
sess = tf.compat.v1.InteractiveSession(graph=tf.compat.v1.Graph())
model = tf.compat.v1.saved_model.loader.load(sess, [tag_constants.SERVING], arg.model)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(arg.save_dir + 'out.avi', fourcc, 25.0, (400, 400))
BCH_POLYNOMIAL = 137
BCH_BITS = 5


def encoder_image(sess, model, image, secret):
    input_secret_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['secret'].name
    input_image_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['image'].name
    input_secret = tf.compat.v1.get_default_graph().get_tensor_by_name(input_secret_name)
    input_image = tf.compat.v1.get_default_graph().get_tensor_by_name(input_image_name)

    output_stegastamp_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs[
        'stegastamp'].name
    output_residual_name = model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs[
        'residual'].name
    output_stegastamp = tf.compat.v1.get_default_graph().get_tensor_by_name(output_stegastamp_name)
    output_residual = tf.compat.v1.get_default_graph().get_tensor_by_name(output_residual_name)

    width = 400
    height = 400

    bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

    if len(secret) > 7:
        print('Error: Can only encode 56bits (7 characters) with ECC')
        return

    data = bytearray(secret + ' ' * (7 - len(secret)), 'utf-8')
    ecc = bch.encode(data)
    packet = data + ecc

    packet_binary = ''.join(format(x, '08b') for x in packet)
    secret = [int(x) for x in packet_binary]
    secret.extend([0, 0, 0, 0])
    #
    # image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    # image = np.array(ImageOps.fit(image, size), dtype=np.float32)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    H, W, _ = image.shape
    scale_percent = max(height / H, width / W)
    image = cv.resize(image, (int(W * scale_percent), int(H * scale_percent)))
    image = image[0:height, 0:width, :].astype(np.float32)
    image /= 255.  # 归一化

    feed_dict = {input_secret: [secret],
                 input_image: [image]}

    hidden_img, residual = sess.run([output_stegastamp, output_residual], feed_dict=feed_dict)

    rescaled = (hidden_img[0] * 255).astype(np.uint8)
    raw_img = (image * 255).astype(np.uint8)
    residual = residual[0] + .5

    residual = (residual * 255).astype(np.uint8)

    # convert the output (RGB) to BGR.
    im_hidden, im_residual = cv.cvtColor(rescaled, cv.COLOR_RGB2BGR), cv.cvtColor(residual, cv.COLOR_RGB2BGR)
    return im_hidden, im_residual


def main():
    secret = arg.secret
    idx = 0
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    if frame_count < (len(secret) / 7):
        print("your video is too short,please change your video!")
        exit()

    while cap.isOpened():
        # if frame is read correctly ret is True
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        im_hidden, im_residual = encoder_image(sess, model, frame, secret[idx:idx + 7])
        idx += 7
        out.write(im_hidden)
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('im_hidden', im_hidden)

        # playing video from file
        if cv.waitKey(10) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    out.release()


if __name__ == "__main__":
    main()
