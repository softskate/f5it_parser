from datetime import datetime, timedelta
import time
import requests
from database import App, Crawl, Product
from keys import payload


def run_spider():
    while True:
        old_crawlers = Crawl.select().where(Crawl.created_at < (datetime.now() - timedelta(days=3)))
        dq = (Product
            .delete()
            .where(Product.crawlid.in_(old_crawlers)))
        dq.execute()
        Crawl.delete().where(Crawl.finished==False)

        appid = App.create(name='f5it')
        crawlid = Crawl.create()
        

        while True:
            try:
                resp = requests.post('https://b2b.1091.ru/api/?format=json', json=payload)
                js_data = resp.json()
                break
            except Exception as e:
                print(f'Error occurred while scraping: {e}')
            time.sleep(60)

        for prod in js_data['Tovar']:
            if 'CollOnPrice' in prod: continue
            item = Product()
            item.appid = appid
            item.crawlid = crawlid
            item.name = prod['Name']
            item.productId = prod['Article']
            item.qty = prod['SkladMSK']
            item.brandName = prod['BrandName']
            item.price = prod['PriceMSK_RUR']
            item.category = ' - '.join([prod[f'razdel{x+1}'] for x in range(3)])
            item.details = {
                "key": prod['key'],
                "Kod1C": prod['Kod1C'],
                "VendorCode": prod['VendorCode'],
                "BrandName": prod['BrandName'],
                "Waranty": prod['Waranty'],
                "SkladMSK": prod['SkladMSK'],
                "SkladNSK": prod['SkladNSK'],
                "TransitMSK": prod['TransitMSK'],
                "TransitNSK": prod['TransitNSK'],
                "DateTransitMSK": prod['DateTransitMSK'],
                "DateTransitNSK": prod['DateTransitNSK'],
                "SourceCode": prod['SourceCode'],
                "KolInPack": prod['KolInPack'],
                "Weight": prod['Weight'],
                "Scope": prod['Scope'],
            }
            item.save(True)
            
        crawlid.finished = True
        crawlid.save()
        time.sleep(60*60)


if __name__ == '__main__':
    while True:
        try: run_spider()
        except Exception as e: print(f'Unexpected exception occurred {e}')
        time.sleep(5)
