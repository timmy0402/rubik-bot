import discord
import json
import os


class AlgorithmsView(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        mode,
        user_id,
        userName,
        initial_group=None,
    ):
        """
        Initialize the AlgorithmsView.

        Args:
            timeout (float | None): The timeout for the view in seconds.
            mode (str): The mode of the view ('oll' or 'pll').
            user_id (int): The ID of the user who initiated the command.
            userName (str): The name of the user.
            initial_group (str, optional): The initial group to display. Defaults to None.
        """
        super().__init__(timeout=timeout)
        self.mode = mode
        self.user_id = user_id
        self.userName = userName
        self.current_page = 0
        self.algorithms_list = []  # List of tuples (id, alg_string)
        self.current_group = initial_group

        self.OLL_GROUPS = {
            "Awkward Shape": ["29", "30", "41", "42"],
            "Big Lightning Bolt": ["39", "40"],
            "C Shape": ["34", "46"],
            "Corners Oriented": ["28", "57"],
            "Cross": ["21", "22", "23", "24", "25", "26", "27"],
            "Dot": ["1", "2", "3", "4", "17", "18", "19", "20"],
            "Fish Shape": ["9", "10", "35", "37"],
            "I Shape": ["51", "52", "55", "56"],
            "P Shape": ["31", "32", "43", "44"],
            "Small L Shape": ["47", "48", "49", "50", "53", "54"],
            "Small Lightning Bolt": ["7", "8", "11", "12"],
            "W Shape": ["36", "38"],
            "T Shape": ["33", "45"],
        }
        self.PLL_GROUPS = {
            "Adjacent Corner Swap": [
                "Aa",
                "Ab",
                "F",
                "Ga",
                "Gb",
                "Gc",
                "Gd",
                "Ja",
                "Jb",
                "Ra",
                "Rb",
                "T",
            ],
            "Diagonal Corner Swap": ["E", "Na", "Nb", "V", "Y"],
            "Edges Only": ["H", "Ua", "Ub", "Z"],
        }

        # Load data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "data", "algorithms.json")

        try:
            with open(json_path, "r") as f:
                self.alg_data = json.load(f)
        except FileNotFoundError:
            # Fallback if running from root
            json_path = os.path.join("src", "data", "algorithms.json")
            try:
                with open(json_path, "r") as f:
                    self.alg_data = json.load(f)
            except Exception as e:
                print(f"Error loading algo json: {e}")
                self.alg_data = {}
                return

        # Setup Select Menu
        self.setup_select_menu()

        # If an initial group is provided, load it
        if self.current_group:
            self.load_group(self.current_group)

    def setup_select_menu(self):
        """
        Dynamically sets up the select menu options based on the mode (OLL or PLL).
        """
        options = []
        groups = self.OLL_GROUPS if self.mode == "oll" else self.PLL_GROUPS

        # Sort keys for consistent order
        sorted_groups = sorted(groups.keys())

        for group in sorted_groups:
            options.append(discord.SelectOption(label=group, value=group))

        # Create the Select item
        select = discord.ui.Select(
            placeholder="Choose a group...",
            min_values=1,
            max_values=1,
            options=options,
            row=0,
        )
        # Set the callback function for the select menu
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        """
        Callback for the select menu. Updates the current group and page based on selection.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This view is not for you.", ephemeral=True
            )
            return
        # Get the selected group from the interaction data
        selected_group = interaction.data["values"][0]
        self.load_group(selected_group)
        self.current_group = selected_group

        # Update view
        await self.update_view(interaction)

    def load_group(self, group_name):
        """
        Loads the algorithms for the specified group into algorithms_list.

        Args:
            group_name (str): The name of the group to load.
        """
        groups = self.OLL_GROUPS if self.mode == "oll" else self.PLL_GROUPS
        data_key = self.mode

        if group_name not in groups:
            self.algorithms_list = []
            return

        # Get the algorithm IDs for the selected group
        alg_ids = groups[group_name]
        # Get the full algorithm data
        full_data = self.alg_data.get(data_key, {})

        # Load the algorithms into algorithms_list
        self.algorithms_list = []
        for alg_id in alg_ids:
            alg_str = full_data.get(alg_id, "Not found")
            self.algorithms_list.append((alg_id, alg_str))

        self.current_page = 0

    def get_embed(self):
        """
        Generates the embed for the current algorithm page.

        Returns:
            discord.Embed: The embed to display.
        """
        if not self.algorithms_list:
            return discord.Embed(
                title="No algorithms selected",
                description="Please select a group from the menu.",
                color=discord.Color.red(),
            )

        alg_id, alg_str = self.algorithms_list[self.current_page]
        title_prefix = "OLL" if self.mode == "oll" else "PLL"

        embed = discord.Embed(
            title=f"{title_prefix} Algorithms: {self.current_group}",
            color=(
                discord.Color.yellow() if self.mode == "oll" else discord.Color.green()
            ),
        )
        embed.add_field(name=f"{title_prefix} {alg_id}", value=alg_str, inline=False)
        embed.set_footer(
            text=f"Algorithm {self.current_page + 1}/{len(self.algorithms_list)}"
        )
        return embed

    async def update_view(self, interaction: discord.Interaction):
        """
        Updates the view with the current embed and button states.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        self.update_buttons()
        embed = self.get_embed()
        if interaction.response.is_done():
            await interaction.edit_original_response(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        """
        Updates the enabled/disabled state of the Back and Next buttons based on current page.
        """
        # Let's dynamically find them to be safe
        back_button = [
            x
            for x in self.children
            if isinstance(x, discord.ui.Button) and x.label == "Back"
        ][0]
        next_button = [
            x
            for x in self.children
            if isinstance(x, discord.ui.Button) and x.label == "Next"
        ][0]

        if not self.algorithms_list:
            back_button.disabled = True
            next_button.disabled = True
        else:
            back_button.disabled = self.current_page == 0
            next_button.disabled = self.current_page == len(self.algorithms_list) - 1

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Callback for the Back button. Moves to the previous page.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button object.
        """
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This view is not for you.", ephemeral=True
            )
            return

        if self.current_page > 0:
            self.current_page -= 1
            await self.update_view(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, row=1)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Callback for the Next button. Moves to the next page.

        Args:
            interaction (discord.Interaction): The interaction object.
            button (discord.ui.Button): The button object.
        """
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This view is not for you.", ephemeral=True
            )
            return

        if self.current_page < len(self.algorithms_list) - 1:
            self.current_page += 1
            await self.update_view(interaction)
        else:
            await interaction.response.defer()
