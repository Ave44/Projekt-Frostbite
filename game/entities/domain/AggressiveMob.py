from abc import ABC

from pygame import Vector2, Rect
from pygame.time import Clock

from game.SoundPlayer import SoundPlayer
from game.entities.domain.Entity import Entity
from game.entities.domain.Mob import Mob
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class AggressiveMob(Mob, ABC):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites, loadedImages: dict, loadedSounds: dict,
                 colliderRect: Rect, enemyData: dict, clock: Clock, midbottom: Vector2, currHealth: int = None, soundPlayer: SoundPlayer = None):
        Mob.__init__(self, visibleSprites, obstacleSprites, loadedImages, loadedSounds, colliderRect, clock, enemyData, midbottom, currHealth, soundPlayer)
        self.damage = enemyData["damage"]
        self.target = None
        self.attackCooldownMs = enemyData["attackCooldownMs"]
        self.timeFromLastAttack = 0
        self.lookForTargetOncePerFrames = 10
        self.framesUntilLookingForTarget = 0

    def isInAttackRange(self, target: Entity | Object) -> bool:
        return self.isInRange(Vector2(target.rect.midbottom), self.actionRange)

    def attack(self, target: Entity | Object):
        target.getDamage(self.damage)
        if target.currHealth == 0:
            self.target = None
            self.destinationPosition = None

    def moveTo(self, target: Entity | Object):
        self.destinationPosition = Vector2(target.rect.midbottom)
        self.move()

    def moveToOrAttack(self, target: Entity | Object):
        if self.isInAttackRange(target):
            if self.timeFromLastAttack >= self.attackCooldownMs:
                self.attack(target)
                self.timeFromLastAttack = 0
        else:
            self.moveTo(target)

    def localUpdate(self):
        if self.target:
            if self.isInSightRange(self.target):
                self.moveToOrAttack(self.target)
                self.timeFromLastAttack += self.clock.get_time()
            else:
                self.target = None
                self.destinationPosition = None
                self.timeFromLastAttack += self.clock.get_time()    

        elif self.framesUntilLookingForTarget == 0:
            self.framesUntilLookingForTarget = self.lookForTargetOncePerFrames
        
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
        else:
            self.moveRandomly()
            self.timeFromLastAttack += self.clock.get_time()
            self.framesUntilLookingForTarget -= 1
