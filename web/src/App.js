import React, {useState} from 'react';
import './App.css';
import PlayButton, {PauseButton,FullScreen,Rewind,Forward,Mute,Dash} from './icons.js';


function App(props) {
  const [playState, setPlayState] = useState('paused')
  
  function play(event){
    let player = document.getElementById('video-player')
    props.location.value!==undefined?props.location.value.endsWith('.mpd')?window.playDASH('http://127.0.0.1:8000/files/'+props.location.value):window.playHLS('http://127.0.0.1:8000/files/'+props.location.value):console.log(null)

    player.onplaying=( event)=>{
      setPlayState('playing')
      setInterval(()=>{
        let slideSeek = document.getElementById('slide-seek'),seekTime = document.getElementById('seek-time')
        slideSeek.value = (100/player.duration)*player.currentTime
        seekTime.innerText = `0:00:${player.currentTime.toFixed()}`
      },1000)
    }
    player.onpause=()=>{
      setPlayState('paused')
    }
    playState === 'paused'?player.play():player.pause()
  }
  function seek(event){
    let player = document.getElementById('video-player')
    event.target.id === 'forward-button'? player.currentTime += 10 : player.currentTime -= 10;
  }
  function slideSeek(event){
    let player = document.getElementById('video-player')
    player.currentTime = (event.target.value/100)*player.duration    
  }
  function slideVolume(event){
    let player = document.getElementById('video-player')
    player.volume = event.target.value/100
  }
  function showPlaylist(){

  }
  return (
    <div className="App">
      <header className="video-header App-header">
        <div id='video-container'>
          <video id='video-player' onLoad={()=>play()} style={{height:'50%',width:'100%',position:'relative'}} onClick={play}>
            <source id='video-player-source' autopictureinpiction='true' ></source>
          </video>
          <div style={{position:'absolute',zIndex:'1000',bottom:'0%',width:'100%'}}>
          <p id='seek-time'>0:00:00</p>
            <input type='range' style={{width:"100%"}} id='slide-seek' onChange={slideSeek} defaultValue='0' />
            <div style={{display:'flex',alignItems:'center'}}>
              <button onClick={seek} id='rewind-button' className='btn'><Rewind /></button>
              <button onClick={play} id='play-button' className='btn'>
                {playState === 'paused'?<PlayButton />:<PauseButton />}</button>
              <button onClick={seek} id='forward-button' className='btn' ><Forward /></button>
              <button onClick={()=>document.getElementById('video-player').requestFullscreen()} className='btn' style={{margin:'0px 10px'}}><FullScreen /></button>
              <button className='btn' onClick={showPlaylist} style={{fontWeight:'bolder',color:"white"}}><Dash style={{fill:'white'}} /> Playlist</button>
              <button onClick={()=>document.getElementById('video-player').volume = 0} className='btn'><Mute /></button>
              <input type='range' style={{width:"20%"}} id='slide-volume' onChange={slideVolume} defaultValue='100' />
            </div>
          </div>
          </div>
      </header>
    </div>
  );
}

export default App;
