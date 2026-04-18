import requests
from .models import HistoricoTesouro

def executar_sync_tesouro():
    url = "https://www.tesourodireto.com.br/o/rentabilidade/investir"
    
    # Headers mais completos para evitar bloqueio
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm',
    }

    try:
        # verify=False pode ser necessário se o seu servidor estiver com certificados SSL vovôs
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        ultimo = HistoricoTesouro.objects.order_by('-data_captura').first()
        if ultimo is not None and ultimo.payload_cru == data:
            print('JSON igual ao último registro; não será salvo porque não é diferente do JSON anterior.')
            return False, 'JSON igual ao último registro; não será salvo.'

        novo = HistoricoTesouro.objects.create(payload_cru=data)
        return True, novo
    except Exception as e:
        # Retornamos o erro para a View mostrar
        return False, str(e)
    
    
    
    
