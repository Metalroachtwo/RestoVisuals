-- Original read-only observer contract. Requiring this module installs nothing.
-- A future authorized host must inject ac and the exposed Pure SDK namespace.
local M = {}
local tracks = {['0.2.11'] = true, ['0.3.0-preview361'] = true}

local function finite(v)
  return type(v) == 'number' and v == v and v ~= math.huge and v ~= -math.huge
end

local function copy(value)
  if type(value) ~= 'table' then return value end
  local result = {}
  for key, child in pairs(value) do result[key] = copy(child) end
  return result
end

function M.new(host, config)
  assert(type(host) == 'table' and type(config) == 'table', 'invalid_adapter_arguments')
  local fields = {csp_version = true, pure_mode = true, max_samples = true}
  for key in pairs(config) do assert(fields[key], 'unknown_configuration_field') end
  assert(tracks[config.csp_version], 'unsupported_csp_track')
  assert(config.pure_mode == 'gamma' or config.pure_mode == 'lcs', 'invalid_pure_profile')
  local maxSamples = config.max_samples or 8
  assert(finite(maxSamples) and maxSamples % 1 == 0 and maxSamples >= 1 and maxSamples <= 64,
    'invalid_sample_bound')
  local requestedVersion, requestedMode = config.csp_version, config.pure_mode
  local active, unsubscribe, cleanupBlocked = false, nil, false
  local receipt = {
    schema_version = 1, adapter = 'restovisuals_read_only_observer',
    execution_scope = host.execution_scope or 'unverified_host',
    state = 'disabled', reason = 'not_started', gameplay_validated = false,
    requested_csp_version = requestedVersion, requested_pure_mode = requestedMode,
    csp_version = 'unknown', csp_build = 0, shader_space_mode = 'unknown',
    pure_fork_identity = 'unknown', stage = 'documented_yebis_callback',
    texture_format = 'unknown', texture_encoding = 'unknown',
    hdr_texture_accessed = false, depth_texture_accessed = false,
    shader_executed = false, settings_written = false, exposure_owned = false,
    callbacks = 0, main_callbacks = 0, auxiliary_callbacks = 0,
    resolution_changes = 0, samples = {}, cleanup = 'not_registered'
  }
  local object = {}

  local function fault(reason)
    active = false
    receipt.state, receipt.reason = 'blocked', reason
    return false
  end

  local function readMode()
    local pure = host.pure
    local fn = type(pure) == 'table' and type(pure.system) == 'table' and pure.system.isCSP_LCS
    if type(fn) ~= 'function' then return nil end
    local ok, linear = pcall(fn)
    if not ok or type(linear) ~= 'boolean' then return nil end
    return linear and 'lcs' or 'gamma'
  end

  local function callback(_params, exposure, mainPass, updateExposure, size)
    -- Never write params and never return true/a canvas to replace YEBIS.
    if not active then return nil end
    local ok = pcall(function()
      if readMode() ~= requestedMode then fault('pure_shader_mode_changed_or_unavailable'); return end
      assert(type(mainPass) == 'boolean' and type(updateExposure) == 'boolean', 'invalid_callback_flags')
      receipt.callbacks = receipt.callbacks + 1
      if not mainPass then receipt.auxiliary_callbacks = receipt.auxiliary_callbacks + 1; return end
      assert(size ~= nil and finite(size.x) and finite(size.y) and size.x % 1 == 0 and size.y % 1 == 0
        and size.x >= 1 and size.y >= 1 and size.x <= 16384 and size.y <= 16384, 'invalid_render_size')
      receipt.main_callbacks = receipt.main_callbacks + 1
      if receipt.width and (receipt.width ~= size.x or receipt.height ~= size.y) then
        receipt.resolution_changes = receipt.resolution_changes + 1
      end
      receipt.width, receipt.height = size.x, size.y
      if #receipt.samples >= maxSamples then return end
      local sample = {width = size.x, height = size.y, update_exposure = updateExposure}
      if finite(exposure) then sample.supplied_exposure = exposure end
      local timing = host.ac.getPerformanceCPUAndGPUTime
      if type(timing) == 'function' then
        local timingOK, cpu, gpu = pcall(timing)
        if timingOK and finite(cpu) and finite(gpu) then
          sample.raw_cpu_time, sample.raw_gpu_time = cpu, gpu
          sample.timing_units = 'unknown_do_not_compute_fps'
        end
      end
      receipt.samples[#receipt.samples + 1] = sample
    end)
    if not ok then fault('callback_input_or_api_failure') end
    return nil
  end

  function object:start()
    if cleanupBlocked then return fault('cleanup_unverified_requires_host_reload') end
    if active then return true end
    if unsubscribe ~= nil then return fault('owned_subscription_requires_shutdown') end
    local ac = host.ac
    if type(ac) ~= 'table' or type(ac.getPatchVersion) ~= 'function'
      or type(ac.getPatchVersionCode) ~= 'function' or type(ac.onPostProcessing) ~= 'function' then
      return fault('required_csp_api_missing')
    end
    local okVersion, version = pcall(ac.getPatchVersion)
    local okBuild, build = pcall(ac.getPatchVersionCode)
    if not okVersion or not okBuild or not tracks[version] or version ~= requestedVersion
      or not finite(build) or build % 1 ~= 0 or build <= 0 then
      return fault('runtime_version_mismatch_or_unknown')
    end
    if version == '0.3.0-preview361' and build ~= 3898 then return fault('preview_build_mismatch') end
    receipt.csp_version, receipt.csp_build = version, build
    local mode = readMode()
    receipt.shader_space_mode = mode or 'unknown'
    if mode == nil then return fault('pure_shader_mode_api_unavailable') end
    if mode ~= requestedMode then return fault('pure_shader_mode_profile_mismatch') end
    local ok, disposer = pcall(ac.onPostProcessing, callback)
    if not ok then return fault('callback_registration_failed') end
    if type(disposer) ~= 'function' then
      cleanupBlocked = true
      receipt.cleanup = 'registration_return_contract_unknown'
      return fault('invalid_unsubscribe_contract')
    end
    unsubscribe, active = disposer, true
    receipt.state, receipt.reason, receipt.cleanup = 'observing', 'observer_only', 'owned_subscription_registered'
    return true
  end

  function object:stop()
    active = false
    if cleanupBlocked then return false end
    local dispose = unsubscribe
    unsubscribe = nil
    if dispose then
      local ok = pcall(dispose)
      if not ok then
        cleanupBlocked = true
        receipt.cleanup = 'unsubscribe_failed_no_automatic_retry'
        receipt.state, receipt.reason = 'blocked', 'shutdown_failed_callback_inert'
        return false
      end
      receipt.cleanup = 'owned_subscription_removed'
    end
    receipt.state, receipt.reason = 'disabled', 'observer_stopped'
    return true
  end

  function object:receipt() return copy(receipt) end
  return object
end

return M
