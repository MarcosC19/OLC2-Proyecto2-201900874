import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom';

// PAGINAS A UTILIZAR EN LA NAVEGACION
import indexPage from './components/principal';
import interpreterPage from './components/interpreterPage';
import compilerPage from './components/compilerPage';
import mirrilaPage from './components/mirillaPage';
import blocksPage from './components/blockPage';
import reportsPage from './components/reportsPage';

export default function App() {
  return (
    <Router>
      <Route path="/" exact component={indexPage}></Route>
      <Route path="/Interpreter" component={interpreterPage}></Route>
      <Route path="/Compiler" component={compilerPage}></Route>
      <Route path="/OptMirr" component={mirrilaPage}></Route>
      <Route path="/OptBlock" component={blocksPage}></Route>
      <Route path="/Reports" component={reportsPage}></Route>
    </Router>
  );
}