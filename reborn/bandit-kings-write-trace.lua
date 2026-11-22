-- Bandit Kings Reborn: Write Trace for Mesen
-- Use this when polling is too noisy. It records CPU RAM writes while you
-- perform one specific action, then ranks the most relevant addresses.

local CONFIG = {
  label = "advance_month",
  watch_start = 0x0000,
  watch_end = 0x07FF,
  ignore_first_frames = 60,
  max_rows = 10
}

local frame = 0
local writes = {}
local recent = {}

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

local function note_write(addr, value)
  if frame < CONFIG.ignore_first_frames then return end

  local entry = writes[addr]
  if not entry then
    entry = { count = 0, first = frame, last = frame, value = byte(value) }
    writes[addr] = entry
  end
  entry.count = entry.count + 1
  entry.last = frame
  entry.value = byte(value)

  recent[#recent + 1] = { addr = addr, value = byte(value), frame = frame }
  while #recent > 8 do
    table.remove(recent, 1)
  end
end

local function ranked_writes()
  local rows = {}
  for addr, entry in pairs(writes) do
    rows[#rows + 1] = { addr = addr, entry = entry }
  end

  table.sort(rows, function(a, b)
    if a.entry.last ~= b.entry.last then
      return a.entry.last > b.entry.last
    end
    if a.entry.count ~= b.entry.count then
      return a.entry.count > b.entry.count
    end
    return a.addr < b.addr
  end)

  return rows
end

local cached_rows = {}

local function draw()
  safe_draw_rectangle(0, 0, 256, 26 + CONFIG.max_rows * 8, 0x7F000000, true)
  safe_draw_string(4, 4, "Bandit Kings Write Trace: " .. CONFIG.label, 0xFFFFFF, 0x000000)
  if frame < CONFIG.ignore_first_frames then
    safe_draw_string(4, 14, "Waiting for startup writes to settle", 0xFFFF66, 0x000000)
    return
  end
  safe_draw_string(4, 14, "Perform exactly one action, then stop", 0xFFFF66, 0x000000)

  local rows = cached_rows
  for i = 1, math.min(CONFIG.max_rows, #rows) do
    local row = rows[i]
    local text = string.format("%s <= %02X x%d", hex(row.addr), row.entry.value, row.entry.count)
    safe_draw_string(4, 16 + i * 8, text, 0x99FF99, 0x000000)
  end
end

local function dump()
  safe_log("Bandit Kings Write Trace candidates for " .. CONFIG.label .. ":")
  local rows = ranked_writes()
  for i = 1, math.min(30, #rows) do
    local row = rows[i]
    safe_log(string.format(
      "%s <= %02X x%d lastFrame=%d",
      hex(row.addr),
      row.entry.value,
      row.entry.count,
      row.entry.last
    ))
  end
end

local function tick()
  frame = frame + 1
  -- Mesen drawings last one frame: draw every frame, re-rank every 10th.
  if frame % 10 == 0 then cached_rows = ranked_writes() end
  draw()
end

local function write_callback(addr, value)
  note_write(addr, value)
end

if emu.memType.nesMemory then
  emu.addMemoryCallback(write_callback, emu.callbackType.write, CONFIG.watch_start, CONFIG.watch_end, emu.cpuType.nes)
else
  emu.addMemoryCallback(write_callback, emu.memCallbackType.cpuWrite, CONFIG.watch_start, CONFIG.watch_end)
end
emu.addEventCallback(tick, emu.eventType.startFrame)
emu.addEventCallback(dump, emu.eventType.scriptEnded)
safe_log("Write Trace running. Wait for the overlay prompt, perform one action, then stop the script.")
