-- Bandit Kings Reborn: Address Lab for Mesen
-- Use this after the broad memory scout. It ranks RAM addresses by a specific
-- before/after value so you can confirm stat addresses with less noise.

local CONFIG = {
  label = "player_gold",
  before_value = 50,
  after_value = 45,
  watch_start = 0x0000,
  watch_end = 0x07FF,
  frames_to_ignore_after_load = 90,
  max_rows = 10
}

assert(CONFIG.before_value >= 0 and CONFIG.before_value <= 255 and CONFIG.before_value == math.floor(CONFIG.before_value), "before_value must be one byte")
assert(CONFIG.after_value >= 0 and CONFIG.after_value <= 255 and CONFIG.after_value == math.floor(CONFIG.after_value), "after_value must be one byte")
assert(CONFIG.frames_to_ignore_after_load >= 1, "Baseline delay must be at least one frame")
assert(CONFIG.watch_start <= CONFIG.watch_end, "Invalid watch range")

local cpu = emu.memType.nesDebug or emu.memType.cpuDebug or emu.memType.nesMemory or emu.memType.cpu
local frame = 0
local baseline = {}
local best = {}

local function safe_log(text)
  if emu.log then emu.log(text) end
end

local function safe_draw_rectangle(x, y, width, height, color, fill)
  if emu.drawRectangle then pcall(emu.drawRectangle, x, y, width, height, color, fill) end
end

local function safe_draw_string(x, y, text, color, background)
  if emu.drawString then pcall(emu.drawString, x, y, text:sub(1, 40), color, background) end
end

local function hex(n)
  return string.format("0x%04X", n)
end

local function byte(value)
  return value % 256
end

local function read_byte(addr)
  return byte(emu.read(addr, cpu))
end

local function score(addr, old_value, new_value)
  local expected_delta = CONFIG.after_value - CONFIG.before_value
  local actual_delta = new_value - old_value
  local value_score = 0
  local delta_score = 0

  if old_value == CONFIG.before_value then value_score = value_score + 4 end
  if new_value == CONFIG.after_value then value_score = value_score + 6 end
  if actual_delta == expected_delta then delta_score = delta_score + 8 end
  if math.abs(actual_delta - expected_delta) <= 1 then delta_score = delta_score + 2 end

  return value_score + delta_score
end

local function take_baseline()
  for addr = CONFIG.watch_start, CONFIG.watch_end do
    baseline[addr] = read_byte(addr)
  end
end

local function scan()
  best = {}
  for addr = CONFIG.watch_start, CONFIG.watch_end do
    local old_value = baseline[addr]
    local new_value = read_byte(addr)
    if old_value ~= new_value then
      local candidate_score = score(addr, old_value, new_value)
      if candidate_score > 0 then
        best[#best + 1] = {
          addr = addr,
          old_value = old_value,
          new_value = new_value,
          candidate_score = candidate_score
        }
      end
    end
  end

  table.sort(best, function(a, b)
    if a.candidate_score ~= b.candidate_score then
      return a.candidate_score > b.candidate_score
    end
    return a.addr < b.addr
  end)
end

local function draw()
  safe_draw_rectangle(0, 0, 256, 30 + math.min(CONFIG.max_rows, #best) * 8, 0x7F000000, true)
  safe_draw_string(4, 4, "Bandit Kings Address Lab: " .. CONFIG.label, 0xFFFFFF, 0x000000)
  safe_draw_string(4, 14, tostring(CONFIG.before_value) .. " -> " .. tostring(CONFIG.after_value), 0xFFFF66, 0x000000)

  if frame < CONFIG.frames_to_ignore_after_load then
    safe_draw_string(4, 26, "Wait, then perform the one test action", 0x99FF99, 0x000000)
    return
  end

  for i = 1, math.min(CONFIG.max_rows, #best) do
    local row = best[i]
    local text = string.format(
      "%s = %02X>%02X score %02d",
      hex(row.addr),
      row.old_value,
      row.new_value,
      row.candidate_score
    )
    safe_draw_string(4, 18 + i * 8, text, 0x99FF99, 0x000000)
  end
end

local function dump()
  safe_log("Bandit Kings Address Lab candidates for " .. CONFIG.label .. ":")
  for i = 1, math.min(20, #best) do
    local row = best[i]
    safe_log(string.format(
      "%s = %02X>%02X score %02d    CONFIG.addresses.%s = %s",
      hex(row.addr),
      row.old_value,
      row.new_value,
      row.candidate_score,
      CONFIG.label,
      hex(row.addr)
    ))
  end
end

local function tick()
  frame = frame + 1
  if frame == CONFIG.frames_to_ignore_after_load then
    take_baseline()
    safe_log("Address Lab baseline captured for " .. CONFIG.label)
  elseif frame > CONFIG.frames_to_ignore_after_load then
    scan()
  end
  if frame % 10 == 0 then draw() end
end

emu.addEventCallback(tick, emu.eventType.startFrame)
emu.addEventCallback(dump, emu.eventType.scriptEnded)
safe_log("Address Lab loaded. Edit CONFIG values, start the script, wait for baseline, perform one matching action, then stop.")
