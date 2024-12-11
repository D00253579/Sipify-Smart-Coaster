let pubnub;
let appChannel1 = "Sipify-channel";
let appChannel2 = "Get-notification"

function hideTemp() {
    document.getElementById("current_temperature").style.display = "none"
}
function hideData() {

    document.getElementById("no_coffee_data").style.display = "none";
    document.getElementById("show_coffee_data").style.display = "block";
    console.log("VALUE: " + document.getElementById("tempNotification").innerHTML)
    sendNotification(document.getElementById("tempNotification").innerHTML)
};

const setupPubNub = () => {
    console.log("Setting up pubnub")
    pubnub = new PubNub({
        publishKey: 'pub-c-8777a30b-5dcb-4cb3-8f28-14b9224c5671',
        subscribeKey: 'sub-c-c0a95f25-6142-4c5a-b5aa-735d9661bcae',
        userId: "Sipify",
    });
    //create a channel
    const channel1 = pubnub.channel(appChannel1);
    const channel2 = pubnub.channel(appChannel2);
    //create a subscription
    const subscription1 = channel1.subscription();
    const subscription2 = channel2.subscription();

    pubnub.addListener({
        status: (s) => {
            console.log('Status', s.category);
            console.log("Connected to pubnub")
        },
    });

    subscription1.onMessage = (messageEvent) => {
        console.log("MessageEvent: " + messageEvent)
        handleMessage(messageEvent.message);
    };

    subscription1.subscribe();

    subscription2.onMessage = (messageEvent) => {
        console.log("MessageEvent: " + messageEvent)
        handleMessage(messageEvent.message);
    };

    subscription2.subscribe();


    hideData();
};
const publishMessage1 = async (message) => {
    const publishPayload1 = {
        channel: appChannel1,
        message: message,
    };
    await pubnub.publish(publishPayload1);
};
const publishMessage2 = async (message) => {
    const publishPayload2 = {
        channel: appChannel2,
        message: message,
    };
    await pubnub.publish(publishPayload2);
};


function handleMessage(message) {
    console.log('Message: ' + message);
    if (parseInt(message) > 3) {
        console.log("MESSAGE FROM PUBNUB: ", message)
        document.getElementById("current_temperature").value = message
        publishMessage1(message)
        // sendNotification(message)
    }
    else if (message == "Cup detected") {
        document.getElementById("show_coffee_data").style.display = "block";
        document.getElementById("no_coffee_data").style.display = "none";
    }
    else if (message == "No cup detected") {
        document.getElementById("no_coffee_data").style.display = "block";
        document.getElementById("show_coffee_data").style.display = "none";
    }

};
function sendNotification(notification) {
    publishMessage2(notification)
};