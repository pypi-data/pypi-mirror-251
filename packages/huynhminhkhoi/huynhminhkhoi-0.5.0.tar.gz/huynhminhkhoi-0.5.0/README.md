[![PyPi Package Version](https://img.shields.io/pypi/v/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/huynhminhkhoi)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/huynhminhkhoi)
[![Documentation Status](https://readthedocs.org/projects/pytba/badge/?version=latest)](https://pytba.readthedocs.io/en/latest/?badge=latest)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyTelegramBotAPI.svg)](https://pypi.org/project/huynhminhkhoi/)
[![PyPi status](https://img.shields.io/pypi/status/pytelegrambotapi.svg?style=flat-square)](https://pypi.python.org/pypi/huynhminhkhoi)

# <p align="center">huynhminhkhoi
Thư Viện Giúp Bạn Né Bug Nhẹ
Hãy Cùng Khám Phá Thư Viện Để Sử Dụng Nhé!
## Nội Dung

* [Cài Đặt Thư Viện](#c%C3%A0i-%C4%91%E1%BA%B7t-th%C6%B0-vi%E1%BB%87n)
* [Các Hàm Cơ Bản](#c%C3%A1c-h%C3%A0m-c%C6%A1-b%E1%BA%A3n)
  * [Get Key](#get-key)
  * [Check Key](#check-key)
* [Code Demo](#code-demo)
* [Các Hàm Cho Admin](#c%C3%A1c-h%C3%A0m-d%C3%A0nh-cho-admin)
  * [Add Key](#add-key)
  * [Remove Key](#remove-key)
* [Contact](#contact)
## Cài Đặt Thư Viện
**Thư viện này đã được thử nghiệm với Python 3.11. Cách cài đặt thư viện:**
```
$ pip install huynhminhkhoi
```

## Các Hàm Cơ Bản
**Lớp huynhminhkhoi (được định nghĩa trong \__init__.py) gói gọn 2 lệnh gọi API. Nó cung cấp các chức năng như `get_key` và `check_key`**

### Get Key

**Tạo 1 Tệp Có Tên Bất Kì Ví Dụ `khoidz.py`. Sau đó, mở tệp và tham khảo đoạn code dưới đây:**

***Kết nối client:***

```python
import huynhminhkhoi
import requests
ip_get = requests.get('http://ip-api.com/json/').json()['query']
list_token_link = ["your_token", "https://huynhminhkhoidev.x10.mx/key.html?keyhomnay="]
client = huynhminhkhoi.Api.client("name_key", list_obj = list_token_link)
```

***Get link key với dữ liệu dict:***
```python
get_key = client.get_key(ip = ip_get)
print(get_key)
```

***Note: `name_key` sẽ là tên key của bạn, 
`list_token_link` sẽ là danh sách lần lượt chứa token link1s và web chứa key của bạn.***

### Check Key
**Để kiểm tra key đúng hay sai. Bạn có thể sử dụng đoạn code mẫu dưới đây:**

***Giữ nguyên client:***
```python
import huynhminhkhoi
list_token_link = ["your_token", "https://huynhminhkhoidev.x10.mx/key.html?keyhomnay="]
client = huynhminhkhoi.Api.client("name_key", list_obj = list_token_link)
```

***Check key với dữ liệu dict:***
```python
ip_get = requests.get('http://ip-api.com/json/').json()['query']
check = client.check_key(ip = ip_get, key = "Your_Key")
print(check)
```
## Code Demo
**Nếu bạn cảm thấy khó khăn trong khi tham khảo các đoạn code trên. Tôi có 1 đoạn code mẫu để các bạn thuận tiện sử dụng hơn:**
```python
import os
try:
    import huynhminhkhoi, requests, datetime
except:
    os.system('pip install huynhminhkhoi')
    os.system('pip install requests')

ip_ = requests.get('http://ip-api.com/json/').json()
ip_get = ip_['query']
list_ = ['Your_Token', 'https://huynhminhkhoidev.x10.mx/key.html?keyhomnay=']
client = huynhminhkhoi.Api.client(name = 'KhoiHuynh1109', list_obj = list_)
while True:
    if not os.path.exists('key.txt'):
        print(f'Ip Của Bạn Là: {ip_get}')
        get_key = client.get_key(ip = ip_get)
        if get_key['status'] == 'error':
            quit(get_key['message'])
        print("Hello My World. I love you")
        print(f"Link Key Ngày Của Bạn Là: {get_key['url']}")
        password = input("Nhập Key Hôm Nay Để Sử Dụng: ")
        check_key = client.check_key(ip = ip_get, key = password)
        if check_key['status'] == 'success' and check_key['types'] == '1day':
            data = {
            'key': password,
            'types': '1day',
            'time_use': datetime.datetime.now(),
            'date': datetime.timedelta(days = 1)
            }
            open('key.txt', 'w').write(str(data))
        else:
            open('key.txt', 'w').write(str(check_key))
    with open('key.txt', 'r') as f:
        try:
            js = eval(f.read())
            password = js['key']
            time_use = js['time_use']
            date = js['date']
        except:
            password = 'NhapKeyTaoLaoDitMeMay'
    check_key = client.check_key(ip = ip_get, key = password)
    if check_key['status'] == 'success':
        if js['types'] == '1day':
            now = datetime.datetime.now()
            if now - time_use <= date:
                hsd = str(date - (now - time_use)).split('.')[0]
                print(f"Key Success | Loại Key: Free 1 Ngày | Sử Dụng Lúc: {time_use.strftime('%d/%m/%Y - %H:%M:%S')} | Hạn Sử Dụng: {hsd}")
                break
            else:
                print("Key Hết Hạn!")
                os.remove('key.txt')
                continue
        else:
            key_types = js['types'].replace('3day', '3 Ngày').replace('7day', '7 Ngày').replace('1month', '1 Tháng')
            print(f"Key Success | Loại Key: Key {key_types} | Sử Dụng Lúc: {time_use} | Hạn Sử Dụng: {check_key['date']}")
            break
    else:
        print("Sai Key Rồi Em")
        os.remove('key.txt')
        continue

#Tiến Trình Sẽ Chạy Bên Dưới
```
**Lưu ý rằng nếu bạn code tool gộp dạng exec(). Hãy đặt check key ở sever đảm bảo né bug 1 chút**

**Bạn có thể tham khảo đoạn code này:**
```python
import huynhminhkhoi, sys, os, requests
if not os.path.exists('key.txt'):
    print("Bug Cái Gì Vậy Chú")
    os.remove(sys.argv[0])
    quit()
try:
    read = eval(open('key.txt', 'r').read())
except:
    print("Bug Cái Gì Vậy Chú")
    os.remove(sys.argv[0])
    quit()
ip_ = requests.get('http://ip-api.com/json/').json()
ip_get = ip_['query']
client = huynhminhkhoi.Api.client(name = 'KhoiHuynh1109', list_obj = [])
check = client.check_key(ip = ip_get, key = read['key'])
if check['status'] == 'error':
    print("Bug Cái Gì Vậy Chú")
    os.remove(sys.argv[0])
    quit()
# Nếu Đúng Key Sẽ Chạy Tiến Trình
```
***Với việc sử dụng `os.remove` ở trên sẽ không ảnh hưởng đến các file khác mà chỉ xoá chính file kẻ bug run lên ví dụ `python khoidz.py` thì khi đó nó sẽ xoá `khoidz.py`***

***Ở `list_obj` phía trên không hề có đối tượng `token` và `long_url`. Bởi vì chỉ gọi hàm `check_key()` nên nó sẽ không xuất hiện lỗi.***

***Lưu ý rằng đây là code đặt ở các file sever giảm thiểu việc crack bằng cách bug ra sever.***

## Các Hàm Dành Cho Admin
**Hàm dành cho admin là gì? Nó là các hàm giúp admin add các key vip như 3 ngày, 7 ngày hay 1 tháng**

***Để sử dụng được hàm này ta cần key admin do Huỳnh Minh Khôi cấp cho. Bạn có thể liên hệ [Facebook](https://www.facebook.com/valerie.alvares) của Khôi để lấy key admin***

### Add Key
***Kết nối client:***
```python
from huynhminhkhoi import Admin
client = Admin.client(admin = "Key_Admin")
```

***Hàm add_key:***
```python
add = client.add_key(key = "Name_Key")
```

***Với `Key_Admin` là key admin được Huỳnh Minh Khôi đưa cho bạn và `Name_Key` là tên key mà bạn muốn***

### Remove Key

**Để xoá key người dùng hay bạn add nhầm key, bạn có thể sử dụng hàm `remove` để xoá nó.**

***Giữ nguyên client:***
```python
from huynhminhkhoi import Admin
client = Admin.client(admin = "Key_Admin")
```

***Hàm Remove:***
```python
rmv = client.remove(key = "Name_Key")
```

## Contact
**Liên hệ [Facebook](https://www.facebook.com/valerie.alvares) để được support hoặc báo lỗi cho tôi fix nhé. Cảm ơn!**
