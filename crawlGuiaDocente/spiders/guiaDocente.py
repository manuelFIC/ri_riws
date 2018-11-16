# -*- coding: utf-8 -*-
import scrapy
import urllib
import urllib2
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from ..items import AsignaturaItem

class GuiadocenteSpider(CrawlSpider):
    name = 'guiaDocente'
    allowed_domains = ["udc.es",]
    start_urls = ['https://www.udc.es/ensino/guiasdocentes//']

    rules = (

        # Extracción de todos los links de todas las facultades. Se restringe la extracción a los 
        #    links terminados en r'.*\/index.php\?centre=[0-9]{1,3}$' y que se encuentren en la 
        #    sección principal. Esta regla hara que los links de las distintas facultades se 
        #    parseen con la función 'parse_centro'
        Rule(LinkExtractor(allow=(r'.*\/index.php\?centre=[0-9]{1,3}$'),  restrict_xpaths=('//div[@class="ap-section udc-user-content "]'))),

        # Acceso a la página que contiene  los links de cada titulación  
        Rule(LinkExtractor(allow=(r'.*\/index.php\?centre=[0-9]{1,3}\&ensenyament=null$'), restrict_xpaths=('//div[@id="menu"]')),),

        # Acceso a cada titulación  
        Rule(LinkExtractor(allow=(r'.*\/index.php\?centre=[0-9]{1,3}\&ensenyament=[a-zA-Z0-9]{6}$'), restrict_xpaths=('//a[@class="subapartat"]'))),

        # Acceso a la página que contiene las asignaturas de una titulacion
        Rule(LinkExtractor(allow=(r'.*\&consulta=assignatures$'), restrict_xpaths=('//div[@id="contingut"]')),),

        # Acceso a la información de una asignatura concreta
        Rule(LinkExtractor(allow=(r'.*\&assignatura=[a-zA-Z0-9]{9}\&any_academic=[0-9]{4}\_[0-9]{2}$'), restrict_xpaths=('//div[@id="contingut"]')), callback="parse_asignatura", follow=True),    )


    def parse_asignatura(self, response): 
    	# Parseo de la cabecera de la asignatura

        # Objeto asignatura
        asignatura = AsignaturaItem()

        # 0.- Obtención de la url de la asignatura
        asignatura['url'] = response.url

        # 1.- Obtención del nombre de la asignatura
        asignatura['nombre_asignatura'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[3]/td[2])').extract_first()

        # 2.- Obtención del nombre de la titulación
        asignatura['nombre_titulacion'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[4]/td[2]/table/tr[1])').extract_first()

        # 3.-Obtención del nombre del centro
        asignatura['nombre_centro'] = response.selector.xpath('normalize-space(//div[@id="access"]/table/tr/td[3]/span[2])').extract_first()

        # 4.- Obtención del código de la asignatura
        asignatura['codigo'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[3]/td[4])').extract_first()
        
        # 5.- Obtención del cuatrimestre
        asignatura['cuatrimestre'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[6]/td[2]//text())').extract_first()

        # 6.- Obtencion del tipo de asignatura
        asignatura['tipo'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[6]/td[4])').extract_first()

        # 7.- Obtencion de los creditos de la asignatura
        asignatura['creditos'] = float(response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[6]/td[5])').extract_first())

        # 8.- Obtencion del curso
        asignatura['curso'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[6]/td[3])').extract_first()

        # 9.- Obtencion del departamento de la asignatura
        asignatura['departamento'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[9]/td[2])').extract_first()

        # 10.- Obtención de los coordinadores
        coordinadores = []
        nombres_html = response.selector.xpath('//div[@id="contingut"]/div/table[2]/tr[10]/td[2]/table/tr//text()').extract()
        emails_html = response.selector.xpath('//div[@id="contingut"]/div/table[2]/tr[10]/td[4]/table/tr//text()').extract()
        if (len(nombres_html)==len(emails_html))and(len(nombres_html)!=0)and(len(emails_html)!=0):
            for i in range(0,len(emails_html)):
            	profesor = {}
                profesor['nombre'] = nombres_html[i]
                profesor['email'] = emails_html[i]
                coordinadores.append(profesor)
        
        asignatura['coordinadores'] = coordinadores
		
        # 11.- Obtención de los profesores y sus emails
        profesores = []
        nombres_html = response.selector.xpath('//div[@id="contingut"]/div/table[2]/tr[11]/td[2]/table/tr//text()').extract()
        emails_html = response.selector.xpath('//div[@id="contingut"]/div/table[2]/tr[11]/td[4]/table/tr//text()').extract()
        if (len(nombres_html)==len(emails_html))and(len(nombres_html)!=0)and(len(emails_html)!=0):
            for i in range(0,len(emails_html)):
            	profesor = {}
                profesor['nombre'] = nombres_html[i]
                profesor['email'] = emails_html[i]
                profesores.append(profesor)

        asignatura['profesores'] = profesores 

        # 12.- Obtencion de la descripcion de la asignatura
        asignatura['descripcion'] = response.selector.xpath('normalize-space(//div[@id="contingut"]/div/table[2]/tr[13]/td[2])').extract_first()

        # Siguiente paso, parsear la seccion 1 de la asignatura (si existe)
        links = LinkExtractor(restrict_xpaths=('//a[@id="seccio1"]')).extract_links(response)
        if len(links)>0:
            url = links[0].url
            yield scrapy.Request(url, callback=self.seccion1, meta={'asignatura': asignatura})
        else:
            asignatura['competencias'] = [] 
            asignatura['contenidos'] = []
            yield asignatura

    def seccion1(self, response):
        # Parseo de la seccion 1 (Competencias del titulo)

        # Se recibe en 'meta' lo ya parseado anteriormente de la asignatura
        asignatura= response.meta['asignatura']
        
        # 13.- Obtencion de las competencias de la asignatura
        competencias = []
        codigos_html = response.selector.xpath('//div[@id="contingut"]/div/table[last()]/tr/td[1]//text()').extract()
        competencias_html = response.selector.xpath('//div[@id="contingut"]/div/table[last()]/tr/td[2]//text()').extract() 
        if (len(codigos_html)==len(competencias_html))and(len(codigos_html)!=0)and(len(competencias_html)!=0):
            for i in range(3,len(competencias_html)):
                competencia = {}
                competencia['codigo'] = codigos_html[i].strip()
                competencia['competencia'] = competencias_html[i].strip()
                competencias.append(competencia)
        
        asignatura['competencias'] = competencias 
      
        # Siguiente paso, parsear la seccion 1 de la asignatura (si existe) (Contenidos de la asignatura)
        links = LinkExtractor(restrict_xpaths=('//a[@id="seccio3"]')).extract_links(response)
        if len(links)>0:
            url = links[0].url
            yield scrapy.Request(url, callback=self.seccion3, meta={'asignatura': asignatura})
        else:
            asignatura['contenidos'] = []
            yield asignatura

    def seccion3(self, response):
        # Parseo de la seccion 3 (Contenidos de la asignatura)
 
        # Se recibe en 'meta' lo ya parseado anteriormente de la asignatura
        asignatura= response.meta['asignatura']
        
        # 13.- Obtencion de los contenidos de la asignatura

        contenidos = []

        linea = response.selector.xpath('//div[@id="contingut"]/div/table[last()]/tr/td[1]').extract()
        if len(linea)>0:
            for i in range(1, len(linea)):
                temas = []
                temas_html = response.selector.xpath('//div[@id="contingut"]/div/table[last()]/tr['+str(i+1)+']/td[1]//text()').extract()
                for k in range(0, len(temas_html)):
                    tema = {}
                    tema['tema'] = temas_html[k].strip()
                    temas.append(tema)

                subtemas = []
                subtemas_html = response.selector.xpath('//div[@id="contingut"]/div/table[last()]/tr['+str(i+1)+']/td[2]//text()').extract()
                for k in range(0, len(subtemas_html)):
                    subtema = {}
                    subtema['subtema'] = subtemas_html[k].strip()
                    subtemas.append(subtema)

                contenido = {}
                contenido['temas'] = temas
                contenido['subtemas'] = subtemas                 
                contenidos.append(contenido)

        asignatura['contenidos'] = contenidos

        yield asignatura

