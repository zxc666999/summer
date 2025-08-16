





import requests




headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.musinsa.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.musinsa.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}


def get_id():
    params = {
        'gf': 'A',
        'caller': 'CATEGORY',
        'category': '104',
    }

    response = requests.get(
        'https://api.musinsa.com/api2/dp/v1/plp/filter/categories',
        params=params,
        headers=headers,
    )
    # print(response.json())
    data_list = response.json().get('data').get('list')[0].get('categoryList')[0].get('categoryList')
    # print(data_list)
    categoryCode_list = []
    for node in data_list:
        categoryCode_list.append(node.get('categoryCode'))
    print(categoryCode_list)
    return categoryCode_list
get_id()

