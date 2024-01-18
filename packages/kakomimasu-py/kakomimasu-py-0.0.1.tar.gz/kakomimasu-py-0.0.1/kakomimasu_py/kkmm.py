import math
from typing import List, Tuple, Optional


class Point:
    def __init__(self, area_point: int, wall_point: int):
        self.area_point = area_point
        self.wall_point = wall_point


class Board:
    def __init__(
        self,
        width: int,
        height: int,
        points: List[int],
        n_agent: Optional[int] = None,
        n_player: Optional[int] = None,
        total_turn: Optional[int] = None,
    ):
        self.width = width
        self.height = height
        self.points = points
        self.n_agent = n_agent
        self.n_player = n_player
        self.total_turn = total_turn


class Action:
    PUT = 1
    NONE = 2
    MOVE = 3
    REMOVE = 4
    SUCCESS = 0
    CONFLICT = 1
    REVERT = 2
    ERR_ONLY_ONE_TURN = 3
    ERR_ILLEGAL_AGENT = 4
    ERR_ILLEGAL_ACTION = 5

    def __init__(self, agent_id: int, action_type: int, x: int, y: int):
        self.agent_id = agent_id
        self.type = action_type
        self.x = x
        self.y = y
        self.res = Action.SUCCESS

    @classmethod
    def from_json(cls, data):
        return cls(data["agent_id"], data["type"], data["x"], data["y"], data["res"])

    @staticmethod
    def get_message(res: int) -> str:
        messages = [
            "success",
            "conflict",
            "revert",
            "err: only 1 turn",
            "err: illegal agent",
            "err: illegal action",
        ]
        return messages[res]

    @classmethod
    def from_array(cls, array: List[Tuple[int, int, int, int]]):
        return [cls(*a) for a in array]


class Agent:
    def __init__(self, field, player_idx: int):
        self.field = field
        self.player_idx = player_idx
        self.x = -1
        self.y = -1
        self.bkx = -1
        self.bky = -1
        self._last_action = None

    @classmethod
    def from_json(cls, data, player_idx: int, field):
        agent = cls(field, player_idx)
        agent.x = data["x"]
        agent.y = data["y"]
        return agent

    def to_json(self):
        return {"x": self.x, "y": self.y}

    def _is_on_board(self) -> bool:
        return self.x != -1

    def _check_on_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.field.width and 0 <= y < self.field.height

    def _check_dir(self, x: int, y: int) -> bool:
        if self.x == x and self.y == y:
            return False
        return abs(self.x - x) <= 1 and abs(self.y - y) <= 1

    def check(self, act) -> bool:
        self._last_action = act
        self.bkx = self.x
        self.bky = self.y
        x = act.x
        y = act.y
        if act.type == Action.PUT:
            return self._check_put(x, y)
        elif act.type == Action.MOVE:
            return self._check_move(x, y)
        elif act.type == Action.REMOVE:
            return self._check_remove(x, y)
        else:
            return False

    def _check_put(self, x: int, y: int) -> bool:
        if self._is_on_board():
            return False
        if not self._check_on_board(x, y):
            return False
        return True

    def _check_move(self, x: int, y: int) -> bool:
        if not self._is_on_board():
            return False
        if not self._check_on_board(x, y):
            return False
        if not self._check_dir(x, y):
            return False
        return True

    def _check_remove(self, x: int, y: int) -> bool:
        if not self._is_on_board():
            return False
        if not self._check_on_board(x, y):
            return False
        if not self._check_dir(x, y):
            return False
        if self.field.get(x, y)["type"] != Field.WALL:
            return False
        return True

    def isValidAction(self) -> Optional[Action]:
        if self._last_action is None:
            return None
        if self._last_action.res != Action.SUCCESS:
            return None
        return self._last_action

    def putOrMove(self) -> bool:
        if self._last_action is None:
            raise Exception("putOrMove called before check")
        if self._last_action.res != Action.SUCCESS:
            return False
        if self._last_action.type == Action.PUT:
            return self._put(self._last_action.x, self._last_action.y)
        elif self._last_action.type == Action.MOVE:
            return self._move(self._last_action.x, self._last_action.y)
        return True

    def _put(self, x: int, y: int) -> bool:
        if not self._check_put(x, y):
            return False
        if not self.field.set_agent(self.player_idx, x, y):
            # throw new Error("can't enter the wall");
            return False
        self.x = x
        self.y = y
        return True

    def _move(self, x: int, y: int) -> bool:
        if not self._check_move(x, y):
            return False
        if not self.field.set_agent(self.player_idx, x, y):
            # throw new Error("can't enter the wall");
            return False
        self.x = x
        self.y = y
        return True

    def remove(self) -> bool:
        if self._last_action is None:
            raise Exception("remove called before check")
        if not self._check_remove(self._last_action.x, self._last_action.y):
            return False
        self.field.set(self._last_action.x, self._last_action.y, Field.AREA, None)
        return True

    def commit(self):
        self._last_action = None

    def revert(self):
        if (
            self._last_action
            and (
                self._last_action.type == Action.MOVE
                or self._last_action.type == Action.PUT
            )
            and self._last_action.res == Action.SUCCESS
        ):
            self._last_action.res = Action.REVERT
            self.x = self.bkx
            self.y = self.bky


class Field:
    AREA = 0
    WALL = 1

    def __init__(
        self,
        width: int,
        height: int,
        points: List[int],
        n_agent: int = None,
        n_player: int = None,
    ):
        if len(points) != width * height:
            raise ValueError("points.length must be equal to width * height")
        self.width = width
        self.height = height
        self.n_agent = n_agent if n_agent else 4
        self.n_player = n_player if n_player else 2
        self.points = points
        self.tiles = [
            {"type": Field.AREA, "player": None} for _ in range(width * height)
        ]

    @classmethod
    def from_json(cls, data):
        field = cls(
            data["width"],
            data["height"],
            data["points"],
            data["n_agent"],
            data["n_player"],
        )
        field.tiles = data["tiles"]
        return field

    def set(self, x: int, y: int, att: int, player_id: Optional[int]):
        if player_id is not None and player_id < 0:
            raise ValueError("player_id must be non-negative")
        self.tiles[x + y * self.width] = {"type": att, "player": player_id}

    def get(self, x: int, y: int) -> dict:
        return self.tiles[x + y * self.width]

    def set_agent(self, player_id: int, x: int, y: int) -> bool:
        tile = self.get(x, y)
        if tile["type"] == Field.WALL and tile["player"] != player_id:
            return False
        self.set(x, y, Field.WALL, player_id)
        return True

    def fill_area(self):
        w, h = self.width, self.height
        extended_field = [
            {"type": Field.AREA, "player": None} for _ in range((w + 2) * (h + 2))
        ]

        # 外側に空白のマスを追加
        for y in range(-1, h + 1):
            for x in range(-1, w + 1):
                if x < 0 or x >= w or y < 0 or y >= h:
                    continue
                extended_field[(x + 1) + (y + 1) * (w + 2)] = self.tiles[x + y * w]

        mask = [1] * len(extended_field)

        while sum(mask):
            area = [0] * len(extended_field)
            for pid in range(self.n_player):
                for i in range(len(extended_field)):
                    area[i] |= 1 << pid

                def chk(x, y):
                    n = x + y * (w + 2)
                    if x < 0 or x >= w + 2 or y < 0 or y >= h + 2:
                        return
                    if area[n] & (1 << pid) == 0:
                        return
                    if (
                        mask[n] != 0
                        and extended_field[n]["type"] == Field.WALL
                        and extended_field[n]["player"] == pid
                    ):
                        return
                    area[n] &= ~(1 << pid)
                    chk(x - 1, y)
                    chk(x + 1, y)
                    chk(x - 1, y - 1)
                    chk(x, y - 1)
                    chk(x + 1, y - 1)
                    chk(x - 1, y + 1)
                    chk(x, y + 1)
                    chk(x + 1, y + 1)

                chk(0, 0)

            for i in range(len(extended_field)):
                if area[i] == 0:
                    mask[i] = 0
                elif area[i] & (area[i] - 1) == 0:  # 2のべき乗かどうかをチェック
                    extended_field[i]["player"] = int(math.log2(area[i]))
                    mask[i] = 0

        # 結果を元のフィールドに反映
        for i in range(w):
            for j in range(h):
                n = i + j * w
                nexp = (i + 1) + (j + 1) * (w + 2)
                if self.tiles[n]["type"] != Field.WALL:
                    self.tiles[n] = extended_field[nexp]

    def get_points(self) -> List[Point]:
        points = []
        for i in range(self.n_player):
            points.append(Point(area_point=0, wall_point=0))

        for idx, tile in enumerate(self.tiles):
            if tile["player"] is None:
                continue
            p = points[tile["player"]]
            point_value = self.points[idx]
            if tile["type"] == Field.WALL:
                p.wall_point += point_value
            elif tile["type"] == Field.AREA:
                p.area_point += abs(point_value)

        return points


class Game:
    def __init__(self, board: Board):
        self.total_turn = board.total_turn if board.total_turn else 30
        self.players = []
        self.field = Field(
            board.width, board.height, board.points, board.n_agent, board.n_player
        )
        self.log = []
        self.turn = 0

    @classmethod
    def from_json(cls, data):
        game = cls(
            data["total_turn"],
            data["field"]["width"],
            data["field"]["height"],
            data["field"]["points"],
            data["field"]["n_agent"],
            data["field"]["n_player"],
        )
        game.players = [Player.from_json(p, game) for p in data["players"]]
        game.field.tiles = data["field"]["tiles"]
        game.log = data["log"]
        game.turn = data["turn"]
        return game

    def attach_player(self, player) -> bool:
        if not self.is_free() or player in self.players:
            return False
        player.index = len(self.players)
        player.set_game(self)
        self.players.append(player)
        return True

    def get_status(self) -> str:
        if self.turn == 0:
            return "free" if len(self.players) < self.field.n_player else "ready"
        elif len(self.log) != self.total_turn:
            return "gaming"
        else:
            return "ended"

    def is_free(self) -> bool:
        return self.get_status() == "free"

    def is_ready(self) -> bool:
        return self.get_status() == "ready"

    def is_gaming(self) -> bool:
        return self.get_status() == "gaming"

    def is_ended(self) -> bool:
        return self.get_status() == "ended"

    def start(self):
        self.turn = 1

    def next_turn(self) -> bool:
        actions = [player.get_actions() for player in self.players]

        self._check_actions(actions)

        self._revert_not_owner_wall()
        self._check_conflict(actions)
        self._revert_overlap()
        self._put_or_move()
        self._remove_or_not()

        self._commit()

        self.field.fill_area()

        self.log.append(
            {
                "players": [
                    {"point": self.field.get_points()[idx], "actions": actions[idx]}
                    for idx in range(len(actions))
                ]
            }
        )

        for player in self.players:
            player.clear_actions()

        if self.turn < self.total_turn:
            self.turn += 1
            return True
        else:
            return False

    def _check_actions(self, actions: List[List[Action]]):
        n_players = len(actions)
        for player_id in range(n_players):
            done_actions = {}
            for action in actions[player_id]:
                agent_id = action.agent_id
                if agent_id < 0 or agent_id >= len(self.players[player_id].agents):
                    action.res = Action.ERR_ILLEGAL_AGENT
                    continue

                if agent_id in done_actions:
                    action.res = Action.ERR_ONLY_ONE_TURN
                    done_actions[agent_id].res = Action.ERR_ONLY_ONE_TURN
                    continue

                done_actions[agent_id] = action

        # 有効な動きをチェック
        for player_id in range(n_players):
            for action in filter(lambda a: a.res == Action.SUCCESS, actions[player_id]):
                agent_id = action.agent_id
                agent = self.players[player_id].agents[agent_id]
                if not agent.check(action):
                    action.res = Action.ERR_ILLEGAL_ACTION

    def _check_conflict(self, actions: List[List[Action]]):
        chkfield = [[] for _ in range(self.field.width * self.field.height)]
        n_players = len(actions)

        # すべての有効なアクションをチェックフィールドにマッピング
        for player_id in range(n_players):
            for action in filter(lambda a: a.res == Action.SUCCESS, actions[player_id]):
                n = action.x + action.y * self.field.width
                if 0 <= n < len(chkfield):
                    chkfield[n].append(action)

        # 同じ場所を対象とするアクションが複数あれば競合と判定
        for field_actions in filter(lambda a: len(a) >= 2, chkfield):
            for action in field_actions:
                action.res = Action.CONFLICT

    def _put_or_move(self):
        for player in self.players:
            for agent in player.agents:
                if not agent.isValidAction():
                    continue
                if not agent.putOrMove():
                    # エラー処理または例外を投げることも可能です。
                    # 例: raise Exception("Illegal action!")
                    pass

    def _revert_overlap(self):
        reverts = False
        chkfield = [[] for _ in range(self.field.width * self.field.height)]
        # エージェントの現在位置と予定位置をチェックフィールドにマッピング
        for player in self.players:
            for agent in player.agents:
                act = agent.isValidAction()
                if act and (act.type == Action.MOVE or act.type == Action.PUT):
                    n = act.x + act.y * self.field.width
                    chkfield[n].append(agent)
                else:
                    if agent.x == -1:
                        continue
                    n = agent.x + agent.y * self.field.width
                    chkfield[n].append(agent)

        # 重複している位置を見つけてエージェントの動作を取り消す
        for agents in filter(lambda a: len(a) >= 2, chkfield):
            for agent in agents:
                agent.revert()
            reverts = True

        # 重複があった場合は再度全てのエージェントの位置をチェック
        if reverts:
            self._revert_overlap()

    def _remove_or_not(self):
        all_agents = [agent for player in self.players for agent in player.agents]

        for agent in all_agents:
            if agent.x == -1:
                continue
            valid_action = agent.isValidAction()
            if not valid_action or valid_action.type != Action.REMOVE:
                continue
            # エージェントがいる場所にREMOVEアクションを実行している場合、そのアクションを取り消す
            if any(a.x == valid_action.x and a.y == valid_action.y for a in all_agents):
                valid_action.res = Action.REVERT
            else:
                agent.remove()

    def _revert_not_owner_wall(self):
        for player in self.players:
            for agent in player.agents:
                if agent.x == -1:
                    continue
                act = agent.isValidAction()
                if not act:
                    continue
                if act.type not in [Action.MOVE, Action.PUT]:
                    continue
                # PUT & MOVE のみを対象とする
                n = act.x + act.y * self.field.width
                tile = self.field.tiles[n]
                is_wall = tile["type"] == Field.WALL
                owner = tile["player"]
                if is_wall and owner != agent.player_idx and owner != -1:
                    agent.revert()

    def _commit(self):
        for player in self.players:
            for agent in player.agents:
                agent.commit()


class Player:
    def __init__(self, id: str, spec: str = ""):
        self.id = id
        self.spec = spec
        self.game = None
        self.actions = []
        self.index = -1
        self.agents = []

    @classmethod
    def from_json(cls, data, game=None):
        player = cls(data["id"], data["spec"])
        player.index = data["index"]
        if game:
            player.set_game(game)
            player.agents = [
                Agent.from_json(a, player.index, game.field) for a in data["agents"]
            ]
        return player

    def to_json(self):
        return {
            "id": self.id,
            "spec": self.spec,
            "index": self.index,
            "actions": self.actions,
            "agents": self.agents,
        }

    def set_game(self, game):
        self.game = game
        for i in range(game.field.n_agent):
            self.agents.append(Agent(game.field, self.index))

    def set_actions(self, actions: List[Action]):
        if self.game is None:
            raise ValueError("Game is not set")
        self.actions = actions

    def get_actions(self) -> List[Action]:
        return self.actions

    def clear_actions(self):
        self.actions = []
