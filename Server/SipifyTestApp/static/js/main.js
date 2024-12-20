let aliveSecond = 0;
let heartBeatRate = 5000;
let pubnub;
let appChannel = "Sipify-channel";


function time() {
    let d = new Date();
    let currentSecond = d.getTime();
    if (currentSecond - aliveSecond > heartBeatRate + 1000) {
        document.getElementById("connection_id").innerHTML = "DEAD";
    }
    else {
        document.getElementById("connection_id").innerHTML = "ALIVE";
    }
    setTimeout('time()', 1000);
}

function keepAlive() {
    fetch('/keep_alive')
        .then(response => {
            if (response.ok) {
                let date = new Date();
                aliveSecond = date.getTime();
                return response.json();
            }
            throw new Error("Server offline");
        })
        .catch(error => console.log(error));
    setTimeout('keepAlive()', heartBeatRate);
}


const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'pub-c-8777a30b-5dcb-4cb3-8f28-14b9224c5671',
        subscribeKey: 'sub-c-c0a95f25-6142-4c5a-b5aa-735d9661bcae',
        userId: "Sipify",
    });
    //create a channel
    const channel = pubnub.channel(appChannel);
    //create a subscription
    const subscription = channel.subscription();

    pubnub.addListener({
        status: (s) => {
            console.log('Status', s.category);
            console.log("Connected to pubnub")
        },
    });

    subscription.onMessage = (messageEvent) => {
        console.log("Message: " + messageEvent)
        handleMessage(messageEvent.message);
    };

    subscription.subscribe();
    console.log("Message: " + messageEvent)

};

const publishMessage = async (message) => {
    const publishPayload = {
        channel: appChannel,
        message: message,
    };
    await pubnub.publish(publishPayload);
};

function handleMessage(message) {
    console.log("Message: " + message)
    if (message == "Cup detected") {
        document.getElementById("motion_id").innerHTML = "There is coffee there";
    }
    if (message == "No cup detected") {
        document.getElementById("motion_id").innerHTML = "No coffee present";
    }
    if (message == "Red LED Activated") {
        document.getElementById("led_id").innerHTML = "Red LED Activated";
    }
    if (message == "Blue LED Activated") {
        document.getElementById("led_id").innerHTML = "Blue LED Activated";
    }
    if (message == "Green LED Activated") {
        document.getElementById("led_id").innerHTML = "Green LED Activated";
    }
    if (message == "LED deactivated") {
        document.getElementById("led_id").innerHTML = "Deactivated";
    }
}