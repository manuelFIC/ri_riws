import React, { Component } from 'react';
import './App.css';
import { 
  ReactiveBase,
  DataSearch,
  MultiList,
  SelectedFilters,
  ResultList,
  DynamicRangeSlider,
 } from '@appbaseio/reactivesearch';


//Functiones para mostrar la lista de profesores
function ListItem(props) {
  return  <tr width="100%">
            <td className="primera-columna-prof"><a className="titulo-campo-prof">{props.value.nombre}</a>  </td>
            <td className="segunda-columna-prof"><a className="atributo-campo-prof">{props.value.email}</a> </td>
          </tr>;
}

function ProfesoresList(props) {
  const coordinadores = props.coordinadores;
  const listItems = coordinadores.map((coordinador) =>
    <ListItem  value={coordinador} />
  );
  return (
    <table width="100%"> 
      <tbody>
        {listItems}
      </tbody>    
    </table>
  );
}


//Functiones para mostrar la lista de competencias
function ListCompetenciasItem(props) {
  return  <tr width="100%">
            <td className="primera-columna-competencias">{props.value.codigo} </td>
            <td className="segunda-columna-competencias">{props.value.competencia} </td>
          </tr>;
}

function CompetenciasList(props) {
  const competencias = props.competencias;
  const listItems = competencias.map((competencia) =>
    <ListCompetenciasItem  value={competencia} />
  );
  return (
    <table width="100%"  className="competencias-table"> 
      <tbody>
        {listItems}
      </tbody>    
    </table>
  );
}


//Functiones para mostrar la lista de contenidos
function ListContenidosTemaItem(props) {
  return <h3>{props.value.tema}</h3> 
}

function ListContenidosSubtemaItem(props) {
  return <h3>{props.value.subtema}</h3> 
}

function LineaContenidosList(props) {
  const linea = props.value;
  const listItemsTemas = linea.temas.map((tema) =>
    <ListContenidosTemaItem  value={tema} />
  );
  const listItemsSubtemas = linea.subtemas.map((subtema) =>
    <ListContenidosSubtemaItem  value={subtema} />
  );

  return (
    <tr width="100%">
      <td className="primera-columna-contenidos">{listItemsTemas} </td>
      <td className="segunda-columna-contenidos">{listItemsSubtemas} </td>
    </tr>
  );
}

function ContenidosList(props) {
  const contenidos = props.contenidos;
  const listItems = contenidos.map((linea) =>
    <LineaContenidosList value={linea} />
  );
  return (
    <table width="100%"  className="contenidos-table"> 
      <tbody>
        {listItems}
      </tbody>    
    </table>
  );
}






class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (

      <div className="main-container">
        <ReactiveBase
          app="asignatura"
          url="http://localhost:9200"        
         >
         <div className="navbar">
            <div className="logo-container">
              <a href="https://www.udc.es/">
                <img
                  className="app-logo"
                  src="Images/logo.png"
                  alt="Universidade da Coruña"
                />
              </a> 
            </div>
            <div className="search-container">
              <div className="search-container2">
                <DataSearch componentId="mainSearch"
                  className="search-bar"
                  dataField={[
                    "nombre_asignatura", 
                    "nombre_titulacion", 
                    "nombre_centro", 
                    "codigo", 
                    "cuatrimeste", 
                    "tipo", 
                    "curso", 
                    "coordinadores.nombre", 
                    "coordinadores.email", 
                    "profesores.nombre", 
                    "profesores.email", 
                    "departamento", 
                    "descripcion", 
                    "competencias.codigo", 
                    "competencias.competencia", 
                    "contenidos.subtemas.subtema", 
                    "contenidos.temas.tema" ]} 
                  fieldWeights={[5, 3, 3, 4, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1 ]}
                  categoryField={[
                    "nombre_asignatura", 
                    "nombre_titulacion", 
                    "nombre_centro", 
                    "codigo", 
                    "cuatrimeste", 
                    "tipo", 
                    "curso", 
                    "coordinadores.nombre", 
                    "coordinadores.email", 
                    "profesores.nombre", 
                    "profesores.email", 
                    "departamento", 
                    "descripcion", 
                    "competencias.codigo", 
                    "competencias.competencia", 
                    "contenidos.subtemas.subtema", 
                    "contenidos.temas.tema"]}
                  queryFormat="and"
                  highlight={false}
                  placeholder="Procura de asignaturas..."
                  iconPosition="right"
                  autosuggest={true}
                  filterLabel="búsqueda"      
                />
                <SelectedFilters showClearAll={true}
                  clearAllLabel="Borrar filtros"
                />
              </div>
            </div>
         </div>
         <hr className="separador-navbar"></hr>
         <div className="sub-container">
            <div className="left-bar-container">
              <div className="left-bar">
                <MultiList componentId="centros-list"
                  dataField="nombre_centro.keyword"
                  className="margen-filtros"
                  size={25}
                  sortBy="asc"
                  title="Filtro por Centros"
                  queryFormat="or"
                  selectAllLabel="Todos os centros"
                  showCheckbox={true}
                  showCount={true}
                  showSearch={true}
                  placeholder="Buscar centro..."
                  react={{
                    and: [
                      "creditosSlider",
                      "mainSearch",
                      "titulaciones-list",
                      "cursos-list"
                    ]
                  }}
                  renderListItem={(label, count) => (
                    <div >
                        {label}
                        <span style={{ marginLeft: 5, color: "#c6007d" }}>
                            {count}
                        </span>
                    </div>
                  )}
                  showFilter={true}
                  filterLabel="Centro"
                  URLParams={false}
                  innerClass={{
                    label: "list-item",
                    input: "list-input",
                    list: "list-filtro",
                    title: "tituloFilter"
                  }}
                />
                <hr className="separador-lateral" />
                <MultiList componentId="titulaciones-list"
                  dataField="nombre_titulacion.keyword"
                  className="margen-filtros"
                  size={25}
                  sortBy="asc"
                  title="Filtro por Titulación"
                  queryFormat="or"
                  selectAllLabel="Todas as Titulacions"
                  showCheckbox={true}
                  showCount={true}
                  showSearch={true}
                  placeholder="Buscar titulación..."
                  react={{
                    and: [
                      "creditosSlider",
                      "mainSearch",
                      "centros-list",
                      "cursos-list"
                    ]
                  }}
                  renderListItem={(label, count) => (
                    <div >
                        {label}
                        <span style={{ marginLeft: 5, color: "#c6007d" }}>
                            {count}
                        </span>
                    </div>
                  )}
                  showFilter={true}
                  filterLabel="Titulación"
                  URLParams={false}
                  innerClass={{
                    label: "list-item",
                    input: "list-input",
                    list: "list-filtro",
                    title: "tituloFilter"
                  }}
                />
                <hr className="separador-lateral" />
                <MultiList componentId="cursos-list"
                  dataField="curso.keyword"
                  className="margen-filtros"
                  size={25}
                  sortBy="asc"
                  title="Filtro por Curso"
                  queryFormat="or"
                  selectAllLabel="Todos os Cursos"
                  showCheckbox={true}
                  showCount={true}
                  showSearch={false}
                  react={{
                    and: [
                      "creditosSlider",
                      "mainSearch",
                      "centros-list",
                      "titulaciones-list"
                    ]
                  }}
                  renderListItem={(label, count) => (
                    <div >
                        {label}
                        <span style={{ marginLeft: 5, color: "#c6007d" }}>
                            {count}
                        </span>
                    </div>
                  )}
                  showFilter={true}
                  filterLabel="Curso"
                  URLParams={false}
                  innerClass={{
                    label: "list-item",
                    input: "list-input",
                    list: "list-filtro",
                    title: "tituloFilter"
                  }}
                />
                <hr className="separador-lateral" />
                <DynamicRangeSlider componentId="creditosSlider"
                  dataField="creditos"
                  className="margen-filtros"
                  title="Créditos"
                  defaultSelected={(min, max) => (
                    {
                      "start": min,
                      "end": max
                    }
                  )}
                  rangeLabels={(min, max) => (
                    {
                      "start": min + " cr.",
                      "end": max + " cr."
                    }
                  )}
                  stepValue={1}
                  showHistogram={true}
                  showFilter={true}
                  interval={2}
                  react={{
                    and: [
                    "mainSearch",
                    "centros-list",
                    "cursos-list",
                    "titulaciones-list"
                    ]
                  }}
                  innerClass={{
                    title: "tituloFilter",
                    slider: "slider-slider",
                    label: "label-slider",
                  }}
                  URLParams={true}
                />
              </div>
            </div>
                  
            <div className= "result-container">
              <ResultList
                componentId="results"
                dataField="nombre_asignatura"
                className="lista_asignaturas"
                react={{
                  and: [
                    "mainSearch",
                    "centros-list",
                    "cursos-list",
                    "titulaciones-list",
                    "creditosSlider",
                  ]
                }}
                pagination={true}
                showResultStats={true}
                paginationAt= "bottom"
                size={10}
                loader="Cargando..."
                noResults="Non se encontraron resultados ..."
                sortOptions={[
                  {
                    dataField: "_score",
                    sortBy: "desc",
                  }
                ]}
                innerClass={{
                  title: "result-title",
                  listItem: "result-item",
                  list: "list-container",
                  resultsInfo: "result-list-info",
                  sortOptions: "sort-options",
                  poweredBy: "powered-by",
                  noResults: "result-stats"
                }}
                onResultStats={(total_results, time_taken) => (
                  <div className="result-stats-custom">
                      {total_results} resultados en {time_taken} ms 
                  </div>
                )}
                onData={function(res) {
                  return {
                
                    description: (
                      <div className="main-description">
                        <div className="ih-item square effect6 top_to_bottom">  
                            <div className="info colored">
                              <div className="title-result-container">
                              <table width="100%">
                                  <tbody>
                                    <tr width="100%">
                                    <td className="titulo-asignatura"> <a href={res.url}><h3 className="overlay-title">{res.nombre_asignatura}</h3> </a> </td>
                                    <td className="codigo-asignatura"> <a href={res.url}><h3 className="overlay-title-codigo">{res.codigo}</h3> </a> </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                              <hr className="separador-result-title"></hr>
                              <div className="overlay-description">
                                <table width="100%">
                                  <tbody>
                                    <tr width="100%">
                                    <td className="primera-columna"><a className="titulo-campo">Titulación</a>  </td>
                                    <td className="segunda-columna"><a className="atributo-campo">{res.nombre_titulacion}</a> </td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Centro</a>  </td>
                                    <td className="segunda-columna"><a className="atributo-campo">{res.nombre_centro}</a> </td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Curso</a>  </td>
                                    <td className="segunda-columna"><a className="atributo-campo">{res.curso}</a> </td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Cuatrimestre</a> </td>
                                    <td className="segunda-columna"><a className="atributo-campo">{res.cuatrimestre}</a></td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Tipo</a></td>
                                    <td className="segunda-columna"><a className="atributo-campo">{res.tipo}</a></td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Créditos</a></td>
                                    <td className="segunda-columna"> <a className="atributo-campo">{res.creditos}</a></td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Departamento</a> </td>
                                    <td className="segunda-columna"> <a className="atributo-campo">{res.departamento}</a></td>
                                    </tr>
                                    <tr>
                                    <td className="primera-columna"><a className="titulo-campo">Descripción</a> </td>
                                    <td className="segunda-columna"> <a className="atributo-campo">{res.descripcion}</a></td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                              <hr className="separador-result-title"></hr>
                              <div className="coordinadores-container">
                                <h3 className="titulo-prof">
                                  Coordinadores 
                                </h3>
                                <ProfesoresList coordinadores={res.coordinadores} />
                              </div>
                              <hr className="separador-result-title"></hr>
                              <div className="coordinadores-container">
                                <h3 className="titulo-prof">
                                  Profesores 
                                </h3>
                                <ProfesoresList coordinadores={res.profesores} />
                              </div>
                              <hr className="separador-result-title"></hr>
                              <div className="contenidos-container">
                                <h3 className="titulo-contenidos">
                                  Contidos
                                </h3>
                                <ContenidosList contenidos={res.contenidos} />
                              </div>
                              <hr className="separador-result-title"></hr>
                              <div className="competencias-container">
                                <h3 className="titulo-competencias">
                                  Competencias
                                </h3>
                                <CompetenciasList competencias={res.competencias} />
                              
                              </div>
                            </div>
                        </div>
                      </div>
                    ),
                   };
                }}
                onNoResults="Resultados non encontrados"
              />
            </div>
         </div>
        </ReactiveBase>
      </div>
    );
  }
}
export default App;
