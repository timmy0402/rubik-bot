import time
import logging
import discord

from stats import update_user_pbs
from database import DatabaseManager
from stats.personal_best import calculate_wca_avg, update_user_average_best

logger = logging.getLogger(__name__)


class TimerView(discord.ui.View):
    """
    A discord.ui.View that provides an interactive stopwatch for users to time their cube solves.
    """

    def __init__(
        self,
        *,
        timeout: float | None = 180,
        user_id: int,
        userName: str,
        puzzle: str,
        db_manager: DatabaseManager,
    ):
        """
        Initialize the TimerView.

        Args:
            timeout (float | None): The timeout for the view in seconds.
            user_id (int): The Discord ID of the user who started the timer.
            userName (str): The name of the user.
            puzzle (str): The type of puzzle being timed (e.g., '3x3').
            db_manager: The database manager instance.
        """
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.user_name = userName
        self.puzzle = puzzle
        self.db_manager = db_manager
        self.message = None
        self.start_time = None
        self.end_time = None

        # Check if the user exists in the database, if not create a new entry
        self.db_id = self._get_or_create_user()

    def _get_or_create_user(self) -> int:
        """
        Retrieves the internal UserID from the database, creating a new user record if necessary.

        Returns:
            int: The UserID from the database.
        """
        try:
            # Check for existing user
            self.db_manager.cursor.execute(
                "SELECT UserID FROM Users WHERE DiscordID=?", (self.user_id,)
            )
            db_id = self.db_manager.cursor.fetchval()

            if not db_id:
                # Insert new user if not found
                self.db_manager.cursor.execute(
                    "INSERT INTO Users(UserName, DiscordID) VALUES(?, ?)",
                    (self.user_name, self.user_id),
                )
                self.db_manager.connection.commit()

                # Fetch the newly created UserID
                self.db_manager.cursor.execute(
                    "SELECT UserID FROM Users WHERE DiscordID=?", (self.user_id,)
                )
                db_id = self.db_manager.cursor.fetchval()

            return db_id
        except Exception as e:
            logger.error(f"Error in _get_or_create_user: {e}")
            return None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Ensures that only the user who started the timer can interact with it.

        Args:
            interaction (discord.Interaction): The interaction object.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "You cannot interact with this timer.", ephemeral=True
            )
            return False
        return True

    async def disable_all_items(self):
        """
        Disables all buttons in the view and updates the message if it exists.
        """
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception as e:
                logger.error(f"Error in disable_all_items: {e}")

    async def on_timeout(self) -> None:
        """
        Handles the view timeout by notifying the user and disabling buttons.
        """
        try:
            if self.message:
                # Notify the user about the timeout
                await self.message.channel.send(
                    f"<@{self.user_id}>, your timer session has timed out.",
                    delete_after=10
                )
            await self.disable_all_items()
        except Exception as e:
            logger.error(f"Error handling on_timeout: {e}")

    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start_timer(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        Starts the timer and updates the UI to show timing is in progress.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        self.start_time = time.time()

        # Disable the start button once timing begins
        button.disabled = True

        embed = discord.Embed(
            title="Timer Started!",
            description=f"Currently timing your **{self.puzzle}** solve.\nClick **Stop** when you are finished.",
            color=discord.Color.green(),
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.secondary)
    async def stop_timer(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        Stops the timer, calculates the elapsed time, and saves it to the database.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        if self.start_time is None:
            await interaction.response.send_message(
                "You must start the timer first!", ephemeral=True
            )
            return

        self.end_time = time.time()
        elapsed_time = round(self.end_time - self.start_time, 2)

        # Save the result to the database
        if self.db_id is None:
            logger.error("Cannot save solve time: User database ID is missing.")
            await interaction.response.send_message(
                "An error occurred: Your user record could not be found. Time not saved.",
                ephemeral=True
            )
            return

        try:
            # Save the solve time to the database
            self.db_manager.cursor.execute(
                "INSERT INTO SolveTimes(UserID, SolveTime, PuzzleType) VALUES(?, ?, ?)",
                (self.db_id, elapsed_time, self.puzzle),
            )
            self.db_manager.connection.commit()
            
            # Update the user's personal best if this solve is better
            is_new_pb = update_user_pbs(self.db_manager, self.db_id, self.puzzle, elapsed_time)

            # Fetch last 15 solves for the specific puzzle to calculate averages
            self.db_manager.cursor.execute(
                "SELECT TOP 15 SolveTime FROM SolveTimes WHERE UserID=? AND PuzzleType=? ORDER BY TIMESTAMP DESC, TimeID DESC",
                (self.db_id, self.puzzle)
            )
            rows = self.db_manager.cursor.fetchall()

            raw_times = [float(row[0]) for row in rows]
            ao5 = calculate_wca_avg(raw_times, 5)
            ao12 = calculate_wca_avg(raw_times, 12)
            
            is_new_ao5, is_new_ao12 = update_user_average_best(self.db_manager, self.db_id, self.puzzle, ao5, ao12)

        except Exception as e:
            logger.error(f"Error saving solve time to database: {e}")
            await interaction.response.send_message(
                "Failed to save your time to the database.", ephemeral=True
            )
            return
        
        # Prepare the completion embed
        pb_messages = []
        if is_new_pb:
            pb_messages.append("✨ **New Personal Best Single!**")
        if is_new_ao5:
            pb_messages.append("🎉 **New Personal Best Ao5!**")
        if is_new_ao12:
            pb_messages.append("🎊 **New Personal Best Ao12!**")

        description = f"**{self.user_name}'s {self.puzzle}** time is: **{elapsed_time}s**\n"
        
        if pb_messages:
            description += "\n" + "\n".join(pb_messages) + "\n"
        else:
            description += "Your record has been saved.\n"

        embed = discord.Embed(
            title="Solve Completed!",
            description=description,
            color=discord.Color.gold() if pb_messages else discord.Color.green(),
        )

        if ao5:
            embed.add_field(name="Current Ao5", value=f"{ao5:.2f}s", inline=True)
        if ao12:
            embed.add_field(name="Current Ao12", value=f"{ao12:.2f}s", inline=True)
        
        embed.set_footer(text=f"Puzzle: {self.puzzle}")

        # Disable all buttons upon completion
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Cancels the current timer session.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button that was clicked.
        """
        embed = discord.Embed(
            title="Timer Cancelled",
            description="The timing session was cancelled by the user.",
            color=discord.Color.red()
        )
        
        # Disable all buttons upon cancellation
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()