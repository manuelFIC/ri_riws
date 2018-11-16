# -*- coding: utf-8 -*-
import scrapy

class AsignaturaItem(scrapy.Item):

    url = scrapy.Field()
    nombre_asignatura = scrapy.Field()
    nombre_titulacion = scrapy.Field() 
    nombre_centro = scrapy.Field() 
    codigo = scrapy.Field()
    cuatrimestre = scrapy.Field()
    tipo = scrapy.Field()
    creditos = scrapy.Field()
    curso = scrapy.Field()
    coordinadores = scrapy.Field()
    profesores = scrapy.Field()
    departamento = scrapy.Field()
    descripcion = scrapy.Field()
    competencias = scrapy.Field()
    contenidos = scrapy.Field()
    pass

