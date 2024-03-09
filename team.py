from ast import BitAnd
from player import Player
from stats import Stats, Statistic
from typing import Optional
# from tabulate import tabulate, SEPARATING_LINE
from event_types import *
from shot_chart import ShotChart
import pandas as pd


def opponent(team: int) -> int:
    return (team + 1) % 2


class Team:
    def __init__(self) -> None:
        self.id = 0
        self.name: str = ""
        self.short: str = ""
        self.players: list[Player] = []
        self.active: list[Player] = [Player()] * 5
        self.stats = Stats()
        self.last_update = 0
        self.shot_chart = ShotChart()

        self.verbose = False
        self.off_strategy = "~unknown~"
        self.def_strategy = "~unknown~"

    def set_starter(self, pid: int, pos: int):
        self.active[pos] = self.players[pid]
        self.players[pid].starter = True

    def make_sub(self, sub_type: SubType, player_out, player_in):
        pout = self.players[player_out]
        pin = self.players[player_in]

        if self.verbose:
            print(f"{str(sub_type)} - OUT: {pout.name}, IN: {pin.name}")

        if sub_type == SubType.SUB_PG:
            self.active[0] = pin
        elif sub_type == SubType.SUB_SG:
            self.active[1] = pin
        elif sub_type == SubType.SUB_SF:
            self.active[2] = pin
        elif sub_type == SubType.SUB_PF:
            self.active[3] = pin
        elif sub_type == SubType.SUB_C:
            self.active[4] = pin

    def make_swap(self, player1: int, player2: int):
        p1 = self.players[player1]
        p2 = self.players[player2]

        pos1 = -1
        pos2 = -1

        for index, player in enumerate(self.active):
            if player.id == p1.id:
                pos2 = index
            elif player.id == p2.id:
                pos1 = index

        pos_name = ["PG", "SG", "SF", "PF", "C"]

        self.active[pos1] = p1
        self.active[pos2] = p2

        if self.verbose:
            print(
                f"SWAP {self.name} - {p1.name} to {pos_name[pos1]} and {p2.name} to {pos_name[pos2]}"
            )

    def update_minutes(self, gameclock: int):
        secs = gameclock - self.last_update

        self.active[0].add_stats(Statistic.SecsPG, secs)
        self.active[1].add_stats(Statistic.SecsSG, secs)
        self.active[2].add_stats(Statistic.SecsSF, secs)
        self.active[3].add_stats(Statistic.SecsPF, secs)
        self.active[4].add_stats(Statistic.SecsC, secs)

        if self.verbose:
            for player in self.active:
                print(
                    f"MINUTES {self.short} - {player.name} +{secs}s = {player.secs_total()}"
                )

        self.last_update = gameclock

    def points(self) -> int:
        return self.stats.full.sheet[Statistic.Points]

    def add_stats(self, stat: Statistic, val: int, pid: Optional[int] = None):
        if isinstance(pid, int):
            if self.verbose:
                print(
                    f"{self.name},  {self.players[pid - 1].name},  {stat.name}: {val}"
                )
            self.players[pid - 1].stats.add(stat, val)
        else:
            if self.verbose:
                print(f"{self.name},  --  {stat.name}: {val}")
        self.stats.add(stat, val)

    def push_stat_sheet(self):
        self.stats.new_qtr_sheet()
        for player in self.players:
            player.stats.new_qtr_sheet()

    def print_stats(self): 
        # sort using 1. PTS and 2. MIN
        players_sorted = sorted(self.players, key = lambda player: ( player.stats.full.sheet[Statistic.Points],
                                        player.stats.full.sheet[Statistic.Seconds]), reverse=True)
        headers = [
            "球员",
            "分钟",
            "得分",
            "投篮",
            "命中率",
            "内投",
            "中投",
            "三分",
            "罚球",
            "+/-",
            "攻板",
            "防板",
            "总板",
            "助攻",
            "失误",
            "抢断",
            "盖帽",
            "犯规",
            "球权",
            "队伍球权",
            "队伍得分",
            "队伍失分",
            "传内投",
            "传中投",
            "传三分",
            "防内投",
            "防中投",
            "防三分",
            "干扰下出手",
            "干扰下命中",
            "受助攻出手",
            "受助攻命中",
        ]

        table = []
        for player in players_sorted:
            if player.name != 'Lucky Fan':
                table.append([player.name + " " + str(player.id), *player.stats.full.row()])
        table.append([self.name, *self.stats.full.row()])
        
        df = pd.DataFrame(table, columns=headers)
        df = df.fillna(0)
        # print(tabulate(table, headers=headers, tablefmt="rst", stralign="right"))
        # print()
        return df
    

    def __eq__(self, other):
        def stats_eql(stat: Statistic):
            if self.stats.full.sheet[stat] != other.stats.full.sheet[stat]:
                print(
                    f"Not eql: {str(stat)} - {self.name}: {self.stats.full.sheet[stat]} != {other.stats.full.sheet[stat]}"
                )
                return False
            return True

        team_eql = (
            self.id == other.id
            and self.name == other.name
            and stats_eql(Statistic.Points)
            and stats_eql(Statistic.FieldGoalsMade)
            and stats_eql(Statistic.FieldGoalsAtt)
            and stats_eql(Statistic.ThreePointsMade)
            and stats_eql(Statistic.ThreePointsAtt)
            and stats_eql(Statistic.FreeThrowsMade)
            and stats_eql(Statistic.FreeThrowsAtt)
            and stats_eql(Statistic.OffRebounds)
            and stats_eql(Statistic.DefRebounds)
            and stats_eql(Statistic.Assists)
            and stats_eql(Statistic.Turnovers)
            and stats_eql(Statistic.Steals)
            and stats_eql(Statistic.Blocks)
            and stats_eql(Statistic.Fouls)
        )

        player_map = {}
        for player in other.players:
            player_map[player.name] = player

        player_eql = True
        for player in self.players:
            other = player_map[player.name]

            def p_stats_eql(stat: Statistic):
                if player.stats.full.sheet[stat] != other.stats.full.sheet[stat]:
                    if __debug__:
                        print(
                            f"Not eql: {player.name} - {str(stat)}: {player.stats.full.sheet[stat]} != {other.stats.full.sheet[stat]}"
                        )
                    return False
                return True

            if __debug__:
                print(
                    player.name,
                    player.stats.full.minutes() == other.stats.full.minutes(),
                    player.stats.full.minutes(),
                    other.stats.full.minutes(),
                )

            player_eql &= (
                player.id == other.id
                and player.name == other.name
                and player.stats.full.minutes() == other.stats.full.minutes()
                and p_stats_eql(Statistic.Points)
                and p_stats_eql(Statistic.FieldGoalsMade)
                and p_stats_eql(Statistic.FieldGoalsAtt)
                and p_stats_eql(Statistic.ThreePointsMade)
                and p_stats_eql(Statistic.ThreePointsAtt)
                and p_stats_eql(Statistic.FreeThrowsMade)
                and p_stats_eql(Statistic.FreeThrowsAtt)
                and p_stats_eql(Statistic.OffRebounds)
                and p_stats_eql(Statistic.DefRebounds)
                and p_stats_eql(Statistic.Assists)
                and p_stats_eql(Statistic.Turnovers)
                and p_stats_eql(Statistic.Steals)
                and p_stats_eql(Statistic.Blocks)
                and p_stats_eql(Statistic.Fouls)
            )

        return team_eql and player_eql
    
    def update_team_minutes_and_gameplayed(self):
        # Calculate team played time (sum of player times divided by 5)
        for player in self.players:
            self.add_stats(Statistic.Seconds, player.stats.full.sheet[Statistic.Seconds], None)
            if player.stats.full.sheet[Statistic.Seconds] > 0:
                player.add_stats(Statistic.GamePlayed, 1)
        self.stats.full.sheet[Statistic.Seconds] = self.stats.full.sheet[Statistic.Seconds] / 5.0        
        self.add_stats(Statistic.GamePlayed, 1, None)
        
    def AccumulateTeamStat(self, team, game):
        # Accumulate the stats of team in a game to the season total

        self.stats.full.sheet = [a + b for a, b in zip(self.stats.full.sheet, team.stats.full.sheet)]
        # Then accumulate stats of players
        for player in team.players:
            for player_exist in self.players:
                if player_exist.id == player.id:
                    player_exist.AccumulatePlayerStat(player)
                    break
            else:
                self.players.append(player)
