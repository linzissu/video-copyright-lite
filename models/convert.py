import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,default='saved_models/stegastamp_pretrained')
parser.add_argument('--output', type=str, default='./model.tflite')
args = parser.parse_args()

if '__name__' == '__main__':
    # Convert the model.
    converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(args.input)
    tflite_model = converter.convert()

    # Save the model.
    with open(parser.output, 'wb') as f:
        tf.write(tflite_model)

    print('Convert sucessful!')
