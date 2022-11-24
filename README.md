# video-chat-django

> This project is based upon WebRTC(Web Real-Time Communications)</br>
> Live, interactive voice and video powered by the only global network dedicated to real-time engagement.</br>

## (Agora Web SDK API Reference)[https://api-ref.agora.io/en/video-sdk/web/4.x/index.html]

### streams.js-

```
const APP_ID = 'YOUR APP ID'
const TOKEN = sessionStorage.getItem('token')
const CHANNEL = sessionStorage.getItem('room')
```

> we are filling them manually, later on we will fill them automatically

-----

1). createClient - 
>> Creates a local client object for managing a call. </br>
>> This is usually the first step of using the Agora Web SDK.</br>
>> The mode and codec properties are required.</br>
</br>
</br>
2). 
store local user audio and video tracks
store remote users audio and video tracks

let localTracks = []
let remoteUsers = []
</br>
</br>

3). 

> each time when a new user joins we make a player for him, we do this dynamically using js

```
let player = `<div  class="video-container" id="user-container-${UID}">
                     <div class="video-player" id="user-${UID}"></div>
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`

    document.getElementById('video-streams').insertAdjacentHTML("beforeend", player)    
```

```
class="video-container"
```

common to all player => will write the css and other stuffs which are common to all players
</br>
</br>
```
id="user-container-${UID}
```
unique for every player 
</br>
</br>


## 4). publish
* Publishes local audio and/or video tracks to a channel.

* After publishing the local tracks, the AgoraRTCClient.on("user-published") callback is triggered on the remote client.
* other users can get these values, so we publish it
* now anybody in the channel can access to these

localTracks[0] -- audio track
localTracks[1] -- video track

* other people to also see it, now anybody in this channel is having access to these values
```
await client.publish([localTracks[0], localTracks[1]])
```

## 5). Adding more users


> when a new user has joined we will call handleUser for him

```
client.on('user-published', ()=>{
console.log("User has joined")
}
)
```
</br>

### when a new user is added -

> take new user audio and video, add it to the DOM </br>

> if mediaType == video </br>
  check is player already exists in DOM or not

> if not exist
 * create a player 
 * add it to the DOM
 * play the video
 * then play audio
-----------------------
Handle left Users

let handleUserLeft = async(user) =>{
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}
------------

 
Adding controls


 <section id="controls-wrapper">
        <div class="icon-wrapper">
            <img class="control-icon" id="mic-btn" src="{% static 'images/microphone.svg' %}" />
        </div>

        <div class="icon-wrapper">
            <img class="control-icon" id="camera-btn" src="{% static 'images/video.svg' %}" />
        </div>

        <div class="icon-wrapper">
            <img class="control-icon" id="leave-btn" src="{% static 'images/leave.svg' %}" />
        </div>
    </section>


redirect user to same page - 
window.open('/', '_self')

-----------------------
till now
we have been working with temporary token, but now we will generate these tokens dynamically

we want our users to crate their own channel and join different channels as they are free to navigate through our site

we handle this using backend-
we gonna have a view and an endpoint

 we will use a package and whenever user enter app_id, channel => a token is automatically generated for him
[agora token builder](https://pypi.org/project/agora-token-builder/)
