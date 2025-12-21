# AlgorithmsView Documentation

`AlgorithmsView` is a custom Discord UI View class designed to display OLL (Orientation of the Last Layer) and PLL (Permutation of the Last Layer) algorithms for Rubik's Cube solvers. It provides an interactive interface with a select menu for choosing algorithm groups where applicable, and pagination controls to navigate through algorithms.

## Class Overview

**File:** `src/algorithms.py`
**Inherits from:** `discord.ui.View`

### Initialization

```python
AlgorithmsView(timeout=180, mode, user_id, userName, initial_group=None)
```

**Parameters:**
- `timeout` (float | None): Time in seconds before the view stops listening to interactions. Default is 180.
- `mode` (str): Operations mode. Accepts `"oll"` or `"pll"`.
- `user_id` (int): Discord ID of the user who triggered the command. Only this user can interact with the view.
- `userName` (str): Username of the user (used for display/logging if needed).
- `initial_group` (str, optional): The name of the algorithm group to load immediately upon initialization.

## Features

1.  **Group Selection**: Users can select different algorithm groups (e.g., "T Shape", "Edges Only") via a Dropdown Menu.
2.  **Pagination**: Displays one algorithm at a time. Users can navigate using **Back** and **Next** buttons.
3.  **Security**: Interactions are restricted to the user who invoked the command.
4.  **Data Loading**: Loads algorithm data from a local `algorithms.json` file.

## Method Reference

### `setup_select_menu()`
Dynamically creates and adds a `discord.ui.Select` menu to the view. The options are populated based on the `mode` (OLL or PLL groups).

### `select_callback(interaction)`
Async callback for the select menu.
- Verifies the user.
- Updates `current_group` based on selection.
- Resets pagination to page 0.
- Triggers `update_view()`.

### `load_group(group_name)`
Loads the list of algorithms for the specified `group_name` into `self.algorithms_list` from the loaded JSON data.
- **Args**: `group_name` (str)

### `get_embed()`
Generates a `discord.Embed` object for the current page.
- **Returns**: `discord.Embed` containing the algorithm title, notation, and footer with page number.

### `update_view(interaction)`
Updates the message with the current embed and button states (enabled/disabled).

### `update_buttons()`
Logic to enable or disable **Back** and **Next** buttons based on the `current_page` index relative to the list length.

### Button Callbacks
- **`back`**: Decrements `current_page`.
- **`next`**: Increments `current_page`.

## Data Structure
The class relies on `src/data/algorithms.json` structured as:
```json
{
  "oll": { "1": "Algorithm...", ... },
  "pll": { "Aa": "Algorithm...", ... }
}
```
Internal dictionaries `self.OLL_GROUPS` and `self.PLL` map group names to lists of algorithm IDs.
