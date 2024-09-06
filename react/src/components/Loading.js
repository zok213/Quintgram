import React from 'react';
import {Background, LoadingText} from './Styles';
import Spinner from "../images/loadingImg/Double Ring-1s-200px.gif";

export default () => {
  return (
    <Background>
      <div width="5%"><img src={Spinner} alt="Loading" /></div>
      <LoadingText>Waiting...</LoadingText>
    </Background>
  );
};
