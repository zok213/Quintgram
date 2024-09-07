import React, { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom'
import axios from "axios"; // Modules in code that make requests to flask
import { useDispatch } from "react-redux";


// Get an image
import drawimg from '../images/drawImg/draw_button.png'
import eraser from '../images/drawImg/eraser_button.png'
import clear from '../images/drawImg/clear_button.png'
import post from '../images/drawImg/post_button.png'
import sketchBook from '../images/drawImg/sketchbook.png'


const Draw = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const canvasRef = useRef(null);
  const [getCtx, setGetCtx] = useState(null);
  const [painting, setPainting] = useState(false);
  const [tool, setTool] = useState("pen");

   // End: Specifying Variables----------------------------------------------------------------------------




   useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = window.innerWidth * 0.589;
    canvas.height = window.innerHeight * 0.59;
    const ctx = canvas.getContext("2d");
    const size = Math.min(canvas.width, canvas.height) / 20; // Calculating pointer size
    ctx.lineWidth = size; // Pointer size
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000000"; // Colors when drawing
    setGetCtx(ctx);
  }, [canvasRef]);
  
  const clearCanvas = () => {
    if (!canvasRef.current) return; // Terminate function when canvasRef is null
    const ctx = canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  };
  // End: clearCanvas----------------------------------------------------------------------------


  const handleTouchStart = e => { // When an event called touch occurs, it recognizes the coordinates of the touch and draws a picture in the recognized place.
    const mouseX = e.touches[0].clientX - canvasRef.current.offsetLeft; // When the touch event occurs, the coordinate value X
    const mouseY = e.touches[0].clientY - canvasRef.current.offsetTop;  // When the touch event occurs, the coordinate value Y
    setPainting(true); // The code that tells you that drawing has started
    draw(mouseX, mouseY); // Now that we've started, call the code draw function to draw
  };
  // End: handleTouchStart----------------------------------------------------------------------------
  

  const handleTouchEnd = e => { // When the touch event ends, change the value of the painting state variable to false, and set the path to the currently drawing picture.
    setPainting(false); // Code to indicate that drawing has ended
    getCtx.closePath(); // The method closes the path by concatenating the first and last points of the current path. At this point, no line is drawn between the last point and the first point. Therefore, this method closes the path and uses it to draw the finished shape.
  };
  // End: handleTouchEnd----------------------------------------------------------------------------


  const handleTouchMove = e => {// When the touch event ends, change the value of the painting state variable to false, and set the path to the currently drawing picture.
    e.preventDefault(); // Prevent other events from occurring
    const mouseX = e.touches[0].clientX - canvasRef.current.offsetLeft; // When the touch event occurs, the coordinate value X
    const mouseY = e.touches[0].clientY - canvasRef.current.offsetTop;  // When the touch event occurs, the coordinate value Y
    draw(mouseX, mouseY); // Now that we've started, call the code draw function to draw
  };
  // End: handleTouchMove----------------------------------------------------------------------------


  
  const draw = async (x, y, isEnd = false) => { // If the code tool is pen, the picture is drawn, and if the eraser is eraser, the picture is erased.
    if (!painting) {
      getCtx.beginPath();
      getCtx.moveTo(x, y);
    } else {
      if (tool === "pen") {
        getCtx.lineTo(x, y);
        getCtx.stroke();
      } else if (tool === "eraser") {
        getCtx.globalCompositeOperation = "destination-out";//The part I touch doesn't come out with color, but erases it
        getCtx.lineWidth = Math.min(canvasRef.current.width, canvasRef.current.height) / 20; // Eraser size
        getCtx.lineTo(x, y);
        getCtx.stroke();
        getCtx.globalCompositeOperation = "source-over";
      }
    }
  };
  // End: draw----------------------------------------------------------------------------


  
  const drawFn = e => { // Functions that are called when a mouse event occurs, you have to think differently about mouse and touch.
    const mouseX = e.nativeEvent.offsetX; //Mouse Position X
    const mouseY = e.nativeEvent.offsetY; //Mouse Position Y
    if (!painting) {
      getCtx.beginPath();
      getCtx.moveTo(mouseX, mouseY);
    } else {
      draw(mouseX, mouseY);
    }
  };
  // End: drawFn----------------------------------------------------------------------------

  const getDrawArea = (canvas) => {
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const imageData = ctx.getImageData(0, 0, w, h);
    const pixels = imageData.data;
    let minX = w, minY = h, maxX = 0, maxY = 0;
  
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const pixelIndex = (y * w + x) * 4;
        if (pixels[pixelIndex + 3] > 0) {
          minX = Math.min(minX, x);
          minY = Math.min(minY, y);
          maxX = Math.max(maxX, x);
          maxY = Math.max(maxY, y);
        }
      }
    }
    
    const padding =40;
    return [
      Math.max(0, minX - padding),
      Math.max(0, minY - padding),
      Math.min(w, maxX + padding) - Math.max(0, minX - padding),
      Math.min(h, maxY + padding) - Math.max(0, minY - padding),
    ];
  };
  
  // End: getDrawArea ----------------------------------------------------------------------------


  const handleClick = async () => { //These are the codes that occur when you press the POST button.
    // Create a new canvas that is the same size as the canvas. Code to put in the new canvas to improve image recognition
    const canvas = canvasRef.current;
    const [x, y, w, h] = getDrawArea(canvas);
    const canvasResized = document.createElement("canvas");
    canvasResized.width = w;
    canvasResized.height = h;
    const context = canvasResized.getContext("2d"); 
    
    // Take the drawn area from the original canvas and draw it on the new canvas.
    context.drawImage(canvas, x, y, w, h, 0, 0, w, h);

    // Start the code that sends the image data to the flask -------------------
    // Extract the new canvas image data as a base64 string.
    const imageData = canvasResized.toDataURL("image/png", { colorSpaceConversion: "none" });
    const blob = await new Promise(resolve => canvasResized.toBlob(resolve, 'image/png'));
    const imageUrl = URL.createObjectURL(blob);
    // Generate HTTP POST request data.
    const data = { "image": imageData };
    const response = await axios.post('http://127.0.0.1:5000/post_data', data); // http://101.101.101.101:80


    dispatch({ type: "CLEARRESULT" });
    dispatch({type:"IMAGEDATA",payload:{image:imageUrl,result:response.data}})
    navigate('/popup')
    clearCanvas();
  };
  // End: handleClick----------------------------------------------------------------------------
  






        
  return (
    <div className='draw_container'>
      <ul className='buttons'>
          <li><button className='draw_button' onClick={() => setTool("pen")}><img src={drawimg} alt='Pencil button'/></button></li>
          <li><button className='eraser_button' onClick={() => setTool("eraser")}><img src={eraser} alt='Eraser button'/></button></li>
          <li><button className='clear_button' onClick={clearCanvas}><img src={clear} alt='Trashcan button'/></button></li>
          <li><button className='post_button' onClick={handleClick}><img src={post} alt='Button to check what the drawn image is'/></button></li>
      </ul>
      <div className='canvas_wrap'>
        <img className='sketch' src={sketchBook} alt='Sketchbook image'></img>
        <canvas
          className="canvas"
          ref={canvasRef}
          onMouseDown={() => setPainting(true)}
          onMouseUp={() => setPainting(false)}
          onMouseMove={e => drawFn(e)}
          onMouseLeave={() => setPainting(false)} // Add an onMouseLeave event
          
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
          onTouchMove={handleTouchMove}
        >
        </canvas>
      </div>
    </div>
  )
}


export default Draw
