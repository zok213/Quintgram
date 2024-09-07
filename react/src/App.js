import './App.css';
import React, { useState} from "react";
import { Route, Routes} from 'react-router-dom';
import { TransitionGroup, CSSTransition } from "react-transition-group";
import { useLocation } from "react-router-dom";

import Cursor from './components/Cursor';
import Header from './components/Header';

import Guide from './pages/Guide';
import Draw from './pages/Draw';
import Popup from './pages/Popup'
import Fairytail from './pages/Fairytail';

function App() {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const location = useLocation(); // location variable.

  const handleMouseMove = (event) => {
    const { clientX, clientY } = event;
    setMousePos({ x: clientX, y: clientY });
  };


  return (
    <div className="App" onMouseMove={handleMouseMove}>
      <Cursor mousePos={mousePos}/>
      {location.pathname !== '/' && <Header/>} {/* Render the Header component only when it is not a guide page. */}
      <TransitionGroup>
        <CSSTransition key={location.key} classNames="fade" timeout={500}>
          <Routes location={location}>
            <Route path='/' element={<Guide/>}/>
            <Route path='/draw' element={<Draw/>} />
            <Route path='/popup' element={<Popup/>}/>
            <Route path='/fairytale' element={<Fairytail/>}/>
          </Routes>
        </CSSTransition>
      </TransitionGroup>
    </div>
  );
}

export default App;
