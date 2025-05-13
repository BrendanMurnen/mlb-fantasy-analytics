--- stg_batting_stats
with
  batting_stats as (
    select
      mlbID,
      strip_accents(decode( replace(name, E'\\\'', '''')::blob ) ) as player_name,
      age,
      Team,
      Season,

      -- Fantasy Points Algorithm
      (-1 * coalesce(CS, 0))
        + (2 * coalesce(doubles, 0))
        -- + (-1 * coalesce(E, 0))
        + (1 * coalesce(HBP, 0))
        + (4 * coalesce(HR, 0))
        + (1 * coalesce(RBI, 0))
        + (1 * coalesce(R, 0))
        + (1 * (
            coalesce(H, 0)
            - coalesce(doubles, 0)
            - coalesce(triples, 0)
            - coalesce(HR, 0)
            )
          ) -- derived Singles
        + (1 * coalesce(SB, 0))
        + (-1 * coalesce(SO, 0))
        + (3 * coalesce(triples, 0))
        + (1 * coalesce(BB, 0))
        as fantasy_points,

      Games,
      PA,
      AB,
      R,
      H,
      doubles,
      triples,
      HR,
      RBI,
      BB,
      IBB,
      SO,
      HBP,
      SH,
      SF,
      GDP,
      SB,
      CS,
      BA,
      OBP,
      SLG,
      OPS
    from source_bref__batting_stats
  )

  , roster_assignments as (
    select
      player_name
      , team_name as fantasy_team_name
      , team_id as fantasy_team_id
    from source_fantrax__roster_assignments
  )

select
  *
  , fantasy_team_id is not null as is_rostered
from batting_stats
left join roster_assignments using (player_name)
