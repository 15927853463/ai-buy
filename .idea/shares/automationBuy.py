import os
import asyncio
from pyppeteer import launch
import datetime
import time
import random


width, height = 1600, 900

# ==== 设定账号密码 （修改此处，指定账号密码）====


# ==== 设定时间 （修改此处，指定时间点）====

#buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')

now_time = datetime.datetime.now()
async def main():
    url = 'http://quote.eastmoney.com/concept/sh600337.html?from=zixuan'
    browser = await launch(
        headless=False,  #设置pyppeteer为有头模式
        args=[f'--window-size={width},{height}', '--disable-infobars']  #设置网页大小，无监控头
    )
    #在浏览器上创建新页面
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    await page.setViewport({'width': width, 'height': height})
    await page.goto(url)
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
    )
    await asyncio.sleep(2)

    await test(page)
    await asyncio.sleep(100)

async def test():
    await page.click('')

asyncio.get_event_loop().run_until_complete(main())