"""#HierarchyCraft environement examples.

Here is the table of available HierarchyCraft environments examples.

If you built one of your own, send us a pull request so we can add it to the list!

| Gym name                           | CLI name          | Reference                       |
|:-----------------------------------|:------------------|:--------------------------------|
| "MineHcraft-v1"                    | `minecraft`       | `hcraft.examples.minecraft`     |
| "MiniHCraftEmpty-v1"               | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftFourRooms-v1"           | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftMultiRoom-v1"           | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftCrossing-v1"            | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftKeyCorridor-v1"         | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftDoorKey-v1"             | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftUnlock-v1"              | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftUnlockPickup-v1"        | `minicraft`       | `hcraft.examples.minicraft`     |
| "MiniHCraftBlockedUnlockPickup-v1" | `minicraft`       | `hcraft.examples.minicraft`     |
| "TowerHcraft-v1"                   | `tower`           | `hcraft.examples.tower`         |
| "RecursiveHcraft-v1"               | `recursive`       | `hcraft.examples.recursive`     |
| "LightRecursiveHcraft-v1"          | `light-recursive` | `hcraft.examples.recursive`     |
| "Treasure-v1"                      | `treasure`        | `hcraft.examples.treasure`      |
| "RandomHcraft-v1"                  | `random`          | `hcraft.examples.random_simple` |


"""

import hcraft.examples.minecraft as minecraft
import hcraft.examples.minicraft as minicraft
import hcraft.examples.random_simple as random_simple
import hcraft.examples.recursive as recursive
import hcraft.examples.tower as tower
import hcraft.examples.treasure as treasure

from hcraft.examples.minecraft import MineHcraftEnv, MINEHCRAFT_GYM_ENVS
from hcraft.examples.random_simple import RandomHcraftEnv
from hcraft.examples.recursive import LightRecursiveHcraftEnv, RecursiveHcraftEnv
from hcraft.examples.tower import TowerHcraftEnv
from hcraft.examples.treasure import TreasureEnv
from hcraft.examples.minicraft import MINICRAFT_ENVS, MINICRAFT_GYM_ENVS

EXAMPLE_ENVS = [
    MineHcraftEnv,
    *MINICRAFT_ENVS,
    TowerHcraftEnv,
    RecursiveHcraftEnv,
    LightRecursiveHcraftEnv,
    TreasureEnv,
    # RandomHcraftEnv,
]

HCRAFT_GYM_ENVS = [
    *MINEHCRAFT_GYM_ENVS,
    *MINICRAFT_GYM_ENVS,
    "TowerHcraft-v1",
    "RecursiveHcraft-v1",
    "LightRecursiveHcraft-v1",
    "Treasure-v1",
]


__all__ = [
    "minecraft",
    "minicraft",
    "recursive",
    "tower",
    "treasure",
    "random_simple",
    "MineHcraftEnv",
    "RandomHcraftEnv",
    "LightRecursiveHcraftEnv",
    "RecursiveHcraftEnv",
    "TowerHcraftEnv",
]
