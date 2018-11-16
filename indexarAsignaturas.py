import os
import glob
import json
import sys
import getopt
import requests

# Indexa todos los ficheros que encuentre en el path
def indexarDocumentos(path, indice, host):
    for root, subdirs, files in os.walk(path):
        for subdir in subdirs:
            dir_path = os.path.join(root, subdir) 
            indexarDocumentos(dir_path, indice, host)
        for filename in files:
            # Construccion de la peticion POST para anhadir un documento
            file_path = os.path.join(root, filename) 
            url = 'http://'+host+'/'+indice+'/_doc/_bulk?pretty'
            headers = {'Content-Type' : 'application/json'}
            response = requests.post(url, data=open(file_path, 'rb'), headers=headers)
            
            # Comprobacion si han ocurrido errores al indexar
            jsonResponse = json.loads(response.content)
            if jsonResponse['errors']:
                print('\tError al subir el fichero '+filename)
            else:
                print('\tIndexados los documentos del fichero \"'+filename+'\"')

def crearIndice(host, indice):
    url = 'http://'+host+'/'+indice
    headers = {'Content-Type' : 'application/json'}
    response = requests.put(url, data=open("./mappingFieldsAsignatura.json", 'rb'), headers=headers)

    # Comprobacion de la respuesta
    jsonResponse = json.loads(response.content)
    try:
        ack = jsonResponse['acknowledged']
        if jsonResponse['acknowledged']:
            print('\tIndice \"'+indice+'\" creado')
    except KeyError as e:
        print('\tError: El indice \"'+indice+'\" ya existe')

def borrarIndice(host, indice):
    url = 'http://'+host+'/'+indice
    headers = {'Content-Type' : 'application/json'}
    response = requests.delete(url)
    
    # Comprobacion de la respuesta
    jsonResponse = json.loads(response.content)
    try:
        ack = jsonResponse['acknowledged']
        if jsonResponse['acknowledged']:
            print('\tIndice \"'+indice+'\" eliminado')
    except KeyError as e:
        print('\tError: El indice \"'+indice+'\" no existe')

def infoIndice(host, indice):
    url = 'http://'+host+'/_cat/indices/'+indice+'?v'

    headers = {'Content-Type' : 'application/json'}
    response = requests.get(url)
    print response.content
        
def help():
    print '\tIndexarElasticSearch.py -i <nombreIndice>  (Indexar en un indice)'
    print '\tIndexarElasticSearch.py -c <nombreIndice>  (Crear indice)'
    print '\tIndexarElasticSearch.py -d <nombreIndice>  (Borrar indice)'
    print '\tIndexarElasticSearch.py -e <nombreIndice>  (Informacion indice)'

def main(argv):
    path = './results' # Directorio donde se almacenan los archivos del crawleado
    host = 'localhost:9200'  # Endpoint de elasticsearch
    
    try:
        opts, args = getopt.getopt(argv,"hi:c:d:e:k:",["nombreIndice"])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-i", "--indexar"):
            if not os.path.exists(path):
                print("\tNo existe el directorio \"%s\""%path)
            else:
                indexarDocumentos(path, arg, host)
        elif opt in ("-c", "--crear"):
            crearIndice(host, arg)
        elif opt in ("-d", "--delete"):
            borrarIndice(host, arg)
        elif opt in ("-e", "--describe"):
            infoIndice(host, arg)
 
if __name__ == '__main__':
    main(sys.argv[1:])

   