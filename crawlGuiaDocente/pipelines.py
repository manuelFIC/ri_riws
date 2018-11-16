# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


    
import json
import os
import shutil
import logging

class JsonPipeline(object):

    def open_spider(self, spider):
        self.path = './results'
        self.titulacion = ''
        self.file = None
        self.contador = 0

        # Borrado y creación de la carpeta "results" para almacenar los
        # resultados de crawlear

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            shutil.rmtree(self.path, ignore_errors=True)
            os.makedirs(self.path) 


    def close_spider(self, spider):
        self.file.write("\n")
        self.file.close()

    def process_item(self, item, spider):

        # Creación/Apertuda del fichero correspondiente para guardar
        # la información del item

        if self.titulacion != item['nombre_titulacion']:
            if self.file is not None:
                self.file.close()
            carpeta = item['nombre_centro']
            if not os.path.exists(self.path+'/'+carpeta):
                os.makedirs(self.path+'/'+carpeta)
            strNorm = item['nombre_titulacion'].replace(":", "").replace("/","-");
            strFile = self.path+'/'+carpeta+'/'+strNorm+'.json'
            self.file = open(strFile, 'ab')
            self.titulacion = item['nombre_titulacion']            

        # Creación de una línea con el identificador de documento
        # Necesario para indexar de manera automatica en elasticsearch
        partesCodigo = item['codigo'].split('G')
        if len(partesCodigo)>0:
            if len(partesCodigo)==1:
                codigo = partesCodigo[0]
            else:
                codigo = partesCodigo[0]+"7"+partesCodigo[1]
            idf = {}
            idf['_id']= codigo
            index = {}
            index['index'] = idf
            line = json.dumps(dict(index),) + "\n"
            self.file.write(line)

            #Creación del objeto JSON de la asignatura
            line = json.dumps(dict(item), sort_keys=True, ) + "\n"
            self.file.write(line)
            self.contador = self.contador+1

            #Mensaje de log
            logger = logging.getLogger()
            nombre_asignatura = item['nombre_asignatura']
            nombre_titulacion = item['nombre_titulacion']
            codigo = item['codigo']
            porcentajeF = (self.contador/3773.0)*100
            porcentaje = ['%.2f' % porcentajeF]
            msg = "   ["+porcentaje[0]+"%]\t--> Titulacion: "+nombre_titulacion+"\tAsignatura: "+nombre_asignatura+" ("+codigo+")"
            logger.info(msg)

        return item