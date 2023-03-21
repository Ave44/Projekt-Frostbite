from abc import abstractmethod

from pygame.math import Vector2
from pygame.time import Clock

from game.entities.domain.Entity import Entity
from game.entities.domain.Mob import Mob
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class AggressiveMob(Mob):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 obstacleSprites: ObstacleSprites,
                 enemyData, clock: Clock, moveEveryMs: int,
                 minMoveTimeMs: int, maxMoveTimeMs: int, attackCooldownMs: int):
        super().__init__(visibleSprites, obstacleSprites, clock, enemyData,
                         enemyData["sightRange"], moveEveryMs, minMoveTimeMs, maxMoveTimeMs)
        self.attackRange = enemyData["attackRange"]
        self.damage = enemyData["damage"]
        self.target = None
        self.attackCooldownMs = attackCooldownMs
        self.timeFromLastAttack = 0

    def isInAttackRange(self, target: Entity | Object) -> bool:
        return self.isInRange(target, self.attackRange)

    def attack(self, target: Entity | Object):
        target.getDamage(self.damage)
        if target.currentHealth == 0:
            self.target = None
            self.destinationPosition = None
        self.afterAttackAction()

    def moveTo(self, target: Entity | Object):
        self.destinationPosition = Vector2(target.rect.midbottom)
        self.move()

    @abstractmethod
    def afterAttackAction(self):
        pass

    def moveToOrAttack(self, target: Entity | Object):
        if self.isInAttackRange(target) and self.timeFromLastAttack >= self.attackCooldownMs:
            self.attack(target)
            self.timeFromLastAttack = 0
        else:
            self.moveTo(target)
            self.timeFromLastAttack += self.clock.get_time()

    def localUpdate(self):
        if not self.target:
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
                return
            self.moveRandomly()
            self.timeFromLastAttack += self.clock.get_time()
            return

        if not self.isInSightRange(self.target):
            self.target = None
            self.destinationPosition = None
            self.timeFromLastAttack += self.clock.get_time()
            return

        self.moveToOrAttack(self.target)
