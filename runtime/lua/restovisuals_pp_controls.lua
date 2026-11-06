-- Original Pure UI adapter. Import is inert; no callback, exposure or effect registration.
local M = {}
local controls = {
  {'Intensity', 1, 0, 1}, {'Exposure EV', 0, -4, 4},
  {'Highlights', 1, 0, 1}, {'Shadows', 0, -.25, .5},
  {'Saturation', 1, 0, 1.5}, {'Contrast', 1, .8, 1.2}
}
local function finite(x) return type(x)=='number' and x==x and x~=math.huge and x~=-math.huge end
function M.new(pure, capability)
  if type(capability)~='table' or capability.csp~='0.3.0-preview361'
    or capability.build~=3898 or capability.pure~='3.50' or capability.mode~='gamma' then
    return nil, 'unverified runtime capability'
  end
  local ui = type(pure)=='table' and type(pure.script)=='table' and pure.script.ui
  if type(ui)~='table' then return nil, 'Pure UI unavailable' end
  for _,name in ipairs({'addSliderInteger','addSliderFloat','getValue'}) do
    if type(ui[name])~='function' then return nil, 'Pure UI unavailable' end
  end
  local self={initialized=false, attempted=false, rendering_connected=false}
  function self:init()
    if self.attempted then return false, 'initialization already attempted' end
    self.attempted=true
    local ok=pcall(function()
      ui.addSliderInteger('RestoVisuals preset', 1, 1, 3, '1 Balanced; 2 Warm; 3 Cool / High Contrast')
      for _,c in ipairs(controls) do ui.addSliderFloat('RestoVisuals '..c[1],c[2],c[3],c[4],'Offline prototype control; render adapter unverified') end
    end)
    if not ok then return false,'UI initialization incomplete; no automatic retry' end
    self.initialized=true
    return true
  end
  function self:read()
    if not self.initialized then return nil,'not initialized' end
    local ok,selection=pcall(ui.getValue,'RestoVisuals preset')
    if not ok then return nil,'control read unavailable' end
    if not finite(selection) or selection%1~=0 or selection<1 or selection>3 then return nil,'invalid preset' end
    local result={preset=({'balanced','warm','cool'})[selection],rendering_connected=false}
    for _,c in ipairs(controls) do
      local ok,v=pcall(ui.getValue,'RestoVisuals '..c[1])
      if not ok then return nil,'control read unavailable' end
      if not finite(v) or v<c[3] or v>c[4] then return nil,'invalid control' end
      result[c[1]]=v
    end
    return result
  end
  return self
end
return M
