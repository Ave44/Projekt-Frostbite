from pygame import Vector2, Rect
from pygame.time import Clock

from game.entities.domain.Entity import Entity
from game.entities.domain.Mob import Mob
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class AggressiveMob(Mob):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites, loadedImages: dict, loadedSounds: dict,
                 colliderRect: Rect, enemyData: dict, clock: Clock, midbottom: Vector2, currHealth: int = None):
        Mob.__init__(self, visibleSprites, obstacleSprites, loadedImages, loadedSounds, colliderRect, clock, enemyData, midbottom, currHealth)
        self.damage = enemyData["damage"]
        self.target = None
        self.attackCooldownMs = enemyData["attackCooldownMs"]
        self.timeFromLastAttack = 0

    def isInAttackRange(self, target: Entity | Object) -> bool:
        return self.isInRange(Vector2(target.rect.midbottom), self.actionRange)

    def attack(self, target: Entity | Object) -> None:
        target.getDamage(self.damage)
        if target.currentHealth == 0:
            self.target = None
            self.destinationPosition = None

    def moveTo(self, target: Entity | Object) -> None:
        self.destinationPosition = Vector2(target.rect.midbottom)
        self.move()

    def moveToOrAttack(self, target: Entity | Object) -> None:
        if self.isInAttackRange(target):
            if self.timeFromLastAttack >= self.attackCooldownMs:
                self.attack(target)
                self.timeFromLastAttack = 0
        else:
            self.moveTo(target)

    def localUpdate(self) -> None:
        if not self.target:
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
            else:
                self.moveRandomly()
                self.timeFromLastAttack += self.clock.get_time()
            return

        if not self.isInSightRange(self.target):
            self.target = None
            self.destinationPosition = None
            self.timeFromLastAttack += self.clock.get_time()
            return

        self.moveToOrAttack(self.target)
        self.timeFromLastAttack += self.clock.get_time()
