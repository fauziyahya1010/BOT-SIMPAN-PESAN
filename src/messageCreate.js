const { Events } = require("discord.js");

module.exports = (client) => {

    client.on(Events.MessageCreate, async (message) => {

        console.log(
            "Pesan diterima:",
            message.author.tag,
            message.author.id,
            message.channel.id,
            message.content
        );

    });

};
