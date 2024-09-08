import React, { useState, useEffect } from 'react';
import axios from "axios";

import { useSelector,useDispatch  } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import popupImg from '../images/popupImg/popupImg.png'
import popupTrue from '../images/popupImg/popupTrue.png'
import popupFalse from '../images/popupImg/popupFalse.png'

import Loading from '../components/Loading';


const Popup = () => {
    const navigate = useNavigate();

    const result = useSelector(state => state.result);
    const [imageUrl, setImageUrl] = useState('');
    const [name, setname] = useState('');
    const [loading, setLoading] = useState(false);


    const dispatch = useDispatch();

    const goToDraw = () => {
        navigate('/draw')
    };




    
    useEffect(() => {
        const url = result[0].image;
        const resultName = result[0].result.prediction;
        setImageUrl(url);
        setname(resultName);
        }, [result]);
    
        
        const handleButtonClick = async () => {
            setLoading(true);
            try {
                // Send POST request to fetch the story
                const storyResponse = await axios.post('http://127.0.0.1:5000/get_story');
        
                // Log the data to inspect its structure
                console.log("Story Response Data:", storyResponse.data);
        
                // Check the structure of the response data
                let storyData = storyResponse.data;
        
                // If the response is a string, try parsing it
                if (typeof storyData === "string") {
                    storyData = JSON.parse(storyData);
                }
        
                let story = '';
        
                // If storyData is an array, join the elements, otherwise treat it as an object or string
                if (Array.isArray(storyData)) {
                    // Concatenate array elements into a single string
                    story = storyData.join(" ");  // Join sentences with a space
                } else if (typeof storyData === 'object') {
                    // If it's an object, concatenate object values (this depends on your data structure)
                    story = Object.values(storyData).join(" ");
                } else if (typeof storyData === 'string') {
                    story = storyData;  // Already a string
                }
        
                // Dispatch actions to clear and update the story in the Redux store
                dispatch({ type: "CLEARSTORY" });
                dispatch({ type: "STORYDATA", payload: { story: story.trim() } }); // trim() removes extra spaces
        
                // Fetch image data associated with the story
                const response = await axios.post('http://127.0.0.1:5000/get_data', {}, { responseType: 'arraybuffer' });
                const blob = new Blob([response.data], { type: 'image/png' });
                const fairytaleImg = URL.createObjectURL(blob);
        
                // Dispatch actions to clear and update the image in the Redux store
                dispatch({ type: "CLEARFAIRYTALE" });
                dispatch({ type: "FAIRYTALE", payload: { fairytaleImg: fairytaleImg } });
                
                // Navigate to the 'fairytale' page
                navigate('/fairytale');
                
            } catch (error) {
                console.error("Error while fetching the story or image:", error);
            } finally {
                setLoading(false); // Turn off the loading indicator
            }
        };
        
        
        
  return (
    <div>{loading ? <Loading /> : null}
    <div className='popup_container'>
        <div className='popup_img_container'>
            <img className='popup_img_bg' src={popupImg} alt='Check the image picture'/>
            <div className='popup_img'>
                {imageUrl ? <img src={imageUrl} alt='picture' /> : null}
            </div>
        </div>
        
        <div className='popup_contents_container'>
            <div className='popup_contents'>
                <div>You drew it! <span>“<strong style={{ fontSize: name.length <= 3 ? "5vw" : "3vw" }}>{ name }</strong>”</span> picture</div>
                <ul>
                    <li>· If you don't like it, you can draw a new one!</li>
                    <li>· <strong>“{name}”</strong> Let's make a fairy tale about it.</li>
                </ul>
            </div>
            <div className='popup_buttons'>
                <button onClick={handleButtonClick}><img src={popupTrue} alt='Pop-up confirm button'></img></button>
                <button onClick={goToDraw}><img src={popupFalse} alt='Pop-up cancel button'></img></button>
            </div>
        </div>
        </div>
    </div>
  )
}

export default Popup