import os
import time
import folium
import folium.plugins
import xml.etree.ElementTree as ET
import json
import random
from folium import Element 

# Defina a pasta onde seus arquivos KML estão localizados 
KML_DIR = "kml" 

# --- FUNÇÃO DE ESTILO INVISÍVEL PARA DADOS DE PESQUISA ---
def style_invisible(feature):
    # Retorna um estilo transparente e sem peso para evitar a visualização
    return {'fillColor': '#00000000', 'color': '#00000000', 'weight': 0, 'opacity': 0}

# --- Suas outras funções (gerador_coordenada, etc.) devem estar aqui ---
def gerador_coordenada(numero: str, dao) -> tuple[bool, str]:
    # Recebe latitude e longitude da DAO
    sucesso, resultado = dao(numero)
    if sucesso:
        link = f"https://www.google.com/maps?q={resultado.latitude},{resultado.longitude}"
        return True, link
    else:
        return False, resultado

def gerar_html_alimentador(nome_kml: str) -> str:
    """
    Gera um mapa Folium para o KML especificado, com barra de pesquisa funcional

    """
    
    caminho_kml = os.path.join(KML_DIR, nome_kml)
    
    if not os.path.exists(caminho_kml):
        print(f"ERRO FileNotFoundError: Arquivo KML não encontrado em: {caminho_kml}")
        return "" 

    NS = {'kml': 'http://www.opengis.net/kml/2.2'}
    elementos_ponto = []
    
    try:
        tree = ET.parse(caminho_kml)
        root = tree.getroot()
        
        for folder_name in ["TRANSFORMADOR", "CHAVES", "CAPACITOR"]:
            xpath_folder = f".//kml:Folder[kml:name='{folder_name}']"
            folder = root.find(xpath_folder, NS)
            
            if folder is not None:
                for placemark in folder.findall('kml:Placemark', NS):
                    nome = placemark.find('kml:name', NS).text if placemark.find('kml:name', NS) is not None else "Sem Nome"
                    point_tag = placemark.find('kml:Point', NS)
                    
                    if point_tag is not None:
                        coordinates_tag = point_tag.find('kml:coordinates', NS)
                        
                        if coordinates_tag is not None and coordinates_tag.text:
                            coords_str = coordinates_tag.text.strip().split(',')
                            
                            elementos_ponto.append({
                                'nome': nome.strip(),
                                'tipo': folder_name,
                                'latitude': float(coords_str[1]),
                                'longitude': float(coords_str[0])
                            })

    except Exception as e:
        print(f"Erro ao analisar KML: {e}")
        return "" 

    if not elementos_ponto:
        return "" 

    lats = [p['latitude'] for p in elementos_ponto]
    lons = [p['longitude'] for p in elementos_ponto]
    
    m = folium.Map(location=[(min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2], zoom_start=14)
    m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])

    features_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    # Preenchimento do GeoJSON com dados
    for p in elementos_ponto:
        features_geojson['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [p['longitude'], p['latitude']]
            },
            'properties': {
                'name': p['nome'] 
            }
        })


    # -----------------------------------------------------------
    # PASSO 1: ADICIONAR CAMADA DE BUSCA (A que deve ficar por BAIXO - Z-index baixo)
    # -----------------------------------------------------------
    
    camada_pesquisa_dados = folium.GeoJson(
        features_geojson, 
        style_function=style_invisible, 
        name=' ', 
        show=False 
    ).add_to(m) 
    
    # Adicionado antes dos Marcadores Visíveis!
    folium.plugins.Search(
        layer=camada_pesquisa_dados,
        search_label='name',
        placeholder='Buscar código do Equipamento (Ex: IT144000605)...',
        collapsed=False,
        position='topright',
        zoom_level=20
    ).add_to(m) 


    # -----------------------------------------------------------
    # PASSO 2: ADICIONAR CAMADA VISÍVEL (A que deve ficar por CIMA - Z-index alto)
    # -----------------------------------------------------------
    
    # O FeatureGroup deve ser adicionado por último para ter o Z-INDEX mais alto.
    camada_marcadores = folium.FeatureGroup(name='Equipamentos Visíveis').add_to(m)

    for p in elementos_ponto:
        # Define ícone e cor
        if p['tipo'] == 'TRANSFORMADOR':
            cor_icone = 'red'
            icone = 'flash'
            icon_prefix = 'fa'
        elif p['tipo'] == 'CHAVES':
            cor_icone = 'green'
            icone = 'toggle-on'
            icon_prefix = 'fa'
        elif p['tipo'] == 'CAPACITOR':
            cor_icone = 'purple'
            icone = 'bolt'
            icon_prefix = 'fa'
        else:
            cor_icone = 'gray'
            icone = 'circle'
            icon_prefix = 'fa'
        
        # 4.1. Adiciona o Marcador Padrão (PIN)
        folium.Marker(
            location=[p['latitude'], p['longitude']],
            tooltip=f"{p['tipo']}: {p['nome']}",
            icon=folium.Icon(color=cor_icone, icon=icone, prefix=icon_prefix)
        ).add_to(camada_marcadores)


    # -----------------------------------------------------------
    # PASSO 3: CONTROLE DE CAMADAS
    # -----------------------------------------------------------
    
    folium.LayerControl().add_to(m)

    # 8. Salva o mapa em um arquivo TEMPORÁRIO
    nome_arquivo_html = f"mapa_{nome_kml.replace('.kml', '')}_{int(time.time())}_{random.randint(1000, 9999)}.html"
    caminho_html_saida = os.path.join(os.getcwd(), nome_arquivo_html)
    m.save(caminho_html_saida)
    
    # A função retorna o caminho do arquivo temporário
    return caminho_html_saida