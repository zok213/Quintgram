import React, { useState, useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import axios from "axios";


import img2 from '../images/fairytaleImg/result_img2.png'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";// 폰트어썸 모듈 이것도 찾아보시면 좋아요
import { faMusic } from "@fortawesome/free-solid-svg-icons";

const Fairytail = () => {
    const result = useSelector(state => state.result);
    const story = useSelector(state => state.story);
    const fairytale = useSelector(state => state.fairytaleImg);

    const [imageUrl, setImageUrl] = useState('');
    const [storyContents, setStoryContents] = useState('');
    const [fairytaleUrl, setFairytaleUrlUrl] = useState('');
    const voiceRef = useRef(null);
 
    useEffect(() => {
        const url = result[0].image;
        setImageUrl(url);
        }, [result]);

    useEffect(()=>{
        const contents = story;
        setStoryContents(contents)
    },[story])

    useEffect(()=>{
        const fairytaleImgResult = fairytale;
        setFairytaleUrlUrl(fairytaleImgResult)
    },[fairytale])

    const voiceButton = async ()=>{
        try {
        //Send a POST request and get a response from the server.
        const voiceResponse = await axios.post('http://127.0.0.1:5000/get_voice', {}, { responseType: 'blob' });// http://101.101.101.101:80
    
        //Converts the received data into blob objects.
        const voiceBlob = new Blob([voiceResponse.data], { type: 'audio/mpeg' });
    
        //Pass the blob object to the Audio object.
        const voice = new Audio(URL.createObjectURL(voiceBlob));
        voiceRef.current = voice;
        } catch (error) {
            console.error(error);
        }
        voiceRef.current.play();
    }


  return (
    <div className='fairytail_container'>
        <div className='img_container'>
            {imageUrl ? <img src={fairytaleUrl} alt="Children's Book Images" /> : null}
        </div>

        <div className='story_container'>
            <div className='story'>
                <div className='draw_img'>
                    {imageUrl ? <img src={imageUrl} alt='Drawing by me' /> : null}
                </div>
                <div className='story_contents'><span>“</span>{storyContents} <span>”</span></div>
                <button className="voice" onClick={voiceButton}><div>Play your voice <FontAwesomeIcon icon={faMusic} /></div></button>
            </div>
            <div className='story_img'>
                <div><img src={img2} alt="Storybook Decorating Images"/></div>
            </div>
        </div>
    </div>
  )
}

export default Fairytail