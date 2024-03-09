from enum import IntEnum

class Statistic(IntEnum):
    Points = 0
    FieldGoalsAtt = 1
    FieldGoalsMade = 2
    InsideShotsAtt = 3
    InsideShotsMade = 4
    MidRangeShotsAtt = 5
    MidRangeShotsMade = 6
    ThreePointsAtt = 7
    ThreePointsMade = 8
    FreeThrowsAtt = 9
    FreeThrowsMade = 10
    OffRebounds = 11
    DefRebounds = 12
    Assists = 13
    Turnovers = 14
    Steals = 15
    Blocks = 16
    Fouls = 17
    Seconds = 18
    PlusMinus = 19
    SecsPG = 20
    SecsSG = 21
    SecsSF = 22
    SecsPF = 23
    SecsC = 24
    ContestInsideShotAtt = 25
    ContestInsideShotMade = 26
    ContestMidRangeShotAtt = 27
    ContestMidRangeShotMade = 28
    ContestThreePointsAtt = 29
    ContestThreePointsMade = 30
    Timeouts30 = 31
    Timeouts60 = 32
    PersonalPossessions = 33
    TeamPossessions = 34
    TeamPtsGet = 35
    TeamPtsLost = 36
    AssistInsideShotAtt = 37
    AssistInsideShotMade = 38
    AssistMidRangeShotAtt = 39
    AssistMidrangeShotMade = 40
    AssistThreePointsAtt = 41
    AssistThreePointsMade = 42
    ContestedShotAtt = 43
    ContestedShotMade = 44
    AssistedShotAtt = 45
    AssistedShotMade = 46
    TeamOffRebounds = 47
    TeamDefRebounds = 48
    OppOffRebounds = 49
    OppDefRebounds = 50
    GamePlayed = 51

class StatSheet:
    def __init__(self) -> None:
        self.sheet = [0] * ( Statistic.GamePlayed + 1 )

    def __repr__(self) -> str:
        return f"""Stats
    MIN: {round(self.sheet[Statistic.Seconds] / 60)}
    PTS: {self.sheet[Statistic.Points]}
    FG:  {self.sheet[Statistic.FieldGoalsMade]} / {self.sheet[Statistic.FieldGoalsAtt]}
    TP:  {self.sheet[Statistic.ThreePointsMade]} / {self.sheet[Statistic.ThreePointsAtt]}
    FT:  {self.sheet[Statistic.FreeThrowsMade]} / {self.sheet[Statistic.FreeThrowsAtt]}
    +/-: {self.sheet[Statistic.PlusMinus]}
    OR:  {self.sheet[Statistic.OffRebounds]}
    DR:  {self.sheet[Statistic.DefRebounds]}
    TR:  {self.sheet[Statistic.OffRebounds] + self.sheet[Statistic.DefRebounds]}
    AST: {self.sheet[Statistic.Assists]}
    TO:  {self.sheet[Statistic.Turnovers]}
    STL: {self.sheet[Statistic.Steals]}
    BLK: {self.sheet[Statistic.Blocks]}
    PF:  {self.sheet[Statistic.Fouls]}
        """

    def row(self):
        return [
            round(self.sheet[Statistic.Seconds] / 60),
            self.sheet[Statistic.Points],
            f"{self.sheet[Statistic.FieldGoalsMade]}/{self.sheet[Statistic.FieldGoalsAtt]}",
            (self.sheet[Statistic.FieldGoalsAtt] and round(self.sheet[Statistic.FieldGoalsMade]/self.sheet[Statistic.FieldGoalsAtt],3)),
            f"{self.sheet[Statistic.InsideShotsMade]}/{self.sheet[Statistic.InsideShotsAtt]}",
            f"{self.sheet[Statistic.MidRangeShotsMade]}/{self.sheet[Statistic.MidRangeShotsAtt]}",
            f"{self.sheet[Statistic.ThreePointsMade]}/{self.sheet[Statistic.ThreePointsAtt]}",
            f"{self.sheet[Statistic.FreeThrowsMade]}/{self.sheet[Statistic.FreeThrowsAtt]}",
            self.sheet[Statistic.PlusMinus],
            self.sheet[Statistic.OffRebounds],
            self.sheet[Statistic.DefRebounds],
            self.sheet[Statistic.OffRebounds] + self.sheet[Statistic.DefRebounds],
            self.sheet[Statistic.Assists],
            self.sheet[Statistic.Turnovers],
            self.sheet[Statistic.Steals],
            self.sheet[Statistic.Blocks],
            self.sheet[Statistic.Fouls],
            self.sheet[Statistic.PersonalPossessions],
            self.sheet[Statistic.TeamPossessions],
            self.sheet[Statistic.TeamPtsGet],
            self.sheet[Statistic.TeamPtsLost],
            f"{self.sheet[Statistic.AssistInsideShotMade]}/{self.sheet[Statistic.AssistInsideShotAtt]}",
            f"{self.sheet[Statistic.AssistMidrangeShotMade]}/{self.sheet[Statistic.AssistMidRangeShotAtt]}",
            f"{self.sheet[Statistic.AssistThreePointsMade]}/{self.sheet[Statistic.AssistThreePointsAtt]}",
            f"{self.sheet[Statistic.ContestInsideShotMade]}/{self.sheet[Statistic.ContestInsideShotAtt]}",
            f"{self.sheet[Statistic.ContestMidRangeShotMade]}/{self.sheet[Statistic.ContestMidRangeShotAtt]}",
            f"{self.sheet[Statistic.ContestThreePointsMade]}/{self.sheet[Statistic.ContestThreePointsAtt]}",
            f"{self.sheet[Statistic.ContestedShotMade]}/{self.sheet[Statistic.ContestedShotAtt]}",
            (self.sheet[Statistic.ContestedShotAtt] and round(self.sheet[Statistic.ContestedShotMade]/self.sheet[Statistic.ContestedShotAtt],3)),
            f"{self.sheet[Statistic.AssistedShotMade]}/{self.sheet[Statistic.AssistedShotAtt]}",
            (self.sheet[Statistic.AssistedShotAtt] and round(self.sheet[Statistic.AssistedShotMade]/self.sheet[Statistic.AssistedShotAtt],3)),

        ]

    def player_stats(self):
        return {
            "secs_pg": self.sheet[Statistic.SecsPG],
            "secs_sg": self.sheet[Statistic.SecsSG],
            "secs_sf": self.sheet[Statistic.SecsSF],
            "secs_pf": self.sheet[Statistic.SecsPF],
            "secs_c": self.sheet[Statistic.SecsC],
            "mins": round(self.sheet[Statistic.Seconds] / 60),
            "pts": self.sheet[Statistic.Points],
            "fgm": self.sheet[Statistic.FieldGoalsMade],
            "fga": self.sheet[Statistic.FieldGoalsAtt],
            "tpm": self.sheet[Statistic.ThreePointsMade],
            "tpa": self.sheet[Statistic.ThreePointsAtt],
            "ftm": self.sheet[Statistic.FreeThrowsMade],
            "fta": self.sheet[Statistic.FreeThrowsAtt],
            "+/-": self.sheet[Statistic.PlusMinus],
            "or": self.sheet[Statistic.OffRebounds],
            "dr": self.sheet[Statistic.DefRebounds],
            "tr": self.sheet[Statistic.OffRebounds] + self.sheet[Statistic.DefRebounds],
            "ast": self.sheet[Statistic.Assists],
            "to": self.sheet[Statistic.Turnovers],
            "stl": self.sheet[Statistic.Steals],
            "blk": self.sheet[Statistic.Blocks],
            "pf": self.sheet[Statistic.Fouls],
            "dunks": None,
            "points_in_the_paint": None,
        }

    def team_stats(self):
        return {
            "pts": self.sheet[Statistic.Points],
            "fgm": self.sheet[Statistic.FieldGoalsMade],
            "fga": self.sheet[Statistic.FieldGoalsAtt],
            "tpm": self.sheet[Statistic.ThreePointsMade],
            "tpa": self.sheet[Statistic.ThreePointsAtt],
            "ftm": self.sheet[Statistic.FreeThrowsMade],
            "fta": self.sheet[Statistic.FreeThrowsAtt],
            "+/-": self.sheet[Statistic.PlusMinus],
            "or": self.sheet[Statistic.OffRebounds],
            "dr": self.sheet[Statistic.DefRebounds],
            "tr": self.sheet[Statistic.OffRebounds] + self.sheet[Statistic.DefRebounds],
            "ast": self.sheet[Statistic.Assists],
            "to": self.sheet[Statistic.Turnovers],
            "stl": self.sheet[Statistic.Steals],
            "blk": self.sheet[Statistic.Blocks],
            "pf": self.sheet[Statistic.Fouls],
            "dunks": None,
            "points_in_the_paint": None,
            "fastbreak_points": None,
            "second_chance_points": None,
            "bench_points": None,
            "points_of_turnovers": None,
            "biggest_lead": None,
            "time_of_possession": None,
            "possessions": None,
            "timeouts30": None,
            "timeouts60": None,
        }

    def minutes(self):
        self.sheet[Statistic.Seconds] = (self.sheet[Statistic.SecsPG]
            + self.sheet[Statistic.SecsSG]
            + self.sheet[Statistic.SecsSF]
            + self.sheet[Statistic.SecsPF]
            + self.sheet[Statistic.SecsC])

class Stats:
    def __init__(self) -> None:
        self.full = StatSheet()
        self.qtr: list[StatSheet] = []

    def add(self, stat: Statistic, val: int):
        self.full.sheet[stat] += val
        self.qtr[-1].sheet[stat] += val

    def new_qtr_sheet(self):
        self.qtr.append(StatSheet())
