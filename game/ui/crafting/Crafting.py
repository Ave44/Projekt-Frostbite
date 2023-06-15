from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.ui.inventory.Inventory import Inventory
    
from pygame import Surface, Vector2
from pygame.sprite import Sprite

from Config import Config
from constants import SLOT_SIZE, SLOT_GAP, BG_COLOR
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages
from game.ui.crafting.recipes.domain.Recipe import Recipe
from game.ui.crafting.recipes.SwordRecipe import SwordRecipe
from game.ui.crafting.recipes.WoodenArmorRecipe import WoodenArmorRecipe

class Crafting(Sprite):
    def __init__(self, config: Config, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages):
        self.recipesList: list[Recipe] = []
        self.addRecipe(SwordRecipe(visibleSprites, loadedImages))
        self.addRecipe(WoodenArmorRecipe(visibleSprites, loadedImages))

        self.image = Surface(
            [(SLOT_SIZE + SLOT_GAP) + SLOT_GAP,
             len(self.recipesList) * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP])
        self.image.fill(BG_COLOR)

        self.rect = self.image.get_rect()
        self.rect.center = Vector2(SLOT_GAP + SLOT_SIZE / 2, config.WINDOW_HEIGHT / 2)

        for idx, recipe in enumerate(self.recipesList):
            position = Vector2(SLOT_GAP, idx * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP)
            recipe.rect.topleft = self.rect.topleft + position
            recipe.draw(self.image, position)

    def addRecipe(self, recipe: Recipe) -> None:
        self.recipesList.append(recipe)

    def hoverMessage(self, mousePos: Vector2, inventory: Inventory) -> str:
        for recipe in self.recipesList:
            if recipe.rect.collidepoint(mousePos):
                return recipe.hoverMessage(inventory)

    def draw(self, displaySurface: Surface) -> None:
        displaySurface.blit(self.image, self.rect)
