from pygame import Surface, Vector2
from pygame.sprite import Sprite

from constants import SLOT_SIZE, SLOT_GAP, BG_COLOR
from game.LoadedImages import LoadedImages
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from recipes.SwordRecipe import SwordRecipe


class Crafting(Sprite):
    def __init__(self, loadedImages: LoadedImages, uiSprites: UiSpriteGroup, center: Vector2):
        super().__init__(uiSprites)
        self.recipesList = [SwordRecipe(loadedImages), SwordRecipe(loadedImages)]
        self.image = Surface(
            [(SLOT_SIZE + SLOT_GAP) + SLOT_GAP,
             len(self.recipesList) * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP])
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = center

        for idx, recipe in enumerate(self.recipesList):
            self.image.blit(recipe.image, (SLOT_GAP, idx * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP))
