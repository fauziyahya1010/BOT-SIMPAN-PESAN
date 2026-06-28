const { Events } = require("discord.js");

const CHANNEL_ID = process.env.CHANNEL_ID;
const OWNER_ID = process.env.OWNER_ID;

const MAX_CODES = 100;

module.exports = (client) => {

    client.on(Events.MessageCreate, async (message) => {

        try {

            if (message.author.bot) return;

            if (OWNER_ID && message.author.id !== OWNER_ID) return;

            if (CHANNEL_ID && message.channel.id !== CHANNEL_ID) return;

            let codes = message.content
                .split(/\r?\n/)
                .map(code => code.trim())
                .filter(code => code.length > 0);

            if (codes.length === 0) return;

            if (codes.length > MAX_CODES) {
                codes = codes.slice(0, MAX_CODES);
            }

            await message.delete().catch(() => {});

            for (const code of codes) {

                await message.channel.send({
                    content: "```\n" + code + "\n```"
                });

                // Delay kecil agar aman dari rate limit Discord
                await new Promise(resolve => setTimeout(resolve, 350));

            }

        } catch (err) {

            console.error(err);

        }

    });

};
