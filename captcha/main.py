

from captcha.predict_func import verify
the_model = 'captcha/model/SVC_Model_zf.pkl'


def get_code(url):
    captcha_list = list(verify(url, the_model))
    return ''.join(captcha_list)


if __name__ == '__main__':
    the_url = 'http://210.30.208.126/(wjuuiaaeik1arortiyixberg)/CheckCode.aspx'
    captcha_list = list(verify(the_url, the_model))
    print(''.join(captcha_list))
