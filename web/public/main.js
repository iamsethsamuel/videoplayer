
window.playHLS = ()=>{
    let player = document.getElementById('video-player')
    if(window.Hls.isSupported){
        let hls = new window.Hls()
        hls.loadSource("http://127.0.0.1:8000/files/A.Million.Little.Things.S02E10.HDTV.x264-SVA[eztv].mkv.m3u8")
        hls.attachMedia(player)
        hls.on(window.Hls.Events.MANIFEST_PARSED,function() {
            player.play();
        }) 
    }
}

window.playDASH = function(url){
    initApp(url)
  }

  function initApp(url){
    window.shaka.polyfill.installAll()
    if(window.shaka.Player.isBrowserSupported()){
        initPlayer(url)
    }else{
        alert("Browser Not supported")
    }

  }
  function initPlayer(url){
    let video = document.getElementById('video-player'),player = new window.shaka.Player(video)
    window.player =  player;
    player.addEventListener('error',event=>console.warn(event))
    player.load(url).then(()=>{video.play();console.log("Playing video");}).catch((event)=>console.warn(video))
  }