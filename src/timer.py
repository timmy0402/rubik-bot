import time
import discord
from DB_Manager import DatabaseManager

class TimerView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180,user_id,userName):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.userName = userName
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.message = None
        self.db_manager.cursor.execute("SELECT UserID FROM Users WHERE DiscordID=?",(user_id))
        self.DB_ID = self.db_manager.cursor.fetchval()
        if(not self.DB_ID):
            self.db_manager.cursor.execute("INSERT INTO Users(UserName,DiscordID) VALUES(?,?)",(userName,user_id))
            self.db_manager.cursor.commit()
            self.db_manager.cursor.execute("SELECT UserID FROM Users WHERE DiscordID=?",(user_id))
            self.DB_ID = self.db_manager.cursor.fetchval()
        
    startTime = None
    endTime = None
    
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        self.db_manager.close()
        await self.message.channel.send("Timed out")
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
            self.db_manager.cursor.execute('INSERT INTO SolveTimes(UserID,SolveTime) VALUES(?, ?)',(self.DB_ID,elapsedTime))
            self.db_manager.cursor.commit()
            self.db_manager.close()
            self.stop()
    
    @discord.ui.button(label="Cancel", 
                       style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user.id != self.user_id):
            await interaction.response.send_message("You can not interact with this button")
        else:
            await interaction.response.send_message("Cancelling")
            self.db_manager.close()
            self.stop()