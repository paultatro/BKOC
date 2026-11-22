-- Bandit Kings Reborn 0.3: Council and Chronicle for Mesen
-- Fill CONFIG.addresses after using bandit-kings-memory-scout.lua.
-- The script is intentionally data-driven so you can tune it without ROM hacking.

local CONFIG = {
  seed = 0x1989,
  enabled = true,
  dry_run = true,
  dry_run_audit_limit = 20,
  difficulty = 3, -- 1: spicy, 2: hard, 3: veteran, 4: cruel
  show_overlay = true,
  month_cooldown_frames = 90,
  doctrine_mode = "adaptive", -- adaptive, hoarder, raider, conspirator, storm
  self_test = false,
  self_test_month_frames = 120,
  max_events_per_month = 3,
  -- This is now a hard cap, including policy and recovery events.
  policy = "balanced", -- balanced, provision, patronage, drill
  policy_key = "P", -- Cycle the policy for the NEXT month.
  chronicle_key = "H", -- Toggle the readable campaign history.
  overlay_key = "O", -- Toggle the overlay without stopping events.
  chronicle_limit = 128,
  event_repeat_gap = 1, -- At least one intervening month between repeats.
  recovery_food_threshold = 18,
  recovery_troops_threshold = 18,
  require_enemy_ownership = true,
  neutral_owner_values = { 0, 255 }, -- Calibrate these for your ROM.
  month_min = 1, -- Use 0/11 for a verified zero-based month field.
  month_max = 12,
  month_stable_frames = 3,
  campaign_twists = true,
  twist_duration_months = 6,
  twist_mode = "adaptive", -- adaptive, thin_harvest, bandit_surge, merchant_war, court_fever, mandate_drift
  nemesis_rivals = false, -- Enable only after confirming matching rival order in every table.
  nemesis_duration_months = 8,
  nemesis_bonus = 2,
  habit_breakers = true,
  habit_threshold_months = 3,
  validate_on_load = true,

  -- Replace these placeholders with discovered RAM addresses.
  -- Unknown addresses can stay nil; matching systems will quietly disable themselves.
  addresses = {
    month = nil,
    player_owner = nil, -- Read-only current player faction ID.
    enemy_owner_start = nil, -- Read-only faction IDs in matching rival order.
    enemy_owner_count = 0,
    enemy_owner_stride = 1,
    player_gold = nil,
    player_food = nil,
    player_popularity = nil,
    player_ruler_health = nil,
    player_ruler_loyalty = nil,
    player_troops = nil,
    player_training = nil,
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
}

local cpu = emu.memType.nesDebug or emu.memType.cpuDebug or emu.memType.nesMemory or emu.memType.cpu
local cpu_write = emu.memType.nesMemory or emu.memType.cpu
local frame = 0
local last_month = nil
local last_month_event_frame = -9999
local pressure = 0
local threat_clock = 0
local doctrine = "adaptive"
local twist = "none"
local twist_months_left = 0
local nemesis_index = nil
local nemesis_months_left = 0
local hoard_streak = 0
local army_streak = 0
local soft_streak = 0
local habit_heat = 0
local event_log = {}
local rng_state = CONFIG.seed
local fake_memory = {}
local dry_run_write_count = 0
local dry_run_writes = {}
local dry_run_shadow = {}
local mutation_count = 0
local event_start_mutations = nil
local campaign_month = 0
local chronicle = {}
local show_chronicle = false
local selected_policy = CONFIG.policy
local paid_policy = "balanced"
local pending_crisis = nil
local recovery_until = 0
local last_event_month = {}
local previous_keys = {}
local candidate_month, candidate_frames = nil, 0
local recovering = false
local last_events_used = 0
local last_budget = 0

local function safe_log(text)
  if emu.log then emu.log(text) end
end

local function safe_draw_rectangle(x, y, width, height, color, fill)
  if emu.drawRectangle then pcall(emu.drawRectangle, x, y, width, height, color, fill) end
end

local function safe_draw_string(x, y, text, color, background)
  if emu.drawString then pcall(emu.drawString, x, y, text:sub(1, 40), color, background) end
end

local function rand(max)
  rng_state = (rng_state * 16807) % 2147483647
  return (rng_state % max) + 1
end

local function choose(list)
  return list[rand(#list)]
end

local function clamp(value, lo, hi)
  if value < lo then return lo end
  if value > hi then return hi end
  return value
end

local function byte(value)
  return value % 256
end

local function read_byte(addr)
  if not addr then return nil end
  if CONFIG.self_test then return fake_memory[addr] or 0 end
  if CONFIG.dry_run and dry_run_shadow[addr] ~= nil then return dry_run_shadow[addr] end
  return byte(emu.read(addr, cpu))
end

local function write_byte(addr, value, floor, ceiling)
  if not addr then return end
  local clamped = clamp(value, floor or 0, ceiling or 255)
  local old_value = read_byte(addr)
  if old_value == clamped then return end
  mutation_count = mutation_count + 1
  if CONFIG.self_test then
    fake_memory[addr] = clamped
    return
  end
  if CONFIG.dry_run then
    dry_run_shadow[addr] = clamped
    dry_run_write_count = dry_run_write_count + 1
    dry_run_writes[#dry_run_writes + 1] = { addr = addr, old = old_value, value = clamped, frame = frame }
    while #dry_run_writes > CONFIG.dry_run_audit_limit do
      table.remove(dry_run_writes, 1)
    end
    return
  end
  emu.write(addr, clamped, cpu_write)
end

local function add_log(text)
  if event_start_mutations and mutation_count == event_start_mutations then return end
  local mode = CONFIG.self_test and "DEMO" or (CONFIG.dry_run and "DRY" or "LIVE")
  chronicle[#chronicle + 1] = { month = campaign_month, mode = mode, text = text }
  while #chronicle > CONFIG.chronicle_limit do table.remove(chronicle, 1) end
  event_log[#event_log + 1] = text
  while #event_log > 4 do
    table.remove(event_log, 1)
  end
  safe_log(string.format("[BKR %s M%03d] %s", mode, campaign_month, text))
end

local function has_range(start_addr, count)
  return start_addr ~= nil and count ~= nil and count > 0
end

local function label_from_range(addr, label, start_addr, count, stride)
  if not has_range(start_addr, count) then return nil end
  stride = stride or 1
  for i = 0, count - 1 do
    if addr == start_addr + i * stride then
      return label .. "[" .. tostring(i + 1) .. "]"
    end
  end
  return nil
end

local function describe_address(addr)
  local exact = {
    { label = "month", addr = CONFIG.addresses.month },
    { label = "player_gold", addr = CONFIG.addresses.player_gold },
    { label = "player_food", addr = CONFIG.addresses.player_food },
    { label = "player_popularity", addr = CONFIG.addresses.player_popularity },
    { label = "player_ruler_health", addr = CONFIG.addresses.player_ruler_health },
    { label = "player_ruler_loyalty", addr = CONFIG.addresses.player_ruler_loyalty },
    { label = "player_troops", addr = CONFIG.addresses.player_troops },
    { label = "player_training", addr = CONFIG.addresses.player_training }
  }

  for _, row in ipairs(exact) do
    if row.addr and addr == row.addr then return row.label end
  end

  return label_from_range(addr, "enemy_gold", CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, CONFIG.addresses.enemy_gold_stride) or
    label_from_range(addr, "enemy_food", CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count, CONFIG.addresses.enemy_food_stride) or
    label_from_range(addr, "enemy_troops", CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, CONFIG.addresses.enemy_troops_stride) or
    label_from_range(addr, "enemy_loyalty", CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, CONFIG.addresses.enemy_loyalty_stride) or
    "unmapped"
end

local function configured_system_count()
  local count = 0
  if CONFIG.addresses.month then count = count + 1 end
  if CONFIG.addresses.player_gold then count = count + 1 end
  if CONFIG.addresses.player_food then count = count + 1 end
  if CONFIG.addresses.player_troops then count = count + 1 end
  if CONFIG.addresses.player_training then count = count + 1 end
  if CONFIG.addresses.player_popularity then count = count + 1 end
  if has_range(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count) then count = count + 1 end
  if has_range(CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count) then count = count + 1 end
  if has_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count) then count = count + 1 end
  if has_range(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count) then count = count + 1 end
  return count
end

local function validate_range(label, start_addr, count, stride)
  if count and count > 0 and not start_addr then
    safe_log("[BKR config] " .. label .. " has count but no start address")
  end
  if start_addr and (not count or count <= 0) then
    safe_log("[BKR config] " .. label .. " has start address but count is 0")
  end
  if stride and stride <= 0 then
    safe_log("[BKR config] " .. label .. " stride must be 1 or higher")
  end
end

local function in_list(value, list)
  for _, item in ipairs(list) do
    if value == item then return true end
  end
  return false
end

local function validate_config()
  if CONFIG.self_test then
    safe_log("[BKR config] self-test mode is ON; real game RAM will not be touched")
    return
  end

  if CONFIG.dry_run then
    safe_log("[BKR config] dry-run mode is ON; real game RAM will be read but not changed")
  end

  if not CONFIG.addresses.month then
    safe_log("[BKR config] month address is missing; monthly director events are disabled")
  end

  if CONFIG.campaign_twists and CONFIG.twist_duration_months < 1 then
    safe_log("[BKR config] twist_duration_months must be 1 or higher")
  end

  if CONFIG.nemesis_rivals and CONFIG.nemesis_duration_months < 1 then
    safe_log("[BKR config] nemesis_duration_months must be 1 or higher")
  end

  if CONFIG.habit_breakers and CONFIG.habit_threshold_months < 1 then
    safe_log("[BKR config] habit_threshold_months must be 1 or higher")
  end

  if not in_list(CONFIG.doctrine_mode, { "adaptive", "hoarder", "raider", "conspirator", "storm" }) then
    safe_log("[BKR config] unknown doctrine_mode: " .. tostring(CONFIG.doctrine_mode))
  end

  if not in_list(CONFIG.twist_mode, { "adaptive", "thin_harvest", "bandit_surge", "merchant_war", "court_fever", "mandate_drift" }) then
    safe_log("[BKR config] unknown twist_mode: " .. tostring(CONFIG.twist_mode))
  end

  local player_core = 0
  if CONFIG.addresses.player_gold then player_core = player_core + 1 end
  if CONFIG.addresses.player_food then player_core = player_core + 1 end
  if CONFIG.addresses.player_troops then player_core = player_core + 1 end
  if player_core == 0 then
    safe_log("[BKR config] no core player economy/troop addresses are set")
  elseif player_core < 3 then
    safe_log("[BKR config] partial core player map; pressure will be approximate")
  end

  validate_range("enemy_gold", CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, CONFIG.addresses.enemy_gold_stride)
  validate_range("enemy_food", CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count, CONFIG.addresses.enemy_food_stride)
  validate_range("enemy_troops", CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, CONFIG.addresses.enemy_troops_stride)
  validate_range("enemy_loyalty", CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, CONFIG.addresses.enemy_loyalty_stride)
end

-- Never strengthen a captured/neutral slot when a live ownership map exists.
-- This guard is evaluated for EVERY affected row, not just when a nemesis rises.
local function enemy_eligible(index)
  local a = CONFIG.addresses
  if a.player_owner and a.enemy_owner_start then
    if index > a.enemy_owner_count then return false end
    local owner = read_byte(a.enemy_owner_start + (index - 1) * a.enemy_owner_stride)
    local player = read_byte(a.player_owner)
    return owner ~= nil and player ~= nil and owner ~= player and
      not in_list(owner, CONFIG.neutral_owner_values)
  end
  return not CONFIG.require_enemy_ownership
end

local function add_range(start_addr, count, delta, floor, ceiling, stride)
  if not start_addr or count <= 0 then return end
  stride = stride or 1
  for i = 0, count - 1 do
    local addr = start_addr + i * stride
    local value = read_byte(addr)
    if value and enemy_eligible(i + 1) then
      write_byte(addr, math.max(value, value + delta), floor or 0, math.max(value, ceiling or 255))
    end
  end
end

local function add_table_index(start_addr, count, index, delta, floor, ceiling, stride)
  if not start_addr or not count or count <= 0 or not index then return false end
  if index < 1 or index > count or not enemy_eligible(index) then return false end
  stride = stride or 1
  local addr = start_addr + (index - 1) * stride
  local value = read_byte(addr)
  if not value then return false end
  write_byte(addr, math.max(value, value + delta), floor or 0, math.max(value, ceiling or 255))
  return true
end

local function nemesis_pool_size()
  local count = 0
  if has_range(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count) and CONFIG.addresses.enemy_gold_count > count then
    count = CONFIG.addresses.enemy_gold_count
  end
  if has_range(CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count) and CONFIG.addresses.enemy_food_count > count then
    count = CONFIG.addresses.enemy_food_count
  end
  if has_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count) and CONFIG.addresses.enemy_troops_count > count then
    count = CONFIG.addresses.enemy_troops_count
  end
  if has_range(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count) and CONFIG.addresses.enemy_loyalty_count > count then
    count = CONFIG.addresses.enemy_loyalty_count
  end
  return count
end

local function set_nemesis()
  if not CONFIG.nemesis_rivals then
    nemesis_index = nil
    nemesis_months_left = 0
    return
  end

  if nemesis_index and enemy_eligible(nemesis_index) and nemesis_months_left > 0 then
    nemesis_months_left = nemesis_months_left - 1
    return
  end

  local count = nemesis_pool_size()
  if count <= 0 then
    nemesis_index = nil
    nemesis_months_left = 0
    return
  end

  local eligible = {}
  for i = 1, count do
    if enemy_eligible(i) then eligible[#eligible + 1] = i end
  end
  if #eligible == 0 then
    nemesis_index, nemesis_months_left = nil, 0
    return
  end
  nemesis_index = choose(eligible)
  nemesis_months_left = CONFIG.nemesis_duration_months - 1
  add_log("Nemesis rival rises at table slot " .. tostring(nemesis_index))
end

local function set_doctrine()
  if CONFIG.doctrine_mode ~= "adaptive" then
    doctrine = CONFIG.doctrine_mode
    return
  end

  local roll = rand(100)
  if pressure >= 7 then
    doctrine = choose({ "raider", "conspirator", "storm" })
  elseif pressure >= 4 then
    doctrine = choose({ "hoarder", "raider", "conspirator" })
  elseif roll <= 40 then
    doctrine = "hoarder"
  elseif roll <= 70 then
    doctrine = "raider"
  else
    doctrine = "conspirator"
  end
end

local function set_twist()
  if not CONFIG.campaign_twists then
    twist = "none"
    twist_months_left = 0
    return
  end

  if twist_months_left > 0 then
    twist_months_left = twist_months_left - 1
    return
  end

  if CONFIG.twist_mode ~= "adaptive" then
    twist = CONFIG.twist_mode
  elseif pressure >= 7 then
    twist = choose({ "thin_harvest", "bandit_surge", "court_fever", "mandate_drift" })
  elseif pressure >= 4 then
    twist = choose({ "bandit_surge", "merchant_war", "court_fever" })
  else
    twist = choose({ "merchant_war", "thin_harvest", "mandate_drift" })
  end

  twist_months_left = CONFIG.twist_duration_months - 1
  add_log("New campaign twist: " .. twist)
end

local function player_score()
  local gold = read_byte(CONFIG.addresses.player_gold) or 0
  local food = read_byte(CONFIG.addresses.player_food) or 0
  local troops = read_byte(CONFIG.addresses.player_troops) or 0
  local training = read_byte(CONFIG.addresses.player_training) or 0
  local popularity = read_byte(CONFIG.addresses.player_popularity) or 0

  return gold + food + troops + math.floor(training / 2) + math.floor(popularity / 2)
end

local function track_habits()
  if not CONFIG.habit_breakers then
    hoard_streak = 0
    army_streak = 0
    soft_streak = 0
    habit_heat = 0
    return
  end

  local gold = read_byte(CONFIG.addresses.player_gold)
  local food = read_byte(CONFIG.addresses.player_food)
  local troops = read_byte(CONFIG.addresses.player_troops)
  local popularity = read_byte(CONFIG.addresses.player_popularity)
  local loyalty = read_byte(CONFIG.addresses.player_ruler_loyalty)

  if gold and food and gold >= 95 and food >= 95 then
    hoard_streak = math.min(hoard_streak + 1, 12)
  else
    hoard_streak = math.floor(hoard_streak / 2)
  end

  if troops and troops >= 105 then
    army_streak = math.min(army_streak + 1, 12)
  else
    army_streak = math.floor(army_streak / 2)
  end

  if (popularity and popularity <= 35) or (loyalty and loyalty <= 35) then
    soft_streak = math.min(soft_streak + 1, 12)
  else
    soft_streak = math.floor(soft_streak / 2)
  end

  habit_heat = clamp(hoard_streak + army_streak + soft_streak, 0, 9)
end

local function habit_breaker_event()
  if not CONFIG.habit_breakers then return end

  local threshold = CONFIG.habit_threshold_months
  if hoard_streak < threshold and army_streak < threshold and soft_streak < threshold then return end

  if hoard_streak >= threshold and hoard_streak >= army_streak and hoard_streak >= soft_streak and CONFIG.addresses.player_gold then
    local loss = 2 + CONFIG.difficulty + math.floor(hoard_streak / 2)
    write_byte(CONFIG.addresses.player_gold, (read_byte(CONFIG.addresses.player_gold) or 0) - loss)
    if CONFIG.addresses.player_food then
      write_byte(CONFIG.addresses.player_food, (read_byte(CONFIG.addresses.player_food) or 0) - math.floor(loss / 2))
    end
    add_log("Hoarded stores draw thieves -" .. tostring(loss))
    hoard_streak = math.floor(hoard_streak / 2)
  elseif army_streak >= threshold and army_streak >= soft_streak and CONFIG.addresses.player_food then
    local loss = 2 + CONFIG.difficulty + math.floor(army_streak / 2)
    write_byte(CONFIG.addresses.player_food, (read_byte(CONFIG.addresses.player_food) or 0) - loss)
    if CONFIG.addresses.player_training then
      write_byte(CONFIG.addresses.player_training, (read_byte(CONFIG.addresses.player_training) or 0) - 1)
    end
    add_log("Idle army camps devour supplies -" .. tostring(loss))
    army_streak = math.floor(army_streak / 2)
  elseif soft_streak >= threshold and (CONFIG.addresses.player_popularity or CONFIG.addresses.player_ruler_loyalty) then
    local loss = 1 + math.floor(soft_streak / 3)
    if CONFIG.addresses.player_popularity then
      write_byte(CONFIG.addresses.player_popularity, (read_byte(CONFIG.addresses.player_popularity) or 0) - loss)
    end
    if CONFIG.addresses.player_ruler_loyalty then
      write_byte(CONFIG.addresses.player_ruler_loyalty, (read_byte(CONFIG.addresses.player_ruler_loyalty) or 0) - 1)
    end
    add_log("Neglected courts invite dissent -" .. tostring(loss))
    soft_streak = math.floor(soft_streak / 2)
  end

  habit_heat = clamp(hoard_streak + army_streak + soft_streak, 0, 9)
end

local function mutate_enemy_economy()
  local boost = CONFIG.difficulty + math.floor(pressure / 3)
  if doctrine == "hoarder" then boost = boost + 2 end
  if twist == "merchant_war" then boost = boost + 2 end
  add_range(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, boost, 0, 220, CONFIG.addresses.enemy_gold_stride)
  add_range(CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count, boost, 0, 220, CONFIG.addresses.enemy_food_stride)
  if nemesis_index then
    add_table_index(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, nemesis_index, CONFIG.nemesis_bonus, 0, 235, CONFIG.addresses.enemy_gold_stride)
    add_table_index(CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count, nemesis_index, CONFIG.nemesis_bonus, 0, 235, CONFIG.addresses.enemy_food_stride)
  end
  add_log("Hoarder rivals stockpile supplies +" .. tostring(boost))
end

local function mutate_enemy_armies()
  local boost = 1 + CONFIG.difficulty + math.floor(pressure / 2)
  if doctrine == "raider" then boost = boost + 2 end
  if twist == "bandit_surge" then boost = boost + 2 end
  add_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, boost, 0, 240, CONFIG.addresses.enemy_troops_stride)
  add_range(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, 1, 0, 100, CONFIG.addresses.enemy_loyalty_stride)
  if nemesis_index then
    add_table_index(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, nemesis_index, CONFIG.nemesis_bonus, 0, 250, CONFIG.addresses.enemy_troops_stride)
    add_table_index(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, nemesis_index, 1, 0, 100, CONFIG.addresses.enemy_loyalty_stride)
  end
  add_log("Raider commanders drill harder +" .. tostring(boost))
end

local function nemesis_pressure()
  if not nemesis_index then return end
  local boost = CONFIG.nemesis_bonus + math.floor(pressure / 3)
  local hit = false

  if doctrine == "hoarder" or twist == "merchant_war" then
    hit = add_table_index(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, nemesis_index, boost, 0, 240, CONFIG.addresses.enemy_gold_stride) or hit
    hit = add_table_index(CONFIG.addresses.enemy_food_start, CONFIG.addresses.enemy_food_count, nemesis_index, boost, 0, 240, CONFIG.addresses.enemy_food_stride) or hit
  elseif doctrine == "conspirator" or twist == "court_fever" then
    hit = add_table_index(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, nemesis_index, 2, 0, 100, CONFIG.addresses.enemy_loyalty_stride) or hit
    hit = add_table_index(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, nemesis_index, 1, 0, 240, CONFIG.addresses.enemy_gold_stride) or hit
  else
    hit = add_table_index(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, nemesis_index, boost, 0, 250, CONFIG.addresses.enemy_troops_stride) or hit
    hit = add_table_index(CONFIG.addresses.enemy_loyalty_start, CONFIG.addresses.enemy_loyalty_count, nemesis_index, 1, 0, 100, CONFIG.addresses.enemy_loyalty_stride) or hit
  end

  if hit then add_log("Nemesis rival sharpens at slot " .. tostring(nemesis_index)) end
end

local function coalition_pulse()
  if not has_range(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count) and
     not has_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count) then
    return
  end

  local boost = 1 + math.floor(pressure / 2)
  add_range(CONFIG.addresses.enemy_gold_start, CONFIG.addresses.enemy_gold_count, boost, 0, 230, CONFIG.addresses.enemy_gold_stride)
  add_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, boost, 0, 245, CONFIG.addresses.enemy_troops_stride)
  add_log("A quiet coalition shares men and coin")
end

local function overextension_tax()
  local troops = read_byte(CONFIG.addresses.player_troops) or 0
  local food = read_byte(CONFIG.addresses.player_food) or 0
  if troops > 90 and food > 0 then
    local loss = clamp(math.floor(troops / 32), 1, 6)
    if twist == "thin_harvest" then loss = loss + 1 end
    write_byte(CONFIG.addresses.player_food, food - loss)
    add_log("Huge armies strain supply -" .. tostring(loss))
  end
end

local function loyalty_conspiracy()
  local loss = 1 + math.floor(pressure / 4)
  if twist == "court_fever" or twist == "mandate_drift" then loss = loss + 1 end
  local hit = false

  if CONFIG.addresses.player_popularity then
    write_byte(CONFIG.addresses.player_popularity, (read_byte(CONFIG.addresses.player_popularity) or 0) - loss)
    hit = true
  end
  if CONFIG.addresses.player_ruler_loyalty then
    write_byte(CONFIG.addresses.player_ruler_loyalty, (read_byte(CONFIG.addresses.player_ruler_loyalty) or 0) - 1)
    hit = true
  end
  if hit then add_log("Conspirators poison court trust -" .. tostring(loss)) end
end

local function seasonal_shock(forced_shock)
  local shock = forced_shock or choose({ "famine", "levy", "bad_omens" })
  if not forced_shock then
    if twist == "thin_harvest" then shock = "famine" end
    if twist == "bandit_surge" then shock = "levy" end
    if twist == "mandate_drift" then shock = "bad_omens" end
  end
  if shock == "famine" and CONFIG.addresses.player_food then
    local loss = 3 + CONFIG.difficulty + math.floor(pressure / 2)
    if twist == "thin_harvest" then loss = loss + 2 end
    if paid_policy == "provision" then loss = math.max(1, math.floor(loss / 2)) end
    write_byte(CONFIG.addresses.player_food, (read_byte(CONFIG.addresses.player_food) or 0) - loss)
    add_log("Famine bites through stores -" .. tostring(loss))
  elseif shock == "levy" and has_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count) then
    local boost = 2 + CONFIG.difficulty
    if twist == "bandit_surge" then boost = boost + 2 end
    add_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count, boost, 0, 245, CONFIG.addresses.enemy_troops_stride)
    add_log("Emergency levies swell rival armies +" .. tostring(boost))
  elseif shock == "bad_omens" and CONFIG.addresses.player_popularity then
    local loss = paid_policy == "patronage" and 1 or 2
    write_byte(CONFIG.addresses.player_popularity, (read_byte(CONFIG.addresses.player_popularity) or 0) - loss)
    add_log("Bad omens unsettle the people")
  end
end

local function squeeze_player()
  local roll = rand(4)
  if twist == "merchant_war" then roll = 1 end
  if twist == "thin_harvest" then roll = 2 end
  if twist == "mandate_drift" then roll = 3 end
  if roll == 1 and CONFIG.addresses.player_gold then
    local tax = 2 + CONFIG.difficulty + math.floor(pressure / 2)
    write_byte(CONFIG.addresses.player_gold, (read_byte(CONFIG.addresses.player_gold) or 0) - tax)
    add_log("Corrupt stewards skim gold -" .. tostring(tax))
  elseif roll == 2 and CONFIG.addresses.player_food then
    local loss = 2 + CONFIG.difficulty + rand(3)
    write_byte(CONFIG.addresses.player_food, (read_byte(CONFIG.addresses.player_food) or 0) - loss)
    add_log("Granary rot spreads food -" .. tostring(loss))
  elseif roll == 3 and CONFIG.addresses.player_popularity then
    write_byte(CONFIG.addresses.player_popularity, (read_byte(CONFIG.addresses.player_popularity) or 0) - 1)
    add_log("Rumors erode public trust")
  elseif CONFIG.addresses.player_training then
    write_byte(CONFIG.addresses.player_training, (read_byte(CONFIG.addresses.player_training) or 0) - 1)
    add_log("Veterans desert quiet drills")
  end
end

local function comeback_guard()
  local troops = read_byte(CONFIG.addresses.player_troops)
  local food = read_byte(CONFIG.addresses.player_food)
  if troops and troops < CONFIG.recovery_troops_threshold then
    write_byte(CONFIG.addresses.player_troops, troops + 4)
    add_log("Desperate volunteers answer the call")
  end
  if food and food < CONFIG.recovery_food_threshold then
    write_byte(CONFIG.addresses.player_food, food + 6)
    add_log("Hidden stores are found")
  end
end

local function enable_self_test()
  CONFIG.addresses.player_owner = 0x017F
  CONFIG.addresses.enemy_owner_start = 0x0180
  CONFIG.addresses.enemy_owner_count = 6
  CONFIG.addresses.enemy_owner_stride = 1
  fake_memory[0x017F] = 1
  for i = 0, 5 do fake_memory[0x0180 + i] = i + 2 end
  CONFIG.addresses.month = 0x0100
  CONFIG.addresses.player_gold = 0x0101
  CONFIG.addresses.player_food = 0x0102
  CONFIG.addresses.player_popularity = 0x0103
  CONFIG.addresses.player_ruler_loyalty = 0x0104
  CONFIG.addresses.player_troops = 0x0105
  CONFIG.addresses.player_training = 0x0106
  CONFIG.addresses.enemy_gold_start = 0x0120
  CONFIG.addresses.enemy_gold_count = 6
  CONFIG.addresses.enemy_gold_stride = 4
  CONFIG.addresses.enemy_food_start = 0x0121
  CONFIG.addresses.enemy_food_count = 6
  CONFIG.addresses.enemy_food_stride = 4
  CONFIG.addresses.enemy_troops_start = 0x0122
  CONFIG.addresses.enemy_troops_count = 6
  CONFIG.addresses.enemy_troops_stride = 4
  CONFIG.addresses.enemy_loyalty_start = 0x0123
  CONFIG.addresses.enemy_loyalty_count = 6
  CONFIG.addresses.enemy_loyalty_stride = 4

  fake_memory[CONFIG.addresses.month] = 1
  fake_memory[CONFIG.addresses.player_gold] = 80
  fake_memory[CONFIG.addresses.player_food] = 72
  fake_memory[CONFIG.addresses.player_popularity] = 55
  fake_memory[CONFIG.addresses.player_ruler_loyalty] = 50
  fake_memory[CONFIG.addresses.player_troops] = 88
  fake_memory[CONFIG.addresses.player_training] = 45

  for i = 0, CONFIG.addresses.enemy_gold_count - 1 do
    fake_memory[CONFIG.addresses.enemy_gold_start + i * CONFIG.addresses.enemy_gold_stride] = 30 + i
    fake_memory[CONFIG.addresses.enemy_food_start + i * CONFIG.addresses.enemy_food_stride] = 28 + i
    fake_memory[CONFIG.addresses.enemy_troops_start + i * CONFIG.addresses.enemy_troops_stride] = 35 + i
    fake_memory[CONFIG.addresses.enemy_loyalty_start + i * CONFIG.addresses.enemy_loyalty_stride] = 40 + i
  end

  add_log("Self-test memory map enabled")
end

local policies = { "balanced", "provision", "patronage", "drill" }
local policy_text = {
  balanced = "Balanced: no cost",
  provision = "Stores: 6 gold -> up to 10 food",
  patronage = "Relief: 8 food -> up to 4 trust",
  drill = "Drill: 5 gold -> up to 4 training"
}

local function apply_policy()
  paid_policy = "balanced"
  local a = CONFIG.addresses
  local cost_addr, benefit_addr, cost, gain, ceiling, label
  if selected_policy == "provision" then
    cost_addr, benefit_addr, cost, gain, ceiling, label = a.player_gold, a.player_food, 6, 10, 220, "Stores"
  elseif selected_policy == "patronage" then
    cost_addr, benefit_addr, cost, gain, ceiling, label = a.player_food, a.player_popularity, 8, 4, 100, "Relief"
  elseif selected_policy == "drill" then
    cost_addr, benefit_addr, cost, gain, ceiling, label = a.player_gold, a.player_training, 5, 4, 100, "Drill"
  else return end
  if not cost_addr or not benefit_addr then return end
  local funds, value = read_byte(cost_addr), read_byte(benefit_addr)
  local actual = math.min(gain, math.max(0, ceiling - value))
  -- Pay once, only when the full cost is affordable and a benefit exists.
  if funds < cost or actual == 0 then return end
  write_byte(cost_addr, funds - cost)
  write_byte(benefit_addr, value + actual)
  paid_policy = selected_policy
  add_log(label .. ": paid " .. cost .. ", gained " .. actual)
end

local function goodwill_event()
  local a = CONFIG.addresses
  local trust = read_byte(a.player_popularity)
  if not trust or trust < 65 then return end
  local food = read_byte(a.player_food)
  if food and food < 180 then
    local gain = math.min(4, 180 - food)
    write_byte(a.player_food, food + gain)
    add_log("Trusted rule: villagers send food +" .. gain)
  end
end

local function crisis_kind()
  local kinds = {}
  if CONFIG.addresses.player_food then kinds[#kinds + 1] = "famine" end
  if CONFIG.addresses.player_popularity then kinds[#kinds + 1] = "bad_omens" end
  if has_range(CONFIG.addresses.enemy_troops_start, CONFIG.addresses.enemy_troops_count) then
    for i = 1, CONFIG.addresses.enemy_troops_count do
      if enemy_eligible(i) then kinds[#kinds + 1] = "levy"; break end
    end
  end
  if #kinds == 0 then return nil end
  local preferred = ({ thin_harvest = "famine", bandit_surge = "levy", mandate_drift = "bad_omens" })[twist]
  if preferred and in_list(preferred, kinds) then return preferred end
  return choose(kinds)
end

local crisis_text = {
  famine = "Famine next month: provision helps",
  bad_omens = "Unrest next month: patronage helps",
  levy = "Rival levy next month: prepare"
}

local function new_month()
  dry_run_shadow = {}
  campaign_month = campaign_month + 1
  local score = player_score()
  pressure = clamp(math.floor(score / 45) + CONFIG.difficulty - 1, 0, 9)
  track_habits()
  pressure = clamp(pressure + math.floor(habit_heat / 4), 0, 9)
  local food, troops = read_byte(CONFIG.addresses.player_food), read_byte(CONFIG.addresses.player_troops)
  recovering = campaign_month <= recovery_until or
    (food ~= nil and food < CONFIG.recovery_food_threshold) or
    (troops ~= nil and troops < CONFIG.recovery_troops_threshold)
  if not recovering then threat_clock = clamp(threat_clock + pressure + CONFIG.difficulty, 0, 99) end
  set_doctrine()
  set_twist()
  set_nemesis()

  local event_budget = CONFIG.max_events_per_month
  local events_used = 0
  local candidates = {}
  local function deliver(id, action, repeatable)
    if events_used >= event_budget then return false end
    if not repeatable and last_event_month[id] and campaign_month - last_event_month[id] <= CONFIG.event_repeat_gap then return false end
    local before = mutation_count
    event_start_mutations = before
    action()
    event_start_mutations = nil
    if mutation_count == before then return false end
    events_used = events_used + 1
    last_event_month[id] = campaign_month
    return true
  end
  local function offer(id, chance, action, forced)
    if forced or rand(100) <= chance then candidates[#candidates + 1] = { id = id, action = action } end
  end

  paid_policy = "balanced"
  -- Recovery has first claim on a small budget; policy and threats use remaining slots.
  if recovering then deliver("recovery", comeback_guard, true) end
  -- A one-slot budget must not let a recurring policy starve a warned crisis.
  local reserve_crisis = not recovering and pending_crisis and campaign_month >= pending_crisis.due
  if not reserve_crisis or event_budget - events_used >= 2 then
    deliver("policy", apply_policy, true)
  end
  if recovering then
    if pending_crisis then add_log("Crisis postponed during recovery") end
  else
    if pending_crisis and campaign_month >= pending_crisis.due then
      local kind = pending_crisis.kind
      if deliver("crisis", function() seasonal_shock(kind) end, true) then
        pending_crisis = nil
        threat_clock = math.floor(threat_clock / 3)
        recovery_until = campaign_month + 1
      end
    end
    -- No additional hostile events in the month a warned crisis lands.
    if recovery_until < campaign_month then
      offer("economy", 35 + pressure * 4, mutate_enemy_economy, doctrine == "hoarder")
      offer("armies", 25 + pressure * 5, mutate_enemy_armies, doctrine == "raider")
      offer("squeeze", 15 + pressure * 5, squeeze_player)
      if doctrine == "conspirator" or twist == "court_fever" then offer("conspiracy", 40 + pressure * 4, loyalty_conspiracy) end
      if pressure >= 5 then
        offer("coalition", 18 + pressure * 3, coalition_pulse)
        offer("nemesis", 20 + pressure * 4, nemesis_pressure)
      end
      if CONFIG.habit_breakers and math.max(hoard_streak, army_streak, soft_streak) >= CONFIG.habit_threshold_months then
        offer("habit", 35 + habit_heat * 6, habit_breaker_event)
      end
      if pressure >= 4 then offer("supply", 100, overextension_tax, true) end
    end
  end
  offer("goodwill", 35, goodwill_event)
  for i = #candidates, 2, -1 do
    local j = rand(i)
    candidates[i], candidates[j] = candidates[j], candidates[i]
  end
  for _, row in ipairs(candidates) do deliver(row.id, row.action) end
  if not recovering and recovery_until < campaign_month and not pending_crisis and event_budget > 0 and
      threat_clock >= 24 + (5 - CONFIG.difficulty) * 3 then
    local kind = crisis_kind()
    if kind then
      pending_crisis = { kind = kind, due = campaign_month + 1 }
      add_log(crisis_text[kind])
    end
  end
  last_events_used, last_budget = events_used, event_budget
  if events_used == 0 then add_log("A quiet month; the council waits") end
  safe_log(string.format("[BKR month] events=%d budget=%d pressure=%d threat=%d", events_used, event_budget, pressure, threat_clock))
  dry_run_shadow = {}
end

local function poll_controls()
  if not emu.isKeyPressed then return end
  local function pressed(key)
    local ok, down = pcall(emu.isKeyPressed, key)
    down = ok and down == true
    local edge = down and not previous_keys[key]
    previous_keys[key] = down
    return edge
  end
  if pressed(CONFIG.policy_key) then
    for i, policy in ipairs(policies) do
      if policy == selected_policy then selected_policy = policies[(i % #policies) + 1]; break end
    end
    add_log("Next council: " .. policy_text[selected_policy])
  end
  if pressed(CONFIG.chronicle_key) then show_chronicle = not show_chronicle end
  if pressed(CONFIG.overlay_key) then CONFIG.show_overlay = not CONFIG.show_overlay end
end

local function wrap_text(text, width)
  local lines, line = {}, ""
  for word in text:gmatch("%S+") do
    if #line + #word + 1 > width and #line > 0 then lines[#lines + 1] = line; line = "" end
    line = line == "" and word or (line .. " " .. word)
  end
  if #line > 0 then lines[#lines + 1] = line end
  return lines
end

local function draw_overlay()
  if not CONFIG.show_overlay then return end
  local mode = CONFIG.self_test and "DEMO" or (CONFIG.dry_run and "DRY RUN" or "LIVE")
  local status = not CONFIG.addresses.month and "MAP REQUIRED" or (recovering and "RECOVERY" or (pending_crisis and "CRISIS WARNED" or "COUNCIL"))
  safe_draw_rectangle(0, 0, 256, 29, 0x40000000, true)
  safe_draw_string(4, 2, "BKR 0.3 " .. mode .. " | " .. status, 0xFFFFFF, 0x000000)
  safe_draw_string(4, 11, CONFIG.policy_key .. ":" .. selected_policy .. " " .. CONFIG.chronicle_key .. ":history " .. CONFIG.overlay_key .. ":hide", 0xCCFFCC, 0x000000)
  safe_draw_string(4, 20, pending_crisis and crisis_text[pending_crisis.kind] or policy_text[selected_policy], 0xFFFF66, 0x000000)
  if show_chronicle then
    local lines = {}
    for _, row in ipairs(chronicle) do
      for _, line in ipairs(wrap_text(string.format("M%03d %s", row.month, row.text), 39)) do lines[#lines + 1] = line end
    end
    safe_draw_rectangle(0, 31, 256, 102, 0x20000000, true)
    safe_draw_string(4, 33, "CHRONICLE / " .. mode .. " / newest entries", 0xFFFFFF, 0x000000)
    local first = math.max(1, #lines - 9)
    for i = first, #lines do safe_draw_string(4, 44 + (i - first) * 8, lines[i], 0xFFFFCC, 0x000000) end
  end
end

local function dump_dry_run_writes()
  if not CONFIG.dry_run then return end
  safe_log("[BKR dry-run] attempted writes: " .. tostring(dry_run_write_count))
  for i, row in ipairs(dry_run_writes) do
    safe_log(string.format("[BKR dry-run] #%d %s 0x%04X %02X>%02X frame=%d", i, describe_address(row.addr), row.addr, row.old, row.value, row.frame))
  end
end

local function tick()
  if not CONFIG.enabled then return end
  frame = frame + 1

  if CONFIG.self_test and frame % CONFIG.self_test_month_frames == 0 then
    local month = read_byte(CONFIG.addresses.month) or 0
    write_byte(CONFIG.addresses.month, (month % 12) + 1)
  end

  poll_controls()
  local month = read_byte(CONFIG.addresses.month)
  if month and month >= CONFIG.month_min and month <= CONFIG.month_max then
    if candidate_month ~= month then candidate_month, candidate_frames = month, 1
    else candidate_frames = candidate_frames + 1 end
    if candidate_frames >= CONFIG.month_stable_frames then
      if last_month == nil then last_month = month
      elseif month ~= last_month and frame - last_month_event_frame >= CONFIG.month_cooldown_frames then
        last_month_event_frame = frame
        last_month = month
        new_month()
      end
    end
  else candidate_month, candidate_frames = nil, 0 end
  -- Mesen drawings default to a one-frame duration: redraw each frame.
  draw_overlay()
end

local function validate_settings()
  local function integer(value, lo, hi, label)
    if type(value) ~= "number" or value ~= math.floor(value) or value < lo or value > hi then
      error("[BKR config] " .. label .. " must be an integer from " .. lo .. " to " .. hi)
    end
  end
  for _, key in ipairs({ "enabled", "dry_run", "show_overlay", "self_test", "campaign_twists", "nemesis_rivals", "habit_breakers", "validate_on_load", "require_enemy_ownership" }) do
    if type(CONFIG[key]) ~= "boolean" then error("[BKR config] " .. key .. " must be boolean") end
  end
  integer(CONFIG.chronicle_limit, 10, 10000, "chronicle_limit")
  integer(CONFIG.event_repeat_gap, 0, 12, "event_repeat_gap")
  integer(CONFIG.month_min, 0, 1, "month_min")
  integer(CONFIG.month_max, CONFIG.month_min + 11, CONFIG.month_min + 11, "month_max")
  integer(CONFIG.month_stable_frames, 1, 120, "month_stable_frames")
  integer(CONFIG.recovery_food_threshold, 1, 100, "recovery_food_threshold")
  integer(CONFIG.recovery_troops_threshold, 1, 100, "recovery_troops_threshold")
  if not in_list(CONFIG.policy, policies) then error("Unknown policy") end
  local keys = {}
  for _, field in ipairs({ "policy_key", "chronicle_key", "overlay_key" }) do
    local key = CONFIG[field]
    if type(key) ~= "string" or #key == 0 or keys[key] then error("Controls must use distinct nonempty key names") end
    keys[key] = true
  end
  if type(CONFIG.neutral_owner_values) ~= "table" then error("neutral_owner_values must be a table") end
  for _, value in ipairs(CONFIG.neutral_owner_values) do integer(value, 0, 255, "neutral owner") end
  integer(CONFIG.seed, 1, 2147483646, "seed")
  integer(CONFIG.difficulty, 1, 4, "difficulty")
  integer(CONFIG.max_events_per_month, 0, 20, "max_events_per_month")
  integer(CONFIG.month_cooldown_frames, 0, 3600, "month_cooldown_frames")
  integer(CONFIG.self_test_month_frames, 1, 3600, "self_test_month_frames")
  integer(CONFIG.dry_run_audit_limit, 1, 10000, "dry_run_audit_limit")
  integer(CONFIG.twist_duration_months, 1, 120, "twist_duration_months")
  integer(CONFIG.nemesis_duration_months, 1, 120, "nemesis_duration_months")
  integer(CONFIG.nemesis_bonus, 0, 20, "nemesis_bonus")
  integer(CONFIG.habit_threshold_months, 1, 12, "habit_threshold_months")
  if not in_list(CONFIG.doctrine_mode, { "adaptive", "hoarder", "raider", "conspirator", "storm" }) then error("Unknown doctrine_mode") end
  if not in_list(CONFIG.twist_mode, { "adaptive", "thin_harvest", "bandit_surge", "merchant_war", "court_fever", "mandate_drift" }) then error("Unknown twist_mode") end
  if not cpu or not cpu_write then error("Mesen NES memory API is unavailable") end
  if CONFIG.self_test then return end
  local occupied = {}
  local function address(addr, label)
    integer(addr, 0, 0x7FFF, label)
    if addr > 0x07FF and addr < 0x6000 then error("Address is outside NES RAM: " .. label) end
    if occupied[addr] then error("Overlapping address fields: " .. occupied[addr] .. " and " .. label) end
    occupied[addr] = label
  end
  for _, key in ipairs({ "month", "player_owner", "player_gold", "player_food", "player_troops", "player_training", "player_popularity", "player_ruler_health", "player_ruler_loyalty" }) do
    if CONFIG.addresses[key] ~= nil then address(CONFIG.addresses[key], key) end
  end
  for _, key in ipairs({ "enemy_gold", "enemy_food", "enemy_troops", "enemy_loyalty", "enemy_owner" }) do
    local start = CONFIG.addresses[key .. "_start"]
    local count = CONFIG.addresses[key .. "_count"]
    local stride = CONFIG.addresses[key .. "_stride"]
    integer(count, 0, 256, key .. "_count")
    integer(stride, 1, 32768, key .. "_stride")
    if (start == nil and count > 0) or (start ~= nil and count == 0) then error("Incomplete table: " .. key) end
    if start then
      for i = 0, math.max(1, count) - 1 do address(start + i * stride, key .. "[" .. (i + 1) .. "]") end
    end
  end
end

validate_settings()
if CONFIG.self_test then
  enable_self_test()
end

if CONFIG.validate_on_load then
  validate_config()
end

local function reset_session()
  frame, campaign_month = 0, 0
  chronicle, last_event_month, previous_keys = {}, {}, {}
  candidate_month, candidate_frames = nil, 0
  pending_crisis, recovery_until, recovering = nil, 0, false
  selected_policy, paid_policy = CONFIG.policy, "balanced"
  dry_run_write_count, dry_run_writes, mutation_count = 0, {}, 0
  event_start_mutations = nil
  doctrine, last_events_used, last_budget = "adaptive", 0, 0
  if CONFIG.self_test then fake_memory = {}; enable_self_test() end
  last_month = nil
  last_month_event_frame = -9999
  pressure, threat_clock, habit_heat = 0, 0, 0
  hoard_streak, army_streak, soft_streak = 0, 0, 0
  nemesis_index, nemesis_months_left = nil, 0
  twist, twist_months_left = "none", 0
  rng_state = CONFIG.seed
  dry_run_shadow = {}
  event_log, chronicle = {}, {}
  add_log("New journal after load/reset")
end

local function dump_chronicle()
  dump_dry_run_writes()
  safe_log("[BKR chronicle] Current session; not saved with emulator save states")
  for _, row in ipairs(chronicle) do
    safe_log(string.format("[BKR chronicle %s M%03d] %s", row.mode, row.month, row.text))
  end
end

emu.addEventCallback(tick, emu.eventType.startFrame)
emu.addEventCallback(dump_chronicle, emu.eventType.scriptEnded)
if emu.eventType.stateLoaded then emu.addEventCallback(reset_session, emu.eventType.stateLoaded) end
if emu.eventType.reset then emu.addEventCallback(reset_session, emu.eventType.reset) end
safe_log("Bandit Kings Reborn 0.3 director loaded. Configured systems: " .. tostring(configured_system_count()))
