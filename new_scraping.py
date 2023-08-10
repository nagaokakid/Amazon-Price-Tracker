from bs4 import BeautifulSoup
import requests

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxies = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

URL = "https://www.amazon.ca/Zojirushi-NP-NWC10XB-Pressure-Induction-Stainless/dp/B088FZXZHY?ref_=Oct_d_omg_d_6647661011_2&pd_rd_w=L9P1p&content-id=amzn1.sym.08f83d5a-3cc9-44c6-8510-c525edee3a31&pf_rd_p=08f83d5a-3cc9-44c6-8510-c525edee3a31&pf_rd_r=9350XVYVVEWSJTZA10SF&pd_rd_wg=twHNw&pd_rd_r=7bdfe181-67b8-4612-8f34-128e40c19c96&pd_rd_i=B088FZXZHY"

webpage = requests.get(URL, headers=HEADERS, proxies=proxies)

soup = BeautifulSoup(webpage.content, features="html.parser")

# Outer Tag Object
title = soup.find(id='productTitle')

# Inner NavigableString Object
title_value = title.get_text()

print(title_value)