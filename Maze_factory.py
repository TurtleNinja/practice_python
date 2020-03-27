from enum import Enum

class MapSite():
    def Enter(self):
        raise NotImplementedError("This is an abstract class")

class Direction(Enum):
    North = 0
    South = 1
    East  = 2
    West  = 3

class Room(MapSite):
    def __init__(self, roomNo):
        self._roomNumber = int(roomNo)
        self._sides = [MapSite] * 4

    def Enter(self):
        print("Entering room " + str(self._roomNumber))

    def SetSide(self, Direction, Mapsite):
        self._sides[Direction] = Mapsite

    def GetSide(self, Direction):
        return self._sides[Direction]

class Wall(MapSite):
    def Enter(self):
        print("\t\tYou've just ran into a wall...")

class Door(MapSite):
    def __init__(self, room1 = None, room2 = None):
        self._room1 = room1
        self._room2 = room2
        self._isOpen = False

    def GetToOtherSideFrom(self, Room):
        if not self._isOpen:
            self.Open()

        if Room._roomNumber == self._room1._roomNumber:
            other_room = self._room2
        else:
            other_room = self._room1
        self._isOpen = False
        return other_room

    def Enter(self):
        if not self._isOpen:
            print("\t\tDoor is not open. Please open door to enter room")
    
    def Open(self):
        self._isOpen = True
        print("\t\tOpening the door between room {} and room {}...".format(self._room1._roomNumber, self._room2._roomNumber))

class Maze():
    def __init__(self):
        self._rooms = {}

    def AddRoom(self, room):
        self._rooms[room._roomNumber] = room  #why so complicated?

    def RoomNo(self, room_number):
        return self._rooms[room_number]

class MazeFactory():
    @classmethod
    def MakeMaze(cls):
        return Maze()
    @classmethod
    def MakeWall(cls):
        return Wall()
    @classmethod
    def MakeRoom(cls, room_number):
        return Room(room_number)
    @classmethod
    def MakeDoor(cls, r1, r2):
        return Door(r1, r2)

#*************************************************
class EnchantedRoom(Room):
    def __init__(self, room_number):
        self._roomNumber = room_number
        self._sides = [MapSite] * 4

    def Enter(self):
        print("Entering enchanted room " + str(self._roomNumber))

class DoorNeedingASpell(Door):
    def __init__(self, room1 = None, room2 = None):
        self._room1 = room1
        self._room2 = room2
        self._isOpen = False
    
    def Open(self):
        self._isOpen = True
        print("\t\tEnter the spell to open door: [a_secrete_spell]")
        print("\t\tOpening the door between room {} and room {}...".format(self._room1._roomNumber, self._room2._roomNumber))

class EnchantedMazeFactory(MazeFactory):
    @classmethod
    def MakeRoom(cls, room_number):
        return EnchantedRoom(room_number)
    @classmethod
    def MakeDoor(cls, r1, r2):
        return DoorNeedingASpell(r1, r2)
        
#*************************************************
class BombRoom(Room):
    def __init__(self, room_number):
        self._roomNumber = room_number
        self._sides = [MapSite] * 4
        self._bombDisabled = False
    
    def Enter(self):
        print("Entering bomb room " + str(self._roomNumber))

    def DisableBomb(self):
        print("Disabling the bomb...")

class BombProofDoor(Door):
    def __init__(self, room1 = None, room2 = None):
        self._room1 = room1
        self._room2 = room2
        self._isOpen = False

    def GetToOtherSideFrom(self, room):
        if not self._isOpen:
            self.Open()
        # obtain the door on the other side
        if room._roomNumber == self._room1._roomNumber:
            other_room = self._room2
        else:
            other_room = self._room1
        # warning about the bombed
        if other_room._bombDisabled:
            print("\t\tThe bomb in room {} was disabled. Safe to enter now.".format(other_room._roomNumber))
        else:
            print("\t\tThe bomb in room {} is active!!".format(other_room._roomNumber))
        return other_room

    def Open(self):
        self._isOpen = True
        print("\t\tOpening the bomb proof door between room {} and room {}...".format(self._room1._roomNumber, self._room2._roomNumber))

class BombProofWall(Wall):
    def Enter(self):
        print("\t\tYou've just ran into a bomb proof wall...")

class BombedMazeFactory(MazeFactory):
    @classmethod
    def MakeRoom(cls, n):
        return BombRoom(n)
    
    @classmethod
    def MakeDoor(cls, r1, r2):
        return BombProofDoor(r1, r2)
    
    @classmethod
    def MakeWall(cls):
        return BombProofWall()


class MazeGame():
    def CreateMaze(self, factory = MazeFactory):
        maze = factory.MakeMaze()
        room1 = factory.MakeRoom(1)
        room2 = factory.MakeRoom(2)
        door12 = factory.MakeDoor(room1, room2)
        # set up room1
        room1.SetSide(Direction.North.value, factory.MakeWall())
        room1.SetSide(Direction.East.value, factory.MakeWall())
        room1.SetSide(Direction.South.value, factory.MakeWall())
        room1.SetSide(Direction.West.value, door12)
        # set up room 2
        room2.SetSide(Direction.North.value, factory.MakeWall())
        room2.SetSide(Direction.West.value, factory.MakeWall())
        room2.SetSide(Direction.South.value, factory.MakeWall())
        room2.SetSide(Direction.East.value, door12)
        # set up the maze
        maze.AddRoom(room1)
        maze.AddRoom(room2)

        return maze

#====================================================#
def find_maze_rooms(aMaze):
    maze_rooms = []
    for room_number in range(5):
        try:
            room = aMaze.RoomNo(room_number)
            print()
            print("The maze has room: " + str(room_number))
            room.Enter()
            maze_rooms.append(room)
            print("Entered the room!")

            for idx in range(4):
                side = room.GetSide(idx)
                side_str = str(side.__class__).replace("<class '__main__.", "").replace("'>", "")
                print("\tRoom: {}, {:<15s}, Type: {}".format(room_number, Direction(idx), side_str))
                side.Enter()
                if side_str == "Door" or side_str == "DoorNeedingASpell" or side_str == "BombProofDoor":
                    next_room = side.GetToOtherSideFrom(room)
                    print("\t\tMoving from room {} to room {}".format(room._roomNumber, next_room._roomNumber))
        except:
            print("The Maze doesn't have room " + str(room_number))

    print("This maze has {} rooms.".format(len(maze_rooms)))


print("***************************")
print("******   MAZE GAME   ******")
print("***************************")
factory = MazeFactory()
maze = MazeGame().CreateMaze(factory)
find_maze_rooms(maze)

factory2 = EnchantedMazeFactory()
enchanted_maze = MazeGame().CreateMaze(factory2)
find_maze_rooms(enchanted_maze)

factory3 = BombedMazeFactory()
bombed_maze = MazeGame().CreateMaze(factory3)
find_maze_rooms(bombed_maze)