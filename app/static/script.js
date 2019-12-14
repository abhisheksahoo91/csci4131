"use strict";

function myOnload() {
    
    function onPlayerLoaded() {
        /*
        console.log('Inside onPlayerLoaded')
        var myFavTracks = [698905582, 744266592, 447098092, 710164312, 771196602];
        DZ.player.playTracks(myFavTracks);
        DZ.player.play();
        */
    }

    console.log('Inside myOnload()')
    DZ.init({
        appId: '8',
        channelUrl: 'http://developers.deezer.com/examples/channel.php',
        player: {
            container: 'player',
            cover: true,
            playlist: false,
            height: 100,
            layout: "dark",
            onload: onPlayerLoaded
        }
    });
}

function playSongs(divId) {
    console.log(divId)
    let divIds = divId.split('_')
    let type = divIds[0]
    let id = divIds[1]
    if (type == 'album') {
        console.log('Playing album : ' + id)
        DZ.player.playAlbum(id)
    } else if (type == 'artist') {
        
    } else if (type == 'playlist') {
        console.log('Playing playlist : ' + id)
        DZ.player.playPlaylist(id)
    } else if (type == 'track') {
        console.log('Playing track : ' + id)
        DZ.player.playTracks([id])
    }
}
