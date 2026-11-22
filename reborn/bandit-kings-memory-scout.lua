-- Bandit Kings Reborn: Memory Scout for Mesen
-- Load this first to discover which RAM bytes change when money, food,
-- officers, provinces, month, loyalty, troops, and ruler data change.

local cpu = emu.memType.nesDebug or emu.memType.cpuDebug or emu.memType.nesMemory or emu.memType.cpu
local start_addr = 0x0000
local end_addr = 0x07FF
local frame = 0
local last = {}
local changes = {}
local frozen = false

local function safe_log(text)
  if emu.log then emu.log(text) end
end

local function safe_draw_rectangle(x, y, width, height, color, fill)
  if emu.drawRectangle then pcall(emu.drawRectangle, x, y, width, height, color, fill) end
end

local function safe_draw_string(x, y, text, color, background)
  if emu.drawString then pcall(emu.drawString, x, y, text:sub(1, 40), color, background) end
end

local function hex(n, width)
  return string.format("$%0" .. tostring(width or 4) .. "X", n)
end

local function byte(value)
  return value % 256
end

local function read_byte(addr)
  return byte(emu.read(addr, cpu))
end

local function snapshot()
  for addr = start_addr, end_addr do
    last[addr] = read_byte(addr)
  end
end

local function note(addr, old_value, new_value)
  local entry = changes[addr]
  if not entry then
    entry = { count = 0, first = frame, last = frame, old = old_value, value = new_value }
    changes[addr] = entry
  end
  entry.count = entry.count + 1
  entry.last = frame
  entry.old = old_value
  entry.value = new_value
end

local function scan()
  if frozen then return end

  for addr = start_addr, end_addr do
    local value = read_byte(addr)
    local old = last[addr]
    if old ~= nil and value ~= old then
      note(addr, old, value)
    end
    last[addr] = value
  end
end

local function top_changes(limit)
  local rows = {}
  for addr, entry in pairs(changes) do
    rows[#rows + 1] = { addr = addr, entry = entry }
  end
  table.sort(rows, function(a, b)
    if a.entry.last ~= b.entry.last then
      return a.entry.last > b.entry.last
    end
    return a.entry.count > b.entry.count
  end)

  local out = {}
  for i = 1, math.min(limit, #rows) do
    local row = rows[i]
    out[#out + 1] = string.format(
      "%s %02X>%02X x%d",
      hex(row.addr),
      row.entry.old,
      row.entry.value,
      row.entry.count
    )
  end
  return out
end

local function draw()
  safe_draw_rectangle(0, 0, 256, 49, 0x7F000000, true)
  safe_draw_string(4, 4, "Bandit Kings Memory Scout", 0xFFFFFF, 0x000000)
  safe_draw_string(4, 14, frozen and "PAUSED - reload to resume" or "Change one stat/menu value at a time", 0xFFFF66, 0x000000)

  local rows = top_changes(4)
  for i, text in ipairs(rows) do
    safe_draw_string(4, 16 + i * 8, text, 0x99FF99, 0x000000)
  end
end

local function tick()
  frame = frame + 1
  scan()
  if frame % 10 == 0 then draw() end
end

local function dump()
  safe_log("Bandit Kings Memory Scout candidates:")
  for _, row in ipairs(top_changes(40)) do
    safe_log(row)
  end
end

snapshot()
emu.addEventCallback(tick, emu.eventType.startFrame)
emu.addEventCallback(dump, emu.eventType.scriptEnded)
safe_log("Memory Scout running. Make one in-game change, watch the overlay, then stop the script to dump candidates.")
