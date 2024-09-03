import time
import discord

class TimerView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.startTime = None
        self.endTime = None
    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async startTimer(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.startTime = time.time()
        await interaction.response.send_message("Stopwatch started!", ephemeral=True)
