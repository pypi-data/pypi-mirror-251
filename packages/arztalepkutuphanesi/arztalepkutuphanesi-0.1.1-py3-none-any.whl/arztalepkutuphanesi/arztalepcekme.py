import requests as _requests
import json as _json
import datetime as _datetime
import pandas as _pd



arztalep_url = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/supply-demand"
today = _datetime.date.today()
tomorrow = today + _datetime.timedelta(days=0)
def arztalepcek(tarih=tomorrow):


    # Saat dilimi ofsetini oluştur
    offset = _datetime.timezone(_datetime.timedelta(hours=3))

    # Boş bir DataFrame oluştur
    all_data = _pd.DataFrame()

    # Saat saat artan bir döngü
    for hour in range(24):
        # Tarihi ve saati güncelle
        current_datetime = _datetime.datetime.combine(tarih, _datetime.time(hour, 0)).replace(tzinfo=offset)
        
        # formatted_datetime'u oluştur
        formatted_datetime = current_datetime.isoformat()
    
        # JSON oluştur
        payload = _json.dumps({
            "date": formatted_datetime
        })

        # İsteği gönder
        response = _requests.post(arztalep_url, data=payload, headers={'Content-Type': 'application/json'})

        # Yanıtı DataFrame'e çevir
        data = _json.loads(response.text)

        # "items" dizisine ulaşın
        items_list = data.get('items', [])

        # Liste elemanlarını DataFrame'e çevirin
        df = _pd.DataFrame(items_list)
        
        df= df.drop(columns=['date'])
        df = df[['price', 'demand', 'supply']]
        df= df.reset_index(drop=True )
        
        all_data = _pd.concat([all_data, df], axis=1)
    all_data["supply"]= all_data["supply"]* -1
    all_data = all_data.fillna("")

    all_data = all_data.rename(columns={
        'price': 'Fiyat',
        'supply': 'Arz',
        'demand': 'Talep',
    })
    # DataFrame'i kaydet

    return all_data