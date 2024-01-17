from mcrcon import MCRcon
from requests import request


class Rcon:
    ip = None
    password = None
    mcr = None
    items_list = None

    def __init__(self, ip: str,
                 password: str):
        self.ip = ip
        self.password = password
        self.mcr = MCRcon(ip, password)
        self.getItemsList()
        self.execute("gamerule mobGriefing false")

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

    def getCoords(self, nickname: str):
        coords = []
        for _ in range(3):
            coords.append(int(
                self.execute(f"execute as {nickname} run data get entity {nickname} Pos[{_}]").split(":")[1].split(".")[
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

    def fill(self, area: int, block, nickname: str, hollow=False):
        if type(block) is int:
            blocktospawn = self.getBlockTypeById(block)
        else:
            blocktospawn = self.getBlockTypeByName(block)
        Px, Py, Pz = self.getCoords(nickname)
        tail = ""
        if hollow:
            tail = "hollow"
        self.execute(
            f"fill {Px - area} {Py - 1} {Pz - area} {Px + area} {Py + area} {Pz + area} minecraft:{blocktospawn} {tail}")

    def giveArmor(self, nickname: str, armortype: str):
        items = ["helmet", "chestplate", "leggings", "boots", "sword"]
        for item in items:
            self.execute(f"give {nickname} {armortype}_{item}")

    def spawnMob(self, mobname):
        self.execute(f"execute at @a run summon minecraft:{mobname} ~ ~ ~")

    def checkDeath(self, nickname: str):
        self.execute(f"execute at {nickname} run scoreboard objectives add hasDied deathCount")
        resp = self.execute("execute if entity @a[scores={hasDied=1..}]")
        self.execute(f"execute at {nickname} run scoreboard players set @a hasDied 0")
        if "passed" in resp:
            return False
        else:
            return True

# px, py, pz = rcon.getCoords("Robocode")
# rcon.setBlock(px, py, pz, "stone")
# rcon.fill(5, "glass", "Robocode", hollow=True)
# rcon.execute("clear Robocode")
# rcon.giveArmor("Robocode", "netherite")
# rcon.spawnMob("sheep")
