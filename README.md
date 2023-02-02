# video-chat-django
(Code)[https://github.com/anupriya567/video-chat-django]

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

### 1). createClient - 
>> Creates a local client object for managing a call. </br>
>> This is usually the first step of using the Agora Web SDK.</br>
>> The mode and codec properties are required.</br>
```
const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})'
```
</br>

### 2). 
* store local user audio and video tracks
* store remote users audio and video tracks
```
let localTracks = []
let remoteUsers = []
```
</br>
</br>

### 3). 

> each time when a new user joins we make a player for him, we do this dynamically using js

```
let player = `<div  class="video-container" id="user-container-${UID}">
                     <div class="video-player" id="user-${UID}"></div>
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`

    document.getElementById('video-streams').insertAdjacentHTML("beforeend", player)    
```
</br>
</br>


## 4). publish
* Publishes local audio and/or video tracks to a channel.

* After publishing the local tracks, the AgoraRTCClient.on("user-published") callback is triggered on the remote client.
* other users can get these values, so we publish it
* now anybody in the channel can access to these

>> localTracks[0] -- audio track
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
```
let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }

        let member = await getMember(user)

        player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="video-player" id="user-${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
        </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio'){
        user.audioTrack.play()
    }
}
```
### 6). Handle left Users

```
let handleUserLeft = async(user) =>{
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}
```

### 7). Adding controls

```
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
```

>>> redirect user to same page - 
    window.open('/', '_self')

### What's next=>
* till now we have been working with temporary token, but now we will generate these tokens dynamically

* we want our users to crate their own channel and join different channels as they are free to navigate through our site

* we handle this using backend-
* we gonna have a view and an endpoint

 * we will use a package and whenever user enter app_id, channel => a token is automatically generated for him
[agora token builder](https://pypi.org/project/agora-token-builder/)



### 8). get_or_create()
(QuerySet API reference)[https://docs.djangoproject.com/en/4.1/ref/models/querysets/]


> Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.</br>
> This is meant to prevent duplicate objects from being created when requests are made in parallel, and as a shortcut to boilerplatish code. For example:

```
try:
    obj = Person.objects.get(first_name='John', last_name='Lennon')
except Person.DoesNotExist:
    obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
    obj.save()
```   
    
> Here, with concurrent requests, multiple attempts to save a Person with the same parameters may be made. To avoid this race condition, the above example can be rewritten using get_or_create() like so:
```
obj, created = Person.objects.get_or_create(
    first_name='John',
    last_name='Lennon',
    defaults={'birthday': date(1940, 10, 9)},
)
```
### 9). Storing Member in Database 

> (making post request using fetch api js)
```
let createMember = async () => {
    let response = await fetch('/create_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
    return member
}
```
</br>
--> views.py

> as we are sending data through post request, we have to use csrf_token but we have'nt used so using  @csrf_exempt

```
@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)

```

> (making get request)

```
let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}
```

```
def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)
```

### Let's how video-chat is working

>> User ROHIT has entered the room = MAIN

![Screenshot (20) (1)](https://user-images.githubusercontent.com/72871727/205432856-e2c67b07-e7dd-4fad-bc2b-a860d7b86014.jpg)
</br>


![Screenshot (21)](https://user-images.githubusercontent.com/72871727/205432940-80f05409-9252-4894-b502-0a41e8ab99e9.jpg)
</br>
</br>
>> Other user RIYA has entered same room MAIN

![Screenshot (24)](https://user-images.githubusercontent.com/72871727/205433024-03c57931-bec8-4b55-8862-4f6bfded1da5.jpg)

</br>

![Screenshot (22)](https://user-images.githubusercontent.com/72871727/205432937-c89c08da-2890-4189-8ed1-b2345223e34d.jpg)
</br>
</br>
>> Other user RAHUL has entered

![Screenshot (25)](https://user-images.githubusercontent.com/72871727/205433022-fed343fd-e10f-4183-b5b2-393b84851f93.jpg)
</br>

![Screenshot (23)](https://user-images.githubusercontent.com/72871727/205432941-eb99428a-2998-4e48-839f-5c686cf7bed3.jpg)

