import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.chatbot import HuggingFaceChatbot
except ImportError:
    from chatbot import HuggingFaceChatbot

# Load environment variables
load_dotenv()

class DiscordChatBot(commands.Bot):
    def __init__(self):
        # Set up intents (permissions for the bot)
        intents = discord.Intents.default()
        intents.message_content = True  # Required to read message content
        intents.messages = True
        intents.guilds = True

        super().__init__(command_prefix='!', intents=intents)

        # Initialize HuggingFace chatbot
        model_name = os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen2.5-72B-Instruct")
        self.chatbot = HuggingFaceChatbot(model_name=model_name)

        # Store conversation history per channel
        self.conversations = {}

    async def on_ready(self):
        """Called when the bot is ready and connected to Discord"""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="mentions | @me to chat"
            )
        )

    async def on_message(self, message):
        """Called when a message is sent in a channel the bot can see"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Check if bot was mentioned
        if self.user.mentioned_in(message):
            # Remove the bot mention from the message
            content = message.content.replace(f'<@{self.user.id}>', '').strip()
            content = content.replace(f'<@!{self.user.id}>', '').strip()

            if not content:
                await message.channel.send("Chào bạn! Mention mình và gửi tin nhắn để chat nhé!")
                return

            # Show typing indicator
            async with message.channel.typing():
                # Get or create conversation history for this channel
                channel_id = message.channel.id
                if channel_id not in self.conversations:
                    self.conversations[channel_id] = HuggingFaceChatbot(
                        model_name=os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen2.5-72B-Instruct")
                    )

                # Get response from chatbot
                response = self.conversations[channel_id].chat(content)

                # Send response (split if too long)
                if len(response) > 2000:
                    # Discord has a 2000 character limit
                    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(response)

        # Process commands (if you want to add custom commands)
        await self.process_commands(message)

# Create bot commands
bot = DiscordChatBot()

@bot.command(name='reset')
async def reset_conversation(ctx):
    """Reset the conversation history for this channel"""
    channel_id = ctx.channel.id
    if channel_id in bot.conversations:
        bot.conversations[channel_id].reset_conversation()
        await ctx.send("Đã reset lịch sử hội thoại cho channel này!")
    else:
        await ctx.send("Chưa có lịch sử hội thoại nào để reset!")

@bot.command(name='ping')
async def ping(ctx):
    """Check if the bot is responsive"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command(name='help_bot')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="Discord AI Chatbot Help",
        description="Hướng dẫn sử dụng bot",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Chat với bot",
        value="Mention bot (@bot_name) và gửi tin nhắn của bạn",
        inline=False
    )
    embed.add_field(
        name="!reset",
        value="Reset lịch sử hội thoại trong channel này",
        inline=False
    )
    embed.add_field(
        name="!ping",
        value="Kiểm tra bot có hoạt động không",
        inline=False
    )
    embed.add_field(
        name="!help_bot",
        value="Hiển thị thông tin trợ giúp này",
        inline=False
    )
    await ctx.send(embed=embed)

def main():
    """Main function to run the bot"""
    # Get Discord token from environment variable
    discord_token = os.getenv("DISCORD_BOT_TOKEN")

    if not discord_token:
        print("ERROR: DISCORD_BOT_TOKEN not found in environment variables!")
        print("Please create a .env file and add your Discord bot token:")
        print("DISCORD_BOT_TOKEN=your_token_here")
        return

    # Run the bot
    try:
        bot.run(discord_token)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
