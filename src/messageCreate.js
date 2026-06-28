const { Events } = require("discord.js");

module.exports = (client) => {

    console.log("messageCreate.js berhasil dimuat");

    client.on(Events.MessageCreate, (message) => {

        console.log("==================================");
        console.log("Pesan diterima");
        console.log("Author :", message.author.tag);
        console.log("User ID:", message.author.id);
        console.log("Channel:", message.channel.id);
        console.log("Isi    :", message.content);
        console.log("==================================");

    });

};
