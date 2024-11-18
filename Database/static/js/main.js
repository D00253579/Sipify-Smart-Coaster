let pubnub;
let appChannel = "Sipify-channel";



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
        handleMessage(messageEvent.message);
    };

    subscription.subscribe();
};

const publishMessage = async (message) => {
    const publishPayload = {
        channel: appChannel,
        message: message,
    };
    await pubnub.publish(publishPayload);
};

function handleMessage(message) {

}