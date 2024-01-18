#epias sitesinden 24 saatlik arz talep cekme
#gerekli kutuphaneler
import requests as _requests
import json as _json
import datetime as _dt
import pandas as _pd
import numpy as _np

def arztalepcek():
    url_arztalep = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/supply-demand"


    #arztalep icin default tarih
    today = _dt.date.today()
    tomorrow = today + _dt.timedelta(days=0)
    # Saat dilimi ofsetini oluştur
    offset = _dt.timezone(_dt.timedelta(hours=3))


    # Boş bir DataFrame oluştur
    all_arztalep = _pd.DataFrame()

    # Saat saat artan bir döngü
    #her saat arztalebi cekmek icin
    for hour in range(24):
        # Tarihi ve saati güncelle
        current__dt = _dt._dt.combine(tomorrow, _dt.time(hour, 0)).replace(tzinfo=offset)
        
        # formatted__dt'u oluştur
        formatted__dt = current__dt.isoformat()
    
        # JSON oluştur
        payload = _json.dumps({
            "date": formatted__dt
        })

        # İsteği gönder
        response = _requests.post(url_arztalep, data=payload, headers={'Content-Type': 'application/json'})

        # Yanıtı DataFrame'e çevir
        data = _json.loads(response.text)

        # "items" dizisine ulaşın
        items_list = data.get('items', [])

        # Liste elemanlarını DataFrame'e çevirin
        df = _pd.DataFrame(items_list)
        
        df= df.drop(columns=['date'])
        df = df[['price', 'demand', 'supply']]
        df= df.reset_index(drop=True )
        
        all_arztalep = _pd.concat([all_arztalep, df], axis=1)
    #arz degerlerini negatif turden pozitife cevirme
    all_arztalep["supply"]= all_arztalep["supply"]* -1
    #nan gelen yerleri bosluga cevirme
    all_arztalep = all_arztalep.fillna("")

    #sutun isimlerini degistirme
    all_arztalep = all_arztalep.rename(columns={
        'price': 'Fiyat',
        'supply': 'Arz',
        'demand': 'Talep',
    })
    # DataFrame'i kaydet

    return all_arztalep