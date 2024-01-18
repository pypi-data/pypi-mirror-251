from mcrcon import MCRcon
from requests import request
import math
import random


class Rcon:
    ip = None
    password = None
    items_list = None
    coliseum_area = 10
    coliseum_height = 4
    player = None

    def __init__(self, ip: str,
                 password: str):
        self.ip = ip
        self.password = password
        self.mcr = MCRcon(ip, password)
        self.getItemsList()
        self.execute("gamerule mobGriefing false")

    def setColiseumSize(self, area: int, height: int):
        self.coliseum_area = area
        self.coliseum_height = height

    def setPlayer(self, nickname: str):
        self.player = nickname

    def getItemsList(self):
        try:
            resp = request('get', 'https://minecraft-ids.grahamedgecombe.com/items.json')
            if resp.status_code == 200:
                self.items_list = resp.json()
        except:
            print("Items list loading error! Maybe check your internet connection?")

    def execute(self, command: str):
        self.mcr.connect()
        lastcommand = self.mcr.command(command)
        self.mcr.disconnect()
        return lastcommand

    def getCoords(self):
        coords = []
        for _ in range(3):
            coords.append(int(
                self.execute(f"execute as {self.player} run data get entity {self.player} Pos[{_}]").split(":")[
                    1].split(".")[
                    0].split(" ")[1]))
            coords[_] -= 1
        return coords

    def title(self, title):
        self.execute('title @a title {"text" : "§c§l' + str(title) + '"}')

    def getBlockTypeById(self, blockid: int):
        if self.items_list is None:
            return blockid
        for item in self.items_list:
            if item['type'] == blockid:
                return item['text_type']
        print(f"There are no such item with id {blockid}")
        return -1

    def getBlockTypeByName(self, blockname: str):
        if self.items_list is None:
            return blockname
        for item in self.items_list:
            if item['name'].lower() == blockname.lower():
                return item['text_type']
        print(f"There are no such item with name {blockname}")
        return -1

    def printItemNames(self):
        if self.items_list is None:
            return
        for item in self.items_list:
            print(item['name'])

    def setBlock(self, xpos: int,
                 ypos: int,
                 zpos: int,
                 block):
        if type(block) is int:
            blocktospawn = self.getBlockTypeById(block)
        else:
            blocktospawn = self.getBlockTypeByName(block)
        self.execute(f"setblock {xpos} {ypos} {zpos} minecraft:{blocktospawn}")

    def fill(self, area: int, block, hollow=False, h=-1):
        if type(block) is int:
            blocktospawn = self.getBlockTypeById(block)
        else:
            blocktospawn = self.getBlockTypeByName(block)
        Px, Py, Pz = self.getCoords()
        tail = ""
        if hollow:
            tail = " hollow"
        if h == -1:
            h = area + 2
        p = self.execute(
            f"fill {Px - area} {Py - 1} {Pz - area} {Px + area} {Py + h - 2} {Pz + area} minecraft:{blocktospawn}{tail}")
        print(p)

    def giveArmor(self, armortype: str):
        items = ["helmet", "chestplate", "leggings", "boots", "sword"]
        for item in items:
            self.execute(f"give {self.player} {armortype}_{item}")

    def spawnMob(self, mobname, x="~", y="~", z="~", params=""):
        self.execute(
            'execute at @a run summon minecraft:' + mobname + ' ' + str(x) + ' ' + str(y) + ' ' + str(z) + params)

    def calculateBlockPos(self, r: int, angle):
        PI = 3.1415926535
        xp = r * math.cos(angle * PI / 180)
        yp = r * math.sin(angle * PI / 180)
        return xp, yp

    def createColiseum(self):
        if self.coliseum_area < 10:
            self.execute('tellraw @a {"text": "Minimum colloseum radius is 10!"}')
            self.coliseum_area = 10
        if self.coliseum_height < 4:
            self.execute('tellraw @a {"text": "Minimum colloseum height is 4!"}')
            self.coliseum_height = 4
        wall_blocks = ["Sandstone", "Red Sandstone", "Sandstone Stairs", "Sandstone", "Sandstone", "Sandstone",
                       "Glowstone"]
        minAngle = math.acos(1 - 1 / self.coliseum_area)
        self.fill(self.coliseum_area, "Air", h=self.coliseum_height + 1)
        self.fill(self.coliseum_area, "Sandstone", h=1)
        x, y, z = self.getCoords()
        for _ in range(self.coliseum_height):
            i = 0
            while i <= 360:
                angle = i
                x1, y1 = self.calculateBlockPos(self.coliseum_area, angle)
                self.setBlock(int(x + x1), int(y) + _, int(z + y1), random.choice(wall_blocks))
                if _ == 1:
                    x1, y1 = self.calculateBlockPos(self.coliseum_area - 1, angle)
                    self.setBlock(int(x + x1), int(y) + _, int(z + y1), "sandstone")
                    x1, y1 = self.calculateBlockPos(self.coliseum_area - 2, angle)
                    self.setBlock(int(x + x1), int(y) + _, int(z + y1), "sandstone")
                    if random.randint(0, 100) > 80:
                        self.spawnMob("villager", int(x + x1), int(y) + _ + 1, int(z + y1), params=" {NoAI:1}")
                if 1 < _ <= 3:
                    x1, y1 = self.calculateBlockPos(self.coliseum_area - 2, angle)
                    self.setBlock(int(x + x1), int(y) + _, int(z + y1), "glass")
                i += minAngle * 8

    def checkDeath(self):
        self.execute(f"execute at {self.player} run scoreboard objectives add hasDied deathCount")
        resp = self.execute("execute if entity @a[scores={hasDied=1..}]")
        self.execute(f"execute at {self.player} run scoreboard players set @a hasDied 0")
        if "passed" in resp:
            return False
        else:
            return True
