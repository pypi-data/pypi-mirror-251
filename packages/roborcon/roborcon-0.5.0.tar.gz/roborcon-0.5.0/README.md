
# roborcon

Module created to provide first lessons on Python And Minecraft (1.16.5 pref) for students in Robocode school.


## Usage/Examples
Example how to auto-build coliseum.
```python
from roborcon import Rcon

rcon = Rcon("server-ip", "rcon-password")
rcon.setPlayer("PlayerNickname")
rcon.setColiseumSize(15,5)
rcon.createColiseum()
```

Sets player nickname(required)
```python
rcon.setPlayer("PlayerNickname")
```
Execute any Rcon command.
```python
rcon.execute("give @a minecraft:diamond")
```
Get player position (array).
```python
x, y, z = rcon.getCoords()
```
Display title (bold red as default).
```python
rcon.title("TitleText")
```
Get all items list (to console).
```python
rcon.printItemNames()
```
Place blocks at position
```python
rcon.setBlock(x, y, z, "block name or id")
```
Fill cubic area around player.
```python
rcon.fill(area=5, "blockname", hollow=False, h=5)
```
Give player Armor, Sword with type
```python
rcon.giveArmor("Diamond")
```
Spawns mob around player or at specific position
(Set enemy to True if spawn around player, if False - spawning at specific position)
```python
rcon.spawnMob("mobname", x=0, y=0, z=0, enemy=True, params="")
```
Checks if player has died between checks
```python
rcon.checkDeath()
```
Change default params of coliseum size
```python
rcon.setColiseumSize(area, height)
```
Create coliseum around player
```python
rcon.createColiseum()
```