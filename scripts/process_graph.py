import xml.etree.ElementTree as ET
import json
import os
import sys


def process_graph():
    base_dir = os.getcwd()
    xml_path = os.path.join(base_dir, 'Metadata', 'lines', '20', 'l20.xml')
    json_path = os.path.join(base_dir, 'grafo_conoscenza.json')
    output_path = os.path.join(base_dir, 'grafo_conoscenza_processed.json')
    if not os.path.exists(xml_path):
        print(f"ERRORE: File XML non trovato in {xml_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(json_path):
        print(f"ERRORE: File JSON non trovato in {json_path}", file=sys.stderr)
        sys.exit(1)
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

if __name__ == '__main__':
    print("=== AVVIO SCRIPT ===")
    process_graph()
    print("=== ELABORAZIONE COMPLETATA ===")