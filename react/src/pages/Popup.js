import React, { useState, useEffect } from 'react';
import axios from "axios";
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import popupImg from '../images/popupImg/popupImg.png';
import popupTrue from '../images/popupImg/popupTrue.png';
import popupFalse from '../images/popupImg/popupFalse.png';

import Loading from '../components/Loading';

const Popup = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const result = useSelector(state => state.result);
    const [imageUrl, setImageUrl] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);

    // Navigate to the drawing page
    const goToDraw = () => {
        navigate('/draw');
    };

    // Handle image and name updates when `result` changes
    useEffect(() => {
        if (result && result.length > 0) {
            const { image, result: { prediction } } = result[0] || {}; // Safely access nested objects
            setImageUrl(image);
            setName(prediction);
        }
    }, [result]);

    // Handle the "Create Story" button click
    const handleButtonClick = async () => {
        setLoading(true);
        try {
            // Send POST request for the story
            const storyResponse = await axios.post('http://127.0.0.1:5000/get_story'); // http://101.101.101.101:80

            let story = "";
            storyResponse.data.forEach((storyPart) => {
                if (storyPart) {
                    story += storyPart;
                }
            });

            // Dispatch story data to Redux
            dispatch({ type: "CLEARSTORY" });
            dispatch({ type: "STORYDATA", payload: { story } });

            // Fetch the image for the fairytale
            const response = await axios.post('http://127.0.0.1:5000/get_data', {}, { responseType: 'arraybuffer' });
            const blob = new Blob([response.data], { type: 'image/png' });
            const fairytaleImg = URL.createObjectURL(blob);

            // Dispatch fairytale image to Redux
            dispatch({ type: "CLEARFAIRYTALE" });
            dispatch({ type: "FAIRYTALE", payload: { fairytaleImg } });

            // Navigate to the fairytale page
            navigate('/fairytale');
        } catch (error) {
            console.error("Error creating story or fetching image:", error);
        } finally {
            setLoading(false); // Turn off loading screen
        }
    };

    return (
        <div>
            {loading && <Loading />}
            <div className='popup_container'>
                <div className='popup_img_container'>
                    <img className='popup_img_bg' src={popupImg} alt='Check the image picture' />
                    <div className='popup_img'>
                        {imageUrl ? <img src={imageUrl} alt='그림' /> : null}
                    </div>
                </div>

                <div className='popup_contents_container'>
                    <div className='popup_contents'>
                        <div>
                        I drew it! <span>“<strong style={{ fontSize: name.length <= 3 ? "5vw" : "3vw" }}>{name}</strong>”</span> 그림
                        </div>
                        <ul>
                            <li>· If you don't like it, you can draw a new one!</li>
                            <li>· <strong>“{name}”</strong>Let's make a fairy tale about.</li>
                        </ul>
                    </div>

                    <div className='popup_buttons'>
                        <button onClick={handleButtonClick}><img src={popupTrue} alt='Pop-up true button' /></button>
                        <button onClick={goToDraw}><img src={popupFalse} alt='Pop-up false button' /></button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Popup;
