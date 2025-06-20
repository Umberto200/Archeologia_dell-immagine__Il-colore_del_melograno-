import xml.etree.ElementTree as ET
import json
import os

def process_graph():
    # Percorsi file (adattati alla tua struttura)
    xml_path = os.path.join('Metadata/lines/20/l20.xml')
    json_path = os.path.join('data', 'grafo_conoscenza.json')
    output_path = 'grafo_conoscenza_processed.json'
    
    # Elaborazione XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    verse_map = {}
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    for line in root.findall('.//tei:l', ns):
        num = line.get('n')
        if num:
            text = ''.join(line.itertext()).strip()
            verse_map[f'#{num}'] = text

    # Elaborazione JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)

    def update_items(obj):
        if isinstance(obj, dict):
            return {k: update_items(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [update_items(item) for item in obj]
        elif isinstance(obj, str):
            for placeholder, text in verse_map.items():
                obj = obj.replace(placeholder, text)
            return obj
        return obj

    processed_data = update_items(graph_data)
    
    # Salvataggio nella root (accessibile da GitHub Pages)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    process_graph()