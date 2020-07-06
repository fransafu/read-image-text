import sys
import string
import numpy as np
import requests
import cv2
import keras.backend as K
from keras.callbacks import ModelCheckpoint, Callback
from keras.models import model_from_json, load_model

from .CRNN import ModelCRNN


class ModelReadImageText(ModelCRNN):
    configs = None
    model = None

    def __init__(self):
        self.config = {
            'img_width': 200,
            'img_height': 31,
            'img_nb_channels': 1,
            'characters': f'0123456789{string.ascii_lowercase}-',
            'label_len': 16,
            'model_path': 'model/pretrained_model.hdf5',
            'conv_filter_size': [64, 128, 256, 256, 512, 512, 512],
            'lstm_nb_units': [128, 128],
            'dropout_rate': 0.25
        }

        super().__init__(self.config)
        self.model = super().CRNN_STN()
        self.model.load_weights(self.config['model_path'])

    def evaluate(self, url):
        img = self.__load_image_from_url(url)
        if img.size == 0:
            return "Sorry. we can't download the image. Check the url and Try again"
        img = self.__preprocess_image(img)
        return self.__predict_text(img)

    def __load_image_from_file(self, img_path):
        return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    def __load_image_from_url(self, url):
        try:
            resp = requests.get(url, stream=True).raw
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            return cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        except requests.exceptions.RequestException:
            return np.array([])

    def __preprocess_image(self, img):
        if img.shape[1] / img.shape[0] < 6.4:
            img = self.__pad_image(img, (self.config['img_width'], self.config['img_height']), self.config['img_nb_channels'])
        else:
            img = self.__resize_image(img, (self.config['img_width'], self.config['img_height']))

        img = img.transpose([1, 0])
        img = np.flip(img, 1)
        img = img / 255.0
        img = img[:, :, np.newaxis]
        return img

    def __predict_text(self, img):
        y_pred = self.model.predict(img[np.newaxis, :, :, :])
        shape = y_pred[:, 2:, :].shape
        ctc_decode = K.ctc_decode(y_pred[:, 2:, :], input_length=np.ones(shape[0])*shape[1])[0][0]
        ctc_out = K.get_value(ctc_decode)[:, :self.config['label_len']]
        result_str = ''.join([self.config['characters'][c] for c in ctc_out[0]])
        result_str = result_str.replace('-', '')
        return result_str

    def __pad_image(self, img, img_size, nb_channels):
        # img_size : (width, height)
        # loaded_img_shape : (height, width)
        img_reshape = cv2.resize(img, (int(img_size[1] / img.shape[0] * img.shape[1]), img_size[1]))
        if nb_channels == 1:
            padding = np.zeros((img_size[1], img_size[0] - int(img_size[1] / img.shape[0] * img.shape[1])), dtype=np.int32)
        else:
            padding = np.zeros((img_size[1], img_size[0] - int(img_size[1] / img.shape[0] * img.shape[1]), nb_channels), dtype=np.int32)
        img = np.concatenate([img_reshape, padding], axis=1)
        return img

    def __resize_image(self, img, img_size):
        img = cv2.resize(img, img_size, interpolation=cv2.INTER_CUBIC)
        img = np.asarray(img)
        return img
