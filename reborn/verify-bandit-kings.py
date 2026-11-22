"""Execute the kit under Lua 5.1 and 5.4 with a mocked Mesen API.

Requires Python and lupa: python -m pip install lupa
Run: python verify-bandit-kings.py
These tests do not validate the game's RAM layout or replace Mesen playtesting.
"""
from pathlib import Path
import unittest
from lupa.lua51 import LuaRuntime as Lua51
from lupa.lua54 import LuaRuntime as Lua54

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "bandit-kings-reborn-director.lua").read_text(encoding="utf-8")
MOCK = '''
memory, writes, logs, callbacks, keys, drawings = {}, {}, {}, {}, {}, {}
emu = {
  memType = {cpu=0, cpuDebug=256},
  memCallbackType = {cpuWrite=1},
  eventType = {startFrame=3, scriptEnded=10, stateLoaded=6, reset=0},
  log=function(s) logs[#logs+1]=s end,
  read=function(a, t) assert(t ~= nil); return memory[a] or 0 end,
  write=function(a, v, t) assert(t ~= nil); assert(v>=0 and v<=255); memory[a]=v; writes[#writes+1]={a,v} end,
  addEventCallback=function(f,t) assert(t~=nil); callbacks[t]=f end,
  addMemoryCallback=function(f,t,a,b,c) assert(t~=nil); memory_callback=f end,
  isKeyPressed=function(k) return keys[k] == true end,
  drawRectangle=function(...) end,
  drawString=function(x,y,text) drawings[#drawings+1]={x=x,y=y,text=text} end
}
'''
EXPOSE = '''
return {config=CONFIG, tick=tick, month=new_month, read=read_byte, write=write_byte,
 economy=mutate_enemy_economy, armies=mutate_enemy_armies, reset=reset_session,
 track=track_habits, breaker=habit_breaker_event, count=configured_system_count,
 validate=validate_settings, rand=rand, audit=dump_dry_run_writes,
 policy=apply_policy, goodwill=goodwill_event, eligible=enemy_eligible,
 shock=seasonal_shock,
 controls=poll_controls, draw=draw_overlay, session=function()
   return {month=campaign_month, policy=selected_policy, paid=paid_policy,
    crisis=pending_crisis, recovery=recovering, until_month=recovery_until,
    events=last_events_used, budget=last_budget, journal=chronicle,
    event_months=last_event_month, writes=dry_run_write_count}
 end}
'''


class DirectorTests(unittest.TestCase):
    runtime = Lua54

    def setUp(self):
        self.lua = self.runtime(unpack_returned_tuples=True)
        self.lua.execute(MOCK)
        self.api = self.lua.execute(SOURCE + EXPOSE)
        self.cfg = self.api.config
        self.mem = self.lua.globals().memory

    def map_player(self):
        for i, key in enumerate(("month", "player_gold", "player_food", "player_troops", "player_training", "player_popularity", "player_ruler_loyalty"), 256):
            self.cfg.addresses[key] = i
            self.mem[i] = 100
        self.mem[256] = 1

    def test_default_is_dry_and_unmapped(self):
        self.assertTrue(self.cfg.dry_run)
        self.assertFalse(self.cfg.nemesis_rivals)
        self.assertEqual(self.api.count(), 0)
        for _ in range(240): self.api.tick()
        self.assertEqual(len(self.lua.globals().writes), 0)

    def test_boost_never_reduces_high_resources(self):
        self.cfg.dry_run = False
        self.cfg.require_enemy_ownership = False
        self.cfg.addresses.enemy_gold_start = 512
        self.cfg.addresses.enemy_gold_count = 1
        self.mem[512] = 250
        self.api.economy()
        self.assertEqual(self.mem[512], 250)

    def test_dry_run_chains_without_touching_ram(self):
        self.mem[512] = 40
        self.api.write(512, 45)
        self.api.write(512, self.api.read(512) + 2)
        self.assertEqual(self.api.read(512), 47)
        self.assertEqual(self.mem[512], 40)
        self.assertEqual(len(self.lua.globals().writes), 0)

    def test_dry_shadow_expires_each_month(self):
        self.mem[512] = 40
        self.api.write(512, 45)
        self.api.month()
        self.assertEqual(self.api.read(512), 40)

    def test_rng_matches_between_lua_versions(self):
        values = []
        for runtime in (Lua51, Lua54):
            lua = runtime(unpack_returned_tuples=True)
            lua.execute(MOCK)
            api = lua.execute(SOURCE + EXPOSE)
            values.append([api.rand(100) for _ in range(200)])
        self.assertEqual(values[0], values[1])

    def test_drawing_failure_does_not_stop_director(self):
        self.lua.execute('emu.drawString=function() error("draw unavailable") end; emu.drawRectangle=emu.drawString')
        for _ in range(40): self.api.tick()

    def test_threat_stays_due_without_delivery(self):
        for _ in range(40): self.api.month()
        rows = [x for x in self.lua.globals().logs.values() if x.startswith("[BKR month]")]
        self.assertIn("threat=99", rows[-1])

    def test_single_event_budget_is_respected(self):
        self.map_player()
        self.cfg.max_events_per_month = 1
        self.cfg.high_pressure_bonus_event = False
        self.cfg.campaign_twists = False
        self.cfg.habit_breakers = False
        for _ in range(100): self.api.month()
        rows = [x for x in self.lua.globals().logs.values() if x.startswith("[BKR month]")]
        self.assertTrue(all("events=0 budget=1" in x or "events=1 budget=1" in x for x in rows))

    def test_zero_budget_delivers_no_events(self):
        self.map_player()
        self.cfg.dry_run = False
        self.cfg.max_events_per_month = 0
        self.cfg.high_pressure_bonus_event = False
        self.cfg.campaign_twists = False
        self.cfg.habit_breakers = False
        self.api.month()
        self.assertEqual(len(self.lua.globals().writes), 0)

    def test_noops_do_not_consume_budget(self):
        self.map_player()
        self.cfg.dry_run = False
        self.cfg.max_events_per_month = 1
        self.cfg.high_pressure_bonus_event = False
        self.cfg.campaign_twists = False
        self.cfg.habit_breakers = False
        self.cfg.doctrine_mode = "hoarder"
        for _ in range(20): self.api.month()
        self.assertGreater(len(self.lua.globals().writes), 0)

    def test_cooldown_retains_month_change(self):
        self.cfg.addresses.month = 256
        self.mem[256] = 1
        for _ in range(3): self.api.tick()
        self.mem[256] = 2
        for _ in range(3): self.api.tick()
        self.mem[256] = 3
        for _ in range(100): self.api.tick()
        rows = [x for x in self.lua.globals().logs.values() if x.startswith("[BKR month]")]
        self.assertEqual(len(rows), 2)

    def test_reset_does_not_treat_loaded_month_as_event(self):
        self.cfg.addresses.month = 256
        self.mem[256] = 3
        for _ in range(3): self.api.tick()
        self.lua.globals().callbacks[6]()
        self.mem[256] = 1
        for _ in range(3): self.api.tick()
        rows = [x for x in self.lua.globals().logs.values() if x.startswith("[BKR month]")]
        self.assertEqual(len(rows), 0)

    def test_invalid_and_overlapping_addresses_rejected(self):
        self.cfg.addresses.player_gold = 0x2000
        with self.assertRaises(Exception): self.api.validate()
        self.cfg.addresses.player_gold = 256
        self.cfg.addresses.month = 256
        with self.assertRaises(Exception): self.api.validate()

    def test_invalid_strides_and_names_rejected(self):
        self.cfg.addresses.enemy_gold_stride = 0
        with self.assertRaises(Exception): self.api.validate()
        self.cfg.addresses.enemy_gold_stride = 1
        self.cfg.twist_mode = "typo"
        with self.assertRaises(Exception): self.api.validate()

    def test_all_scripts_load_on_both_api_shapes(self):
        for modern in (False, True):
            for path in ROOT.glob("*.lua"):
                lua = self.runtime(unpack_returned_tuples=True)
                lua.execute(MOCK)
                if modern:
                    lua.execute('emu.memType={nesMemory=1,nesDebug=2}; emu.memCallbackType=nil; emu.callbackType={write=1}; emu.cpuType={nes=1}')
                lua.execute(path.read_text(encoding="utf-8"))
                for _ in range(150):
                    if lua.globals().callbacks[3]: lua.globals().callbacks[3]()
                if lua.globals().callbacks[10]: lua.globals().callbacks[10]()

    def test_long_self_test_and_no_real_writes(self):
        lua = self.runtime(unpack_returned_tuples=True)
        lua.execute(MOCK)
        api = lua.execute(SOURCE.replace("self_test = false,", "self_test = true,") + EXPOSE)
        for _ in range(24000): api.tick()
        self.assertEqual(api.count(), 10)
        self.assertEqual(len(lua.globals().writes), 0)

    def select(self, policy):
        for _ in range(4):
            if self.api.session().policy == policy: return
            self.lua.globals()['keys']['P'] = True
            self.api.controls()
            self.lua.globals()['keys']['P'] = False
            self.api.controls()
        self.fail('Policy not found')

    def map_rivals(self):
        self.cfg.addresses.player_owner = 400
        self.mem[400] = 1
        self.cfg.addresses.enemy_owner_start = 410
        self.cfg.addresses.enemy_owner_count = 4
        self.cfg.addresses.enemy_owner_stride = 1
        self.cfg.addresses.enemy_gold_start = 512
        self.cfg.addresses.enemy_gold_count = 4
        for i, owner in enumerate((1, 0, 255, 2)):
            self.mem[410 + i] = owner
            self.mem[512 + i] = 40

    def test_ownership_blocks_player_neutral_and_captured_rows(self):
        self.map_rivals()
        self.cfg.dry_run = False
        self.api.economy()
        self.assertEqual([self.mem[512+i] for i in range(3)], [40,40,40])
        self.assertGreater(self.mem[515], 40)
        before = self.mem[515]
        self.mem[413] = 1
        self.api.economy()
        self.assertEqual(self.mem[515], before)

    def test_missing_ownership_map_blocks_rival_mutations(self):
        self.cfg.dry_run = False
        self.cfg.addresses.enemy_gold_start = 512
        self.cfg.addresses.enemy_gold_count = 1
        self.mem[512] = 40
        self.api.economy()
        self.assertEqual(self.mem[512], 40)

    def test_policy_transaction_cost_and_capped_actual_benefit(self):
        self.map_player()
        self.cfg.dry_run = False
        self.select('provision')
        self.mem[258] = 216
        self.api.policy()
        self.assertEqual((self.mem[257], self.mem[258]), (94,220))
        self.assertIn('gained 4', self.api.session().journal[len(self.api.session().journal)].text)

    def test_policy_never_charges_if_unaffordable_capped_or_unmapped(self):
        self.map_player()
        self.cfg.dry_run = False
        self.select('provision')
        self.mem[257] = 5
        self.api.policy()
        self.assertEqual(len(self.lua.globals().writes), 0)
        self.mem[257], self.mem[258] = 100, 250
        self.api.policy()
        self.assertEqual(len(self.lua.globals().writes), 0)
        self.cfg.addresses.player_food = None
        self.api.policy()
        self.assertEqual(len(self.lua.globals().writes), 0)

    def test_other_policies_and_goodwill_have_exact_costs(self):
        self.map_player()
        self.cfg.dry_run = False
        self.mem[261], self.mem[260] = 60, 40
        self.select('patronage')
        self.api.policy()
        self.assertEqual((self.mem[258], self.mem[261]), (92,64))
        self.select('drill')
        self.api.policy()
        self.assertEqual((self.mem[257], self.mem[260]), (95,44))
        self.api.goodwill()
        self.assertEqual(self.mem[258], 92)
        self.mem[261] = 65
        self.api.goodwill()
        self.assertEqual(self.mem[258], 96)

    def test_keyboard_uses_edges_and_survives_missing_api(self):
        self.lua.globals()['keys']['P'] = True
        for _ in range(30): self.api.controls()
        self.assertEqual(self.api.session().policy, 'provision')
        self.lua.execute('emu.isKeyPressed=nil')
        self.api.controls()

    def test_month_glitches_and_invalid_values_do_not_trigger_events(self):
        self.cfg.addresses.month = 256
        self.mem[256] = 1
        for _ in range(3): self.api.tick()
        self.mem[256] = 2
        self.api.tick()
        self.mem[256] = 1
        for _ in range(4): self.api.tick()
        self.mem[256] = 255
        for _ in range(100): self.api.tick()
        self.assertEqual(self.api.session().month, 0)
        self.mem[256] = 2
        for _ in range(3): self.api.tick()
        self.assertEqual(self.api.session().month, 1)

    def test_zero_based_calendar_wrap(self):
        self.cfg.month_min, self.cfg.month_max = 0,11
        self.cfg.addresses.month = 256
        self.mem[256] = 11
        for _ in range(3): self.api.tick()
        self.mem[256] = 0
        for _ in range(3): self.api.tick()
        self.assertEqual(self.api.session().month, 1)

    def test_crisis_is_warned_in_prior_month_and_then_resolves(self):
        self.map_player()
        for _ in range(30):
            self.api.month()
            if self.api.session().crisis: break
        state = self.api.session()
        self.assertIsNotNone(state.crisis)
        self.assertEqual(state.crisis.due, state.month + 1)
        self.assertEqual(state.until_month, 0)
        self.api.month()
        self.assertIsNone(self.api.session().crisis)
        self.assertEqual(self.api.session().until_month, self.api.session().month + 1)
        self.api.month()
        self.assertTrue(self.api.session().recovery)

    def test_one_slot_budget_does_not_starve_crisis_for_policy(self):
        self.map_player()
        self.cfg.max_events_per_month = 1
        self.select('provision')
        for _ in range(30):
            self.api.month()
            if self.api.session().crisis: break
        self.assertIsNotNone(self.api.session().crisis)
        self.api.month()
        self.assertIsNone(self.api.session().crisis)
        self.assertEqual(self.api.session().events, 1)

    def test_recovery_prevents_rival_boosts_and_further_losses(self):
        self.map_player()
        self.map_rivals()
        self.cfg.dry_run = False
        self.mem[258], self.mem[259] = 2,3
        self.api.month()
        self.assertTrue(self.api.session().recovery)
        self.assertGreater(self.mem[258], 2)
        self.assertGreater(self.mem[259], 3)
        self.assertEqual(self.mem[515], 40)

    def test_hard_cap_includes_twists_habits_and_policy(self):
        self.map_player()
        self.cfg.max_events_per_month = 1
        self.cfg.twist_mode = 'bandit_surge'
        self.select('provision')
        for _ in range(40):
            self.api.month()
            self.assertLessEqual(self.api.session().events, 1)
        self.cfg.max_events_per_month = 0
        self.cfg.dry_run = False
        self.api.month()
        self.assertEqual(len(self.lua.globals().writes), 0)

    def test_repeated_hostile_events_have_an_intervening_month(self):
        self.map_player()
        self.cfg.max_events_per_month = 20
        prior = {}
        for _ in range(80):
            self.api.month()
            for name, month in self.api.session().event_months.items():
                if name in ('crisis','policy','recovery'): continue
                if name in prior and month != prior[name]: self.assertGreater(month - prior[name], 1)
                prior[name] = month

    def test_journal_is_bounded_labeled_and_reset_clears_audit(self):
        self.map_player()
        self.cfg.chronicle_limit = 12
        for _ in range(50): self.api.month()
        self.assertEqual(len(self.api.session().journal), 12)
        self.assertTrue(all(row.mode == 'DRY' for row in self.api.session().journal.values()))
        self.assertGreater(self.api.session().writes, 0)
        self.api.reset()
        self.assertEqual(self.api.session().writes, 0)
        self.assertEqual(self.api.session().month, 0)
        self.assertIsNone(self.api.session().crisis)
        self.assertEqual(len(self.api.session().journal), 1)

    def test_overlay_draws_every_frame_with_honest_mode(self):
        for _ in range(5): self.api.tick()
        self.assertEqual(len(self.lua.globals().drawings), 15)
        self.assertIn('DRY RUN', self.lua.globals().drawings[1].text)
        self.assertIn('MAP REQUIRED', self.lua.globals().drawings[1].text)

    def test_incomplete_tables_and_ambiguous_settings_rejected(self):
        self.cfg.addresses.enemy_gold_count = 1
        with self.assertRaises(Exception): self.api.validate()
        self.cfg.addresses.enemy_gold_count = 0
        self.cfg.dry_run = 'false'
        with self.assertRaises(Exception): self.api.validate()
        self.cfg.dry_run = True
        self.cfg.chronicle_key = self.cfg.policy_key
        with self.assertRaises(Exception): self.api.validate()
        self.cfg.chronicle_key = 'H'
        self.cfg.policy_key = None
        with self.assertRaises(Exception): self.api.validate()

    def test_paid_preparation_mitigates_crisis(self):
        self.map_player()
        self.cfg.dry_run = False
        self.select('provision')
        self.api.policy()
        before = self.mem[258]
        self.api.shock('famine')
        protected_loss = before - self.mem[258]
        self.select('balanced')
        self.api.policy()
        before = self.mem[258]
        self.api.shock('famine')
        self.assertLess(protected_loss, before - self.mem[258])
        self.mem[261] = 60
        self.select('patronage')
        self.api.policy()
        before = self.mem[261]
        self.api.shock('bad_omens')
        self.assertEqual(before - self.mem[261], 1)

    def test_demo_is_generated_from_current_director(self):
        expected = SOURCE.replace('  self_test = false,','  self_test = true,',1).replace('  nemesis_rivals = false,','  nemesis_rivals = true,',1)
        self.assertEqual((ROOT/'bandit-kings-reborn-demo.lua').read_text(encoding='utf-8'), expected)


class DirectorLua51Tests(DirectorTests):
    runtime = Lua51


if __name__ == "__main__":
    unittest.main(verbosity=2)
