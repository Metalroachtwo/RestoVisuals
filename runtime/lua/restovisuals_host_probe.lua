-- Original, finite observation experiment. Import has no native side effects.
local M = {}

function M.run(host, Observer, config, runID)
  assert(type(host) == 'table' and type(Observer) == 'table', 'invalid_probe_host')
  assert(type(runID) == 'string' and #runID >= 8 and #runID <= 64, 'invalid_run_id')
  for _, name in ipairs({'schedule', 'cancel', 'on_release', 'write'}) do
    assert(type(host[name]) == 'function', 'missing_probe_lifecycle_api')
  end
  local nativeCalls, stoppedAt, cleanupOK = 0, nil, true
  local deadline, grace, releaseCancel, observer
  local event, finished, initialWrite = 'preparing', false, false
  local object = {}
  local function receipt()
    return {schema_version = 1, run_id = runID, event = event,
      execution_scope = host.execution_scope or 'unverified_host',
      native_callback_invocations = nativeCalls,
      callbacks_after_stop = stoppedAt and (nativeCalls - stoppedAt) or 0,
      stop_witness_available = stoppedAt ~= nil,
      owned_lifecycle_calls_succeeded = cleanupOK,
      named_pure_effect_registered = false, shader_executed = false,
      game_visuals_validated = false, buffer_encoding = 'unknown',
      observer = observer and observer:receipt() or nil}
  end
  local function persist(nextEvent)
    event = nextEvent
    local ok, written = pcall(host.write, receipt())
    return ok and written == true
  end
  local function cancelTimer(id)
    if id == nil then return end
    local ok, removed = pcall(host.cancel, id)
    if not ok or removed ~= true then cleanupOK = false end
  end
  local function cancelRelease()
    if type(releaseCancel) == 'function' then
      local cancel = releaseCancel
      releaseCancel = nil
      if not pcall(cancel) then cleanupOK = false end
    end
  end
  local function finish(reason)
    if finished then return end
    finished = true
    if observer and not observer:stop() then cleanupOK = false end
    stoppedAt = stoppedAt or nativeCalls
    cancelTimer(deadline); deadline = nil
    cancelTimer(grace); grace = nil
    cancelRelease()
    if stoppedAt ~= nativeCalls then cleanupOK = false end
    persist(reason)
  end
  local function schedule(callback, seconds)
    local ok, id = pcall(host.schedule, callback, seconds)
    if not ok or type(id) ~= 'number' or id ~= id or id < 0 or id % 1 ~= 0 then
      cleanupOK = false
      return nil
    end
    return id
  end
  function object:receipt() return receipt() end
  function object:stop() finish('explicit_stop'); return cleanupOK end

  local proxy = setmetatable({}, {__index = host.ac})
  proxy.onPostProcessing = function(callback)
    return host.ac.onPostProcessing(function(...)
      nativeCalls = nativeCalls + 1
      return callback(...)
    end)
  end
  observer = Observer.new({ac = proxy, pure = host.pure, execution_scope = host.execution_scope}, config)
  initialWrite = persist('prepared_not_registered')
  if not initialWrite then finish('receipt_sink_failed_no_start'); return object end

  local ok, handle = pcall(host.on_release, function()
    releaseCancel = nil -- The host is already dispatching this release callback.
    finish('host_released')
  end)
  if not ok or type(handle) ~= 'function' then
    cleanupOK = false
    finish('release_registration_unknown_no_observer_start')
    return object
  end
  releaseCancel = handle
  deadline = schedule(function()
    deadline = nil
    if finished then return end
    if not observer:stop() then cleanupOK = false end
    stoppedAt = nativeCalls
    if not persist('observer_stopped_waiting_for_witness') then cleanupOK = false end
    grace = schedule(function()
      grace = nil
      finish(nativeCalls == stoppedAt and 'stop_witness_completed' or 'callback_after_unsubscribe')
    end, 1)
    if grace == nil then finish('witness_timer_failed') end
  end, 10)
  if deadline == nil then finish('deadline_registration_unknown_no_observer_start'); return object end
  if not observer:start() then finish('observer_start_blocked'); return object end
  if not persist('observer_started') then finish('receipt_sink_failed_after_start') end

  return object
end

return M
