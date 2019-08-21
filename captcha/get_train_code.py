import requests


def get_codeimg(captcha_url):
    i = 51
    for i in range(200):
        i = int(i)
        i += 1
        session = requests.session()
        r = session.get(captcha_url)
        img_name = 'full_image/' + 'code_' + str(i) + '.jpg'
        with open(img_name, 'wb') as f:
            f.write(r.content)
        print(i)
