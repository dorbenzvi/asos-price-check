import re
import requests

def getImg(productUrl, productId):
    newurl = re.findall("\/([0-9a-zA-Z+.-]+)[\/&| ]",productUrl)
    print(newurl[1])
    print(productUrl)
    mark = re.findall(r"clr=[a-z,-]*&", productUrl)
    # print(mark[0][4:-1])
    newmark=mark[0][4:-1]
    newmark=newmark.replace("-","")
    print(newmark)
    newgoodurl = "https://images.asos-media.com/products/"+newurl[1]+"/"+productId+"-1-"+newmark+"?$&wid=513&fit=constrain"
    print(newgoodurl)
    return newgoodurl
