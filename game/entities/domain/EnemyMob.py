from abc import abstractmethod

from pygame.math import Vector2
from pygame.time import Clock

from game.entities.domain.Entity import Entity
from game.entities.domain.Mob import Mob
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class EnemyMob(Mob):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 obstacleSprites: ObstacleSprites,
                 enemyData, clock: Clock):
        super().__init__(visibleSprites, obstacleSprites, clock, enemyData, enemyData["sightRange"], 200, 500, 700)
        self.attackRange = enemyData["attackRange"]
        self.damage = enemyData["damage"]
        self.target = None

    def isInAttackRange(self, target: Entity | Object) -> bool:
        return self.isInRange(target, self.attackRange)

    def attack(self, target: Entity | Object):
        target.getDamage(self.damage)
        self.afterAttackAction()

    def moveTo(self, target: Entity | Object):
        self.destinationPosition = Vector2(target.rect.midbottom)
        self.move()

    @abstractmethod
    def afterAttackAction(self):
        pass

    def moveToOrAttack(self, target: Entity | Object):
        if self.isInAttackRange(target):
            self.attack(target)
        else:
            self.moveTo(target)

    def localUpdate(self):
        if not self.target:
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
                return
            self.moveRandomly()
            return

        if not self.isInSightRange(self.target):
            self.target = None
            self.destinationPosition = None
            return

        self.moveToOrAttack(self.target)
