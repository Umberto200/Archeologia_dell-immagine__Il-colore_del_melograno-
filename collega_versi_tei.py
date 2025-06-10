import json
import xml.etree.ElementTree as ET

# Percorsi dei file
xml_file = "l20.xml"
json_file = "grafo_conoscenza.json"
output_file = "grafo_conoscenza_updated.json"

# Parsing del file XML TEI
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace TEI
namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Estrazione dei versi numerati dal file XML
versi = {}
for l in root.findall(".//tei:l", namespaces):
    numero = l.attrib.get("n")
    testo = ''.join(l.itertext()).strip() if l is not None else ""
    if numero:
        versi[numero] = testo

# Caricamento del file JSON
with open(json_file, "r", encoding="utf-8") as f:
    grafo = json.load(f)

# Funzione ricorsiva per aggiornare i campi "ex:testo"
def aggiorna_testi(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "ex:testo" and isinstance(v, str) and v.startswith("#"):
                numero = v.lstrip("#")
                if numero in versi:
                    obj[k] = versi[numero]
            else:
                aggiorna_testi(v)
    elif isinstance(obj, list):
        for item in obj:
            aggiorna_testi(item)

# Aggiornamento del grafo
aggiorna_testi(grafo)

# Salvataggio del grafo aggiornato
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(grafo, f, ensure_ascii=False, indent=2)

print(f"Grafo aggiornato salvato in '{output_file}'")
