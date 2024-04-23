import requests
import xml.etree.ElementTree as xml
from team import Team
from game import Game
from bbapi import BBApi
from player import Player
from stats import *
from main import *
from os.path import exists
import numpy as np
import pandas as pd

class Season:
    def __init__(self, league_id, season_no) -> None:
        self.league_id = league_id
        self.season_no = season_no
        self.teams: list[Team] = []
        self.games: list[Game] = []
        
    def import_game(self, game, gamelimit, minutelimit):
        game.play()
        self.games.append(game)
        # load teams and update number
        for team in game.teams:
            for team_exist in self.teams:
                if team_exist.id == team.id:
                    team_exist.AccumulateTeamStat(team, game)
                    break
            else:
                self.teams.append(team)      
    
    def generate_season_report_players(self, gamelimit, minutelimit):
        headers = [
            "球员","球队","出场次数","分钟","得分","投篮命中","投篮","投篮命中率",
            "内投命中","内投","内投命中率","中投命中","中投","中投命中率","三分命中","三分","三分命中率",
            "罚球命中","罚球","罚球命中率",
            "进攻篮板","防守篮板","总篮板",
            "助攻","失误","抢断","盖帽","犯规",
            "百回合得分","百回合失分","百回合净胜分","on-off百回合净胜分","on-off百回合得分","on-off百回合失分",
            "球权使用率","真实命中率","干扰下命中","干扰下出手","干扰下命中率","干扰下出手比例",
            "接球攻命中","接球攻出手","接球攻命中率","接球攻出手比例",
            "助攻率","助失比","进攻篮板率","防守篮板率","总篮板率","失误率",
            "传内投命中","传内投出手","传中投命中","传中投出手","传三分命中","传三分出手","传球后命中","传球后出手","传球转化率",
            "防内投命中","防内投出手","防中投命中","防中投出手","防三分命中","防三分出手","防总命中","防总出手","对位命中率",
            "PG比例","SG比例","SF比例","PF比例","C比例"
        ]

        headers_team = ["球队","分钟","得分","失分","投篮命中","投篮","投篮命中率",
            "内投命中","内投","内投命中率","中投命中","中投","中投命中率","三分命中","三分","三分命中率",
            "罚球命中","罚球","罚球命中率",
            "进攻篮板","防守篮板","总篮板",
            "助攻","失误","抢断","盖帽","犯规",
            "48分钟回合数","百回合得分","百回合失分","百回合净胜分",
            "真实命中率","干扰下命中","干扰下出手","干扰下命中率","干扰下出手比例",
            "接球攻命中","接球攻出手","接球攻命中率","接球攻出手比例",
            "助失比","进攻篮板率","防守篮板率","总篮板率","失误率",
            "传内投命中","传内投出手","传中投命中","传中投出手","传三分命中","传三分出手","传球后命中","传球后出手","传球转化率",
            "防内投命中","防内投出手","防中投命中","防中投出手","防三分命中","防三分出手","防总命中","防总出手","对位命中率",]

        file_name = f"results/League{self.league_id}_Season{self.season_no}.xlsx"
        table1 = []
        table2 = []
        with pd.ExcelWriter(file_name) as writer:
            for team in self.teams:
                for player in team.players:
                    if player.name != 'Lucky Fan':
                        pstat = player.stats.full.sheet
                        tstat = team.stats.full.sheet
                        table1.append([player.name + " " + str(player.id),
                                      team.name + " " + str(team.id),
                                      pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.Seconds]) / 60 / pstat[Statistic.GamePlayed], # 分钟
                                      np.float64(pstat[Statistic.Points]) / pstat[Statistic.GamePlayed], # 得分
                                      np.float64(pstat[Statistic.FieldGoalsMade]) / pstat[Statistic.GamePlayed], # 投篮
                                      np.float64(pstat[Statistic.FieldGoalsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.FieldGoalsMade]) / pstat[Statistic.FieldGoalsAtt],
                                      np.float64(pstat[Statistic.InsideShotsMade]) / pstat[Statistic.GamePlayed], # 内投
                                      np.float64(pstat[Statistic.InsideShotsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.InsideShotsMade]) / pstat[Statistic.InsideShotsAtt],
                                      np.float64(pstat[Statistic.MidRangeShotsMade]) / pstat[Statistic.GamePlayed], # 中投
                                      np.float64(pstat[Statistic.MidRangeShotsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.MidRangeShotsMade]) / pstat[Statistic.MidRangeShotsAtt],
                                      np.float64(pstat[Statistic.ThreePointsMade]) / pstat[Statistic.GamePlayed], # 三分
                                      np.float64(pstat[Statistic.ThreePointsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.ThreePointsMade]) / pstat[Statistic.ThreePointsAtt],
                                      np.float64(pstat[Statistic.FreeThrowsMade]) / pstat[Statistic.GamePlayed], # 罚球
                                      np.float64(pstat[Statistic.FreeThrowsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.FreeThrowsMade]) / pstat[Statistic.FreeThrowsAtt],
                                      np.float64(pstat[Statistic.OffRebounds]) / pstat[Statistic.GamePlayed], # 篮板
                                      np.float64(pstat[Statistic.DefRebounds]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.OffRebounds] + pstat[Statistic.DefRebounds]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.Assists]) / pstat[Statistic.GamePlayed], # 助攻
                                      np.float64(pstat[Statistic.Turnovers]) / pstat[Statistic.GamePlayed], # 失误
                                      np.float64(pstat[Statistic.Steals]) / pstat[Statistic.GamePlayed], # 抢断
                                      np.float64(pstat[Statistic.Blocks]) / pstat[Statistic.GamePlayed], # 盖帽
                                      np.float64(pstat[Statistic.Fouls]) / pstat[Statistic.GamePlayed], # 犯规
                                      np.float64(pstat[Statistic.TeamPtsGet]) / pstat[Statistic.TeamPossessions] * 100, # 进攻百回合
                                      np.float64(pstat[Statistic.TeamPtsLost]) / pstat[Statistic.TeamPossessions] * 100, # 防守百回合
                                      np.float64(pstat[Statistic.TeamPtsGet] - pstat[Statistic.TeamPtsLost]) / pstat[Statistic.TeamPossessions] * 100, # 净胜百回合
                                      (np.float64(pstat[Statistic.TeamPtsGet] - pstat[Statistic.TeamPtsLost]) / pstat[Statistic.TeamPossessions]
                                            -np.float64(tstat[Statistic.TeamPtsGet] - pstat[Statistic.TeamPtsGet] - tstat[Statistic.TeamPtsLost] + pstat[Statistic.TeamPtsLost]) / (tstat[Statistic.TeamPossessions] - pstat[Statistic.TeamPossessions])) * 100,
                                      (np.float64(pstat[Statistic.TeamPtsGet]) / pstat[Statistic.TeamPossessions]
                                            -np.float64(tstat[Statistic.TeamPtsGet] - pstat[Statistic.TeamPtsGet]) / (tstat[Statistic.TeamPossessions] - pstat[Statistic.TeamPossessions])) * 100,
                                      (np.float64(pstat[Statistic.TeamPtsLost]) / pstat[Statistic.TeamPossessions]
                                            -np.float64(tstat[Statistic.TeamPtsLost] - pstat[Statistic.TeamPtsLost]) / (tstat[Statistic.TeamPossessions] - pstat[Statistic.TeamPossessions])) * 100,
                                      np.float64(pstat[Statistic.PersonalPossessions]) / pstat[Statistic.TeamPossessions], # 使用率
                                      np.float64(pstat[Statistic.Points]) / 2 / (pstat[Statistic.FieldGoalsAtt] + 0.44 * pstat[Statistic.FreeThrowsAtt]),
                                      np.float64(pstat[Statistic.ContestedShotMade]) / pstat[Statistic.GamePlayed], # 干扰
                                      np.float64(pstat[Statistic.ContestedShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.ContestedShotMade]) / pstat[Statistic.ContestedShotAtt],
                                      np.float64(pstat[Statistic.ContestedShotAtt]) / pstat[Statistic.FieldGoalsAtt],
                                      np.float64(pstat[Statistic.AssistedShotMade]) / pstat[Statistic.GamePlayed], # 接球攻
                                      np.float64(pstat[Statistic.AssistedShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.AssistedShotMade]) / pstat[Statistic.AssistedShotAtt],
                                      np.float64(pstat[Statistic.AssistedShotAtt]) / pstat[Statistic.FieldGoalsAtt],
                                      np.float64(pstat[Statistic.Assists]) / (pstat[Statistic.TeamShotsMade] - pstat[Statistic.FieldGoalsMade]),
                                      np.float64(pstat[Statistic.Assists]) / pstat[Statistic.Turnovers],
                                      np.float64(pstat[Statistic.OffRebounds]) / (pstat[Statistic.TeamOffRebounds] + pstat[Statistic.OppDefRebounds]), # 攻板率
                                      np.float64(pstat[Statistic.DefRebounds]) / (pstat[Statistic.TeamDefRebounds] + pstat[Statistic.OppOffRebounds]), # 防板率
                                      np.float64(pstat[Statistic.DefRebounds] + pstat[Statistic.OffRebounds]) / (pstat[Statistic.TeamDefRebounds] + pstat[Statistic.TeamOffRebounds] + pstat[Statistic.OppDefRebounds] + pstat[Statistic.OppOffRebounds]), # 总板率
                                      np.float64(pstat[Statistic.Turnovers]) / (pstat[Statistic.FieldGoalsAtt] + 0.44 * pstat[Statistic.FreeThrowsAtt] + pstat[Statistic.Turnovers]), # 失误率
                                      np.float64(pstat[Statistic.AssistInsideShotMade]) / pstat[Statistic.GamePlayed], # 传球给队友
                                      np.float64(pstat[Statistic.AssistInsideShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.AssistMidrangeShotMade]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.AssistMidRangeShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.AssistThreePointsMade]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.AssistThreePointsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.AssistInsideShotMade] + pstat[Statistic.AssistMidrangeShotMade] + pstat[Statistic.AssistThreePointsMade]) / pstat[Statistic.GamePlayed], # 总和
                                      np.float64(pstat[Statistic.AssistInsideShotAtt] + pstat[Statistic.AssistMidRangeShotAtt] + pstat[Statistic.AssistThreePointsAtt]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.AssistInsideShotMade] + pstat[Statistic.AssistMidrangeShotMade] + pstat[Statistic.AssistThreePointsMade]) / (pstat[Statistic.AssistInsideShotAtt] + pstat[Statistic.AssistMidRangeShotAtt] + pstat[Statistic.AssistThreePointsAtt]),
                                      np.float64(pstat[Statistic.ContestInsideShotMade]) / pstat[Statistic.GamePlayed], # 防守对位
                                      np.float64(pstat[Statistic.ContestInsideShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.ContestMidRangeShotMade]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.ContestMidRangeShotAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.ContestThreePointsMade]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.ContestThreePointsAtt]) / pstat[Statistic.GamePlayed],
                                      np.float64(pstat[Statistic.ContestInsideShotMade] + pstat[Statistic.ContestMidRangeShotMade] + pstat[Statistic.ContestThreePointsMade]) / pstat[Statistic.GamePlayed], # 总和
                                      np.float64(pstat[Statistic.ContestInsideShotAtt] + pstat[Statistic.ContestMidRangeShotAtt] + pstat[Statistic.ContestThreePointsAtt]) / pstat[Statistic.GamePlayed], 
                                      np.float64(pstat[Statistic.ContestInsideShotMade] + pstat[Statistic.ContestMidRangeShotMade] + pstat[Statistic.ContestThreePointsMade]) / (pstat[Statistic.ContestInsideShotAtt] + pstat[Statistic.ContestMidRangeShotAtt] + pstat[Statistic.ContestThreePointsAtt]),
                                      np.float64(pstat[Statistic.SecsPG]) / pstat[Statistic.Seconds],
                                      np.float64(pstat[Statistic.SecsSG]) / pstat[Statistic.Seconds],
                                      np.float64(pstat[Statistic.SecsSF]) / pstat[Statistic.Seconds],
                                      np.float64(pstat[Statistic.SecsPF]) / pstat[Statistic.Seconds],
                                      np.float64(pstat[Statistic.SecsC]) / pstat[Statistic.Seconds],
                                      
                                      ])
                table2.append([team.name + " " + str(team.id),
                    np.float64(tstat[Statistic.Seconds]) / 60 / tstat[Statistic.GamePlayed], # 分钟
                    np.float64(tstat[Statistic.Points]) / tstat[Statistic.GamePlayed], # 得分
                    np.float64(tstat[Statistic.TeamPtsLost]) / tstat[Statistic.GamePlayed], # 失分
                    np.float64(tstat[Statistic.FieldGoalsMade]) / tstat[Statistic.GamePlayed], # 投篮
                    np.float64(tstat[Statistic.FieldGoalsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.FieldGoalsMade]) / tstat[Statistic.FieldGoalsAtt],
                    np.float64(tstat[Statistic.InsideShotsMade]) / tstat[Statistic.GamePlayed], # 内投
                    np.float64(tstat[Statistic.InsideShotsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.InsideShotsMade]) / tstat[Statistic.InsideShotsAtt],
                    np.float64(tstat[Statistic.MidRangeShotsMade]) / tstat[Statistic.GamePlayed], # 中投
                    np.float64(tstat[Statistic.MidRangeShotsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.MidRangeShotsMade]) / tstat[Statistic.MidRangeShotsAtt],
                    np.float64(tstat[Statistic.ThreePointsMade]) / tstat[Statistic.GamePlayed], # 三分
                    np.float64(tstat[Statistic.ThreePointsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.ThreePointsMade]) / tstat[Statistic.ThreePointsAtt],
                    np.float64(tstat[Statistic.FreeThrowsMade]) / tstat[Statistic.GamePlayed], # 罚球
                    np.float64(tstat[Statistic.FreeThrowsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.FreeThrowsMade]) / tstat[Statistic.FreeThrowsAtt],
                    np.float64(tstat[Statistic.OffRebounds]) / tstat[Statistic.GamePlayed], # 篮板
                    np.float64(tstat[Statistic.DefRebounds]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.OffRebounds] + tstat[Statistic.DefRebounds]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.Assists]) / tstat[Statistic.GamePlayed], # 助攻
                    np.float64(tstat[Statistic.Turnovers]) / tstat[Statistic.GamePlayed], # 失误
                    np.float64(tstat[Statistic.Steals]) / tstat[Statistic.GamePlayed], # 抢断
                    np.float64(tstat[Statistic.Blocks]) / tstat[Statistic.GamePlayed], # 盖帽
                    np.float64(tstat[Statistic.Fouls]) / tstat[Statistic.GamePlayed], # 犯规
                    np.float64(tstat[Statistic.TeamPossessions]) / (tstat[Statistic.Seconds] / 60) * 48, # PACE
                    np.float64(tstat[Statistic.TeamPtsGet]) / tstat[Statistic.TeamPossessions] * 100, # 进攻百回合
                    np.float64(tstat[Statistic.TeamPtsLost]) / tstat[Statistic.TeamPossessions] * 100, # 防守百回合
                    np.float64(tstat[Statistic.TeamPtsGet] - tstat[Statistic.TeamPtsLost]) / tstat[Statistic.TeamPossessions] * 100, # 净胜百回合
                    np.float64(tstat[Statistic.Points]) / 2 / (tstat[Statistic.FieldGoalsAtt] + 0.44 * tstat[Statistic.FreeThrowsAtt]),
                    np.float64(tstat[Statistic.ContestedShotMade]) / tstat[Statistic.GamePlayed], # 干扰
                    np.float64(tstat[Statistic.ContestedShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.ContestedShotMade]) / tstat[Statistic.ContestedShotAtt],
                    np.float64(tstat[Statistic.ContestedShotAtt]) / tstat[Statistic.FieldGoalsAtt],
                    np.float64(tstat[Statistic.AssistedShotMade]) / tstat[Statistic.GamePlayed], # 接球攻
                    np.float64(tstat[Statistic.AssistedShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.AssistedShotMade]) / tstat[Statistic.AssistedShotAtt],
                    np.float64(tstat[Statistic.AssistedShotAtt]) / tstat[Statistic.FieldGoalsAtt],
                    np.float64(tstat[Statistic.Assists]) / tstat[Statistic.Turnovers],
                    np.float64(tstat[Statistic.OffRebounds]) / (tstat[Statistic.OffRebounds] + tstat[Statistic.OppDefRebounds]), # 攻板率
                    np.float64(tstat[Statistic.DefRebounds]) / (tstat[Statistic.DefRebounds] + tstat[Statistic.OppOffRebounds]), # 防板率
                    np.float64(tstat[Statistic.DefRebounds] + tstat[Statistic.OffRebounds]) / (tstat[Statistic.DefRebounds] + tstat[Statistic.OffRebounds] + tstat[Statistic.OppDefRebounds] + tstat[Statistic.OppOffRebounds]), # 总板率
                    np.float64(tstat[Statistic.Turnovers]) / (tstat[Statistic.FieldGoalsAtt] + 0.44 * tstat[Statistic.FreeThrowsAtt] + tstat[Statistic.Turnovers]), # 失误率
                    np.float64(tstat[Statistic.AssistInsideShotMade]) / tstat[Statistic.GamePlayed], # 传球给队友
                    np.float64(tstat[Statistic.AssistInsideShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.AssistMidrangeShotMade]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.AssistMidRangeShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.AssistThreePointsMade]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.AssistThreePointsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.AssistInsideShotMade] + tstat[Statistic.AssistMidrangeShotMade] + tstat[Statistic.AssistThreePointsMade]) / tstat[Statistic.GamePlayed], # 总和
                    np.float64(tstat[Statistic.AssistInsideShotAtt] + tstat[Statistic.AssistMidRangeShotAtt] + tstat[Statistic.AssistThreePointsAtt]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.AssistInsideShotMade] + tstat[Statistic.AssistMidrangeShotMade] + tstat[Statistic.AssistThreePointsMade]) / (tstat[Statistic.AssistInsideShotAtt] + tstat[Statistic.AssistMidRangeShotAtt] + tstat[Statistic.AssistThreePointsAtt]),
                    np.float64(tstat[Statistic.ContestInsideShotMade]) / tstat[Statistic.GamePlayed], # 防守对位
                    np.float64(tstat[Statistic.ContestInsideShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.ContestMidRangeShotMade]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.ContestMidRangeShotAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.ContestThreePointsMade]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.ContestThreePointsAtt]) / tstat[Statistic.GamePlayed],
                    np.float64(tstat[Statistic.ContestInsideShotMade] + tstat[Statistic.ContestMidRangeShotMade] + tstat[Statistic.ContestThreePointsMade]) / tstat[Statistic.GamePlayed], # 总和
                    np.float64(tstat[Statistic.ContestInsideShotAtt] + tstat[Statistic.ContestMidRangeShotAtt] + tstat[Statistic.ContestThreePointsAtt]) / tstat[Statistic.GamePlayed], 
                    np.float64(tstat[Statistic.ContestInsideShotMade] + tstat[Statistic.ContestMidRangeShotMade] + tstat[Statistic.ContestThreePointsMade]) / (tstat[Statistic.ContestInsideShotAtt] + tstat[Statistic.ContestMidRangeShotAtt] + tstat[Statistic.ContestThreePointsAtt]),
                                     
                    ]
                )
           
           
           
            # Player stats
            df1 = pd.DataFrame(table1, columns=headers)
            df1 = df1.fillna(0)
            df1 = df1[df1['出场次数'] >= gamelimit]
            df1 = df1[df1['分钟'] >= minutelimit]
            df1 = df1.sort_values(by=['得分'], ascending=False)
            df1.to_excel(
                        writer,
                        sheet_name="Players",
                        index=False,
                        header=False,
                        startrow=1,
                        freeze_panes=(1, 2),
                    )
            worksheet1 = writer.sheets['Players']
            for colx, value in enumerate(df1.columns.values):
                worksheet1.write(0, colx, value)
            
            for column in df1:
                column_length = max(df1[column].astype(str).map(len).max(), len(column)) + 1
                col_idx = df1.columns.get_loc(column)
                worksheet1.set_column(col_idx, col_idx, column_length)
            workbook = writer.book
            text_format = workbook.add_format({'text_wrap': True, 'bold': True})
            num_format_1 = workbook.add_format({'num_format': '0.0'})
            num_format_2 = workbook.add_format({'num_format': '0.00'})
            num_format_3 = workbook.add_format({'num_format': '0.000'})

            worksheet1.set_row(0, 40, text_format)
            for col_idx in [*range(3,7), 8, 9, 11, 12, 14, 15, 17, 18,
                        *range(20,34), 36, 37, 40, 41, *range(50,58),
                        *range(59,67)]:
                worksheet1.set_column(col_idx, col_idx, None, num_format_1)
            for col_idx in [7, 10, 13, 16, 19, 34, 35, 38, 39,
                        *range(42,50), 58, 67]:
                worksheet1.set_column(col_idx, col_idx, None, num_format_3)
            for col_idx in [45, *range(68,73)]:
                worksheet1.set_column(col_idx, col_idx, None, num_format_2)
            worksheet1.autofilter(0, 0, df1.shape[0], df1.shape[1] - 1)

            # Team stats
            df2 = pd.DataFrame(table2, columns=headers_team)
            df2 = df2.fillna(0)
            df2 = df2.sort_values(by=['百回合净胜分'], ascending=False)
            df2.to_excel(
                        writer,
                        sheet_name="Teams",
                        index=False,
                        header=False,
                        startrow=1,
                        freeze_panes=(1, 1),
                    )
            worksheet2 = writer.sheets['Teams']
            for colx, value in enumerate(df2.columns.values):
                worksheet2.write(0, colx, value)
            
            for column in df2:
                column_length = max(df2[column].astype(str).map(len).max(), len(column)) + 1
                col_idx = df2.columns.get_loc(column)
                worksheet2.set_column(col_idx, col_idx, column_length)

            worksheet2.set_row(0, 40, text_format)
            for col_idx in range(1,62):
                worksheet2.set_column(col_idx, col_idx, None, num_format_1)
            for col_idx in [6, 9, 12, 15, 18, 31, 34, 35,
                        *range(38,45), 53, 62]:
                worksheet2.set_column(col_idx, col_idx, None, num_format_3)
            for col_idx in [40,]:
                worksheet2.set_column(col_idx, col_idx, None, num_format_2)
            worksheet2.autofilter(0, 0, df2.shape[0], df2.shape[1] - 1)


        
def fetch_data(username: str, password: str, leagueid: int, seasonid: int, gamelimit: int, minutelimit: int):
    api = BBApi(username, password)

    unique_ids = set[str]()

    team_ids = api.standings(leagueid, seasonid)
    print(f"Season {seasonid}: teams: {len(team_ids)}")
    for team_id in team_ids:
        match_ids = api.schedule(team_id, seasonid)
        unique_ids.update(match_ids)
        print(f"LeagueID: {leagueid}, Season {seasonid}: matches: {len(match_ids)}")

    with open("uids-various.txt", "w", encoding='utf-8') as f:
        for index, uid in enumerate(unique_ids):
            print(f"Fetch {uid} ({index+1}/{len(unique_ids)})")
            f.write(str(uid) + "\n")
    
    season = Season(leagueid, seasonid)
    for index, uid in enumerate(unique_ids):
        text = get_xml_text(uid)
        try:
            events, ht, at = parse_xml(text)
        except:
            continue
        arg_game = argparse.Namespace(username = username, password = password, print_events=False, print_stats=False, save_charts=False, verify=False)
        game = Game(uid, events, ht, at, arg_game, [])
        season.import_game(game, gamelimit, minutelimit)
        print(f"Game {uid} analyzed ({index+1}/{len(unique_ids)})")
    
    season.generate_season_report_players(gamelimit, minutelimit)
        
    pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--leagueid", type=int, required=True)
    parser.add_argument("--season", type=int, required=True)
    parser.add_argument("--gamelimit", type=float, default=1)
    parser.add_argument("--minutelimit", type=float, default=5)
    args = parser.parse_args()

    fetch_data(
        args.username, args.password, args.leagueid, args.season, args.gamelimit, args.minutelimit
    )
    
    