import bchlib
import cv2 as cv
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants, signature_constants
import os
from tqdm import tqdm

class Stegastamp:
    def __init__(self, MODEL_PATH):
        self.width, self.height = 400, 400
        self.BCH_POLYNOMIAL = 137
        self.BCH_BITS = 5

        self.sess = tf.compat.v1.InteractiveSession(graph=tf.compat.v1.Graph())
        self.model = tf.compat.v1.saved_model.loader.load(self.sess, [tag_constants.SERVING], MODEL_PATH)

        input_secret_name = self.model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['secret'].name
        input_image_name = self.model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs['image'].name
        self.input_secret = tf.compat.v1.get_default_graph().get_tensor_by_name(input_secret_name)
        self.input_image = tf.compat.v1.get_default_graph().get_tensor_by_name(input_image_name)

        output_stegastamp_name = self.model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['stegastamp'].name
        output_residual_name = self.model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['residual'].name
        self.output_stegastamp = tf.compat.v1.get_default_graph().get_tensor_by_name(output_stegastamp_name)
        self.output_residual = tf.compat.v1.get_default_graph().get_tensor_by_name(output_residual_name)

        output_secret_name = self.model.signature_def[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY].outputs['decoded'].name
        self.output_secret = tf.compat.v1.get_default_graph().get_tensor_by_name(output_secret_name)

    def encode(self, secret, video_path):
        bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)

        # read
        cap = cv.VideoCapture(video_path)
        suffix = video_path.split('.')[-1]

        # write
        write_video_path = video_path + '.tmp.mp4'
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter(write_video_path, fourcc, 25.0, (400, 400))

        idx = 0
        frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        if frame_count < (len(secret) / 7):
            print("your video is too short,please change your video!")
            exit()

        pbar = tqdm(total=frame_count)
        while cap.isOpened():
            # if frame is read correctly ret is True
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # encode a single image.
            secret_idc, image = secret[idx:idx + 7], frame
            if len(secret_idc) > 7:
                print('Error: Can only encode 56bits (7 characters) with ECC')
                continue

            data = bytearray(secret_idc + ' ' * (7 - len(secret_idc)), 'utf-8')
            ecc = bch.encode(data)
            packet = data + ecc

            packet_binary = ''.join(format(x, '08b') for x in packet)
            secret_idc = [int(x) for x in packet_binary]
            secret_idc.extend([0, 0, 0, 0])

            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            H, W, _ = image.shape
            scale_percent = max(self.height / H, self.width / W)
            image = cv.resize(image, (int(W * scale_percent), int(H * scale_percent)))
            image = image[0:self.height, 0:self.width, :].astype(np.float32)
            image /= 255.  # 归一化

            feed_dict = {self.input_secret: [secret_idc],
                        self.input_image: [image]}

            hidden_img, residual = self.sess.run([self.output_stegastamp, self.output_residual], feed_dict=feed_dict)

            rescaled = (hidden_img[0] * 255).astype(np.uint8)
            im_hidden = cv.cvtColor(rescaled, cv.COLOR_RGB2BGR)

            idx += 7
            out.write(im_hidden)

            pbar.update(1)
        pbar.close()

        cap.release()
        cv.destroyAllWindows()
        out.release()

        # overwrite the old video
        new_video_path = video_path.replace(suffix, 'mp4')
        os.system('rm {}'.format(video_path))
        os.system('mv {} {}'.format(write_video_path, new_video_path))
        return new_video_path.split('/')[-1]

    def decode(self, video_path):
        cap = cv.VideoCapture(video_path)
        frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        print(frame_count)
        decode_secret = str()

        pbar = tqdm(total=frame_count)
        while cap.isOpened():
            pbar.update(1)
            
            # if frame is read correctly ret is True
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            H, W, _ = image.shape
            scale_percent = max(self.height / H, self.width / W)
            image = cv.resize(image, (int(W * scale_percent), int(H * scale_percent)))
            image = image[0:self.height, 0:self.width, :].astype(np.float32)
            image /= 255.  # 归一化

            feed_dict = {self.input_image:[image]}

            secret = self.sess.run([self.output_secret],feed_dict=feed_dict)[0][0]

            packet_binary = ''.join([str(int(bit)) for bit in secret[:96]])
            packet = bytes(int(packet_binary[i : i + 8], 2) for i in range(0, len(packet_binary), 8))
            packet = bytearray(packet)

            bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
            data, ecc = packet[:-bch.ecc_bytes], packet[-bch.ecc_bytes:]

            bitflips = bch.decode_inplace(data, ecc)
            frame_num = int(cap.get(cv.CAP_PROP_POS_FRAMES))
            if bitflips != -1:
                try:
                    code = data.decode("utf-8")
                    decode_secret += code
                    continue
                except:
                    continue
            print(frame_num, 'Failed to decode')
        
        pbar.close()
        print(decode_secret)

        return decode_secret