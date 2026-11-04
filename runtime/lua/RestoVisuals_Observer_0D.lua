-- Original loader entry. A workspace-only preparer supplies this run identifier.
local runID = '__RESTOVISUALS_RUN_ID__'
if runID == '__RESTOVISUALS_' .. 'RUN_ID__' then return end
local guard = 'RestoVisuals_Observer_0D_lifetime'
if rawget(_G, guard) ~= nil then return end
rawset(_G, guard, {run_id = runID, attempted = true})

-- Contain Lua load/sink errors so they do not propagate into Pure's loader.
-- pcall is not recovery from a fatal native/C++ error.
local ok = pcall(function()
  local folder = ac.getFolder(ac.FolderID.ExtRoot)
    .. '/config-ext/PureLdrEffects/RestoVisuals_Observer_0D/'
  local Observer = dofile(folder .. 'restovisuals_observer.lua')
  local Probe = dofile(folder .. 'restovisuals_host_probe.lua')
  local host = {ac = ac, pure = pure, execution_scope = 'csp_runtime_unverified',
    schedule = setTimeout, cancel = clearTimeout, on_release = ac.onRelease,
    write = function(data) return io.save(folder .. 'runtime-receipt.json', JSON.stringify(data)) end}
  local experiment = Probe.run(host, Observer,
    {csp_version = '0.3.0-preview361', pure_mode = 'gamma', max_samples = 8}, runID)
  rawget(_G, guard).experiment = experiment
end)
if not ok and ac and type(ac.log) == 'function' then
  pcall(ac.log, 'RestoVisuals observer probe failed; no rendering operation was requested')
end
