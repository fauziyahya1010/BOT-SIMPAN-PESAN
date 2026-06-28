const {
    Client,
    GatewayIntentBits,
    Partials,
    Events
} = require("discord.js");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ],
    partials: [
        Partials.Channel
    ]
});

// ==============================
// Railway Variables
// ==============================

const TOKEN = process.env.DISCORD_TOKEN;

if (!TOKEN) {
    console.error("ERROR: Railway Variable 'DISCORD_TOKEN' tidak ditemukan.");
    process.exit(1);
}

// ==============================
// Bot Ready
// ==============================

client.once(Events.ClientReady, () => {

    console.clear();

    console.log("===========================================");
    console.log("      Discord Auto Code Bot");
    console.log("===========================================");
    console.log(`Bot     : ${client.user.tag}`);
    console.log(`Bot ID  : ${client.user.id}`);
    console.log("Status  : ONLINE");
    console.log("===========================================");

});

// ==============================
// Load Events
// ==============================

require("./messageCreate")(client);

// ==============================

client.login(TOKEN);
