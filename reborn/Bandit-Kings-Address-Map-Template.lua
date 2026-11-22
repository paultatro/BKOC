-- Bandit Kings Reborn: Address Map Template
-- Paste confirmed values into the CONFIG.addresses block in
-- bandit-kings-reborn-director.lua. Keep unknown values nil or 0.
-- For the first real test, set dry_run = true in the director.

addresses = {
  -- Required for month-triggered director events.
  month = nil,

  -- Read-only ownership map; needed by the default rival guard.
  -- Each owner row must describe the SAME entity as each rival stat row.
  player_owner = nil,
  enemy_owner_start = nil,
  enemy_owner_count = 0,
  enemy_owner_stride = 1,

  -- Player values. Start with gold, food, and troops.
  player_gold = nil,
  player_food = nil,
  player_popularity = nil,
  player_ruler_health = nil,
  player_ruler_loyalty = nil,
  player_troops = nil,
  player_training = nil,

  -- Enemy tables. Use stride = 1 when values are adjacent.
  enemy_gold_start = nil,
  enemy_gold_count = 0,
  enemy_gold_stride = 1,

  enemy_food_start = nil,
  enemy_food_count = 0,
  enemy_food_stride = 1,

  enemy_troops_start = nil,
  enemy_troops_count = 0,
  enemy_troops_stride = 1,

  enemy_loyalty_start = nil,
  enemy_loyalty_count = 0,
  enemy_loyalty_stride = 1
}

-- Example only:
--
-- addresses = {
--   month = 0x0140,
--   player_gold = 0x0152,
--   player_food = 0x0153,
--   player_troops = 0x0154,
--   player_training = nil,
--   player_popularity = nil,
--   player_ruler_health = nil,
--   player_ruler_loyalty = nil,
--   enemy_gold_start = 0x0220,
--   enemy_gold_count = 12,
--   enemy_gold_stride = 8,
--   enemy_food_start = nil,
--   enemy_food_count = 0,
--   enemy_food_stride = 1,
--   enemy_troops_start = 0x0222,
--   enemy_troops_count = 12,
--   enemy_troops_stride = 8,
--   enemy_loyalty_start = nil,
--   enemy_loyalty_count = 0,
--   enemy_loyalty_stride = 1
-- }
