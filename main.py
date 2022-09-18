import requests
import json
import os

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}


def get_data(head):
    page = 0
    result_list = []

    url = f'https://www.landingfolio.com/api/inspiration?page=&sortBy=most-popula'
    req = requests.get(url=url, headers=head)
    data = req.json()

    for item in data:
        if 'colors' in item:

            images = item.get('screenshots')[0].get('images')
            result_list.append(
                {
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'desktop_img': f"https://landingfoliocom.imgix.net/{images.get('desktop')}",
                    'mobile-img': f"https://landingfoliocom.imgix.net/{images.get('mobile')}"
                }
            )

    with open('data.json', 'a', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    get_img()


def get_img():

    with open('data.json', encoding='utf-8') as file:
        src = json.load(file)
        for item in src:
            title = item.get('title')
            desktop_url = item.get('desktop_img')
            mobile_url = item.get('mobile-img')

            try:
                req_for_desktop = requests.get(url=desktop_url)
                req_for_mobile = requests.get(url=mobile_url)

                if not os.path.exists(f'data/{title}'):
                    os.mkdir(f'data/{title}')

                with open(f'data/{title}/{title} desktop.png', 'bw') as img:
                    img.write(req_for_desktop.content)

                with open(f'data/{title}/{title} mobile.png', 'bw') as img:
                    img.write(req_for_mobile.content)

            except Exception as ex:
                continue


def main():
    # get_data(headers)
    get_img()


if __name__ == '__main__':
    main()
