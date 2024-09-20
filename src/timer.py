import time
import discord

class TimerView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180,user_id):
        super().__init__(timeout=timeout)
        self.user_id = user_id
    startTime = None
    endTime = None
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view = self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("Timedout")
        await self.disable_all_items()

    @discord.ui.button(label="Start", 
                       style=discord.ButtonStyle.success)
    async def startTimer(self,interaction : discord.Interaction, button: discord.ui.Button):
        if(interaction.user.id != self.user_id):
            await interaction.response.send_message("You can not interact with this button")
        else:
            await interaction.response.send_message("Time started!")
            self.startTime = time.time()
    
    @discord.ui.button(label="Stop",
                       style=discord.ButtonStyle.secondary)
    async def stopTime(self,interaction : discord.Interaction, button:discord.ui.Button):
        if(interaction.user.id != self.user_id):
            await interaction.response.send_message("You can not interact with this button")
        else:
            self.endTime = time.time()
            elapsedTime = self.endTime - self.startTime
            elapsedTime = round(elapsedTime,2)
            await interaction.response.send_message("Your time is: " + str(elapsedTime))
            self.stop()
    
    @discord.ui.button(label="Cancel", 
                       style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user.id != self.user_id):
            await interaction.response.send_message("You can not interact with this button")
        else:
            await interaction.response.send_message("Cancelling")
            self.stop()