import React,{useState,useEffect} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Route,BrowserRouter as Router, Switch } from 'react-router-dom';
import { Link } from 'react-router-dom/cjs/react-router-dom';

import App from './App';
import * as serviceWorker from './serviceWorker';
const url = 'http://127.0.0.1:8000'
function fileUploader(event){
    if(event.target.file){
      fetch('http://127.0.0.1:8000/createhls',{method:'post',credentials:"omit",mode:'no-cors',body:new FormData(event.target)}).then((event)=>{
        console.log(event.text().then(text=>alert(text)))
      }).catch((error)=>{console.log(error)})
    }
  }
function Home(props){
    const [videos,setVideos] = useState([])
    useEffect(()=>{
        fetch(url).then(res=>{res.json().then(data=>{
            setVideos(JSON.parse(data))
        }).catch(err=>console.log(err))})
        .catch(err=>console.warn(err))
    },[])
    return videos.length>0 ?<><div style={{display:'flex',flexDirection:'row',flexWrap:"wrap"}}>
      {videos.map(video=><Link key={videos.indexOf(video)} to={{pathname:'/playvideo',value:video.fields.url}} className='card' style={{textDecoration:'none'}}>
        <h3>{video.fields.name}</h3>
        <img alt={video.fields.name} src={`${url}/files/${video.fields.poster}`} className='card-img' />
      </Link>)}
    </div>
    <footer id='player-footer' style={{width:'100%',height:'fit-content', bottom:"30%",padding:'10px'}}>
          <p>Select a video from files or enter the video's URL</p>
          <form encType='multipart/form-data' onSubmit={(event)=>{event.preventDefault();fileUploader(event)}} style={{width:"100%",height:"20%", display:'flex'}}>
            <input type='text' placeholder='File name' style={{width:'50%'}} name='name' /><br />
            <select name='type' placeholder='Type '>
              <option defaultValue>DASH</option>
              <option >HLS</option>
            </select>
            <input type="file" name='file'/>
            <input type='submit' value='Upload' />
          </form>
        </footer>
    </>:<p className='App-header' style={{color:'red'}}>Error</p>
}

ReactDOM.render(<Router>
  <Switch>
    <Route exact path='/' component={Home} />
    <Route exact path='/playvideo' component={App} />
    </Switch></Router>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
