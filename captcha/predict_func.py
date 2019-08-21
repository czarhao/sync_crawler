import urllib
import requests
import urllib.request
import numpy as np
from PIL import Image
from sklearn.externals import joblib


def verify(url, model, save=False):
    """
    :param url: 验证码地址
    :param model: 处理该验证码的模型
    :param save: 是否保存临时文件到cache
    :return:
    """
    session = requests.session()
    if save:
        pic_file = 'captcha/cache/captcha.png'
        urllib.request.urlretrieve(url, pic_file)
        image = Image.open(pic_file).convert("L")
    else:
        r = session.get(url)
        print(r)
        with open('captcha/cache/captcha.png', 'wb') as f:
            f.write(r.content)
        image = Image.open('captcha/cache/captcha.png')
    x_size, y_size = image.size
    y_size -= 5

    # y from 1 to y_size-5
    # x from 4 to x_size-18
    piece = (x_size-24) / 8
    centers = [4+piece*(2*i+1) for i in range(4)]
    data = np.empty((4, 21 * 16), dtype="float32")
    for i, center in enumerate(centers):
        single_pic = image.crop((center-(piece+2), 1, center+(piece+2), y_size))
        data[i, :] = np.asarray(single_pic, dtype="float32").flatten() / 255.0
        if save:
            single_pic.save('captcha/cache/captcha-%s.png' % i)
    clf = joblib.load(model)
    answers = clf.predict(data)
    answers = map(chr, map(lambda x: x + 48 if x <= 9 else x + 87 if x <= 23 else x + 88, map(int, answers)))
    return answers

