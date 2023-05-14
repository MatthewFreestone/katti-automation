import requests


def main():
    username = 'matthew-freestone'
    token = "7412e41f4f38ccfcf61c933ba882c95893943def3dc98b2ac4d76e8f0e7d2d3a"
    url = "https://open.kattis.com"
    creds = {
        "user": username,
        "token": token,
        "script": "true"
    }
    login_response = requests.post(url + "/login", data=creds)

    response = requests.get(url + "/submissions/11015735",
                            cookies=login_response.cookies)
    with open("./submission_get_response.txt", 'w') as f:
        f.write(response.text)
    print(response.status_code)


if __name__ == '__main__':
    main()
