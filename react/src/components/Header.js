import React from 'react'
import { useNavigate } from 'react-router-dom'


import logo from '../images/headerImg/logo.png'
import drawButton from '../images/headerImg/drawButton.png'
import guideButton from '../images/headerImg/guideButton.png'




const Header = () => {

    const navigate = useNavigate();
    const goToDraw = () => {
        navigate('/draw')
    };

    const goToGuide = () => {
        navigate('/')
    };

  return (
    <div className='header_container'>
            <h1><img className='logo' src={logo} alt='Logo image'/></h1>
            <ul>
                <li><button onClick={goToDraw}><img className='draw_button' src={drawButton} alt='Sketchbook move button'/></button></li>
                <li><button onClick={goToGuide}><img className='guide_button' src={guideButton} alt='Guide movement button'/></button></li>
            </ul>
    </div>
  )
}

export default Header
