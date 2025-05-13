-- stg_pitching_stats
with
  pitching_stats as (
    select
      mlbID,
      strip_accents(decode( replace(name, E'\\\'', '''')::blob ) ) as player_name,
      age,
      team,
      season,

      -- Fantasy Points Algorithm
      (-2 * coalesce(ER, 0))
        + (-1 * coalesce(H, 0))
        -- + (2 * coalesce(HLD, 0))
        + (3 * round(coalesce(IP, 0)) ) -- get base IP
        + (1 * ((coalesce(IP, 0) * 10) % 10) ) -- get partial innings totals
        + (-2 * coalesce(L, 0))
        -- + (3 * coalesce(QS, 0))
        + (3 * coalesce(SV, 0))
        + (1 * coalesce(SO, 0))
        + (-1 * coalesce(BB, 0))
        + (2 * coalesce(W, 0))
      as fantasy_points,

      G,
      GS,
      W,
      L,
      SV,
      IP,
      H,
      R,
      ER,
      BB,
      SO,
      HR,
      HBP,
      ERA,
      AB,
      doubles,
      triples,
      IBB,
      GDP,
      SF,
      SB,
      CS,
      WHIP,
      SO9,
      SOW
    from source_bref__pitching_stats
  )

  , roster_assignments as (
    select
      case
        when player_name = 'J.P. Sears' then 'JP Sears'
        when player_name = 'Nestor Cortes Jr.' then 'Nestor Cortes'
        else player_name
      end as player_name
      , team_name as fantasy_team_name
      , team_id as fantasy_team_id
    from source_fantrax__roster_assignments
  )

select
  *
  , fantasy_team_id is not null as is_rostered
from pitching_stats
left join roster_assignments using (player_name)
