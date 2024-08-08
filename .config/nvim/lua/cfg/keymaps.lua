local M = {}

function M.getopt(mode_lhs_opts, key)
  local opts = mode_lhs_opts[3]
  if opts ~= nil then
    return opts[key]
  end
  return nil
end

function M.set(mode_lhs_opts, rhs, opts)
  local key_opts = mode_lhs_opts[3]
  opts["desc"] = M.getopt(mode_lhs_opts, "desc")
  return vim.keymap.set(mode_lhs_opts[1], mode_lhs_opts[2], rhs, opts)
end

function M.groups(keymaps)
  local groups = {}
  local trie = require("trie").new()
  for k, v in pairs(keymaps) do
    local lhs = v[2]
    trie:insert(lhs)
  end
  local groups = trie:groupByCommonPrefix()
  for prefix, words in pairs(groups) do
    if #prefix > 0 and prefix ~= "<" then
      for k, v in pairs(keymaps) do
        if string.sub(v[2], 1, string.len(prefix)) == prefix then
          if v[3] ~= nil then
            if v[3]["group"] ~= nil then
              groups[prefix] = v[3]["group"]
              -- print("Key: ".. v[2] .. " Prefix: " .. prefix .. " group: " .. v[3]["group"])
            end
          end
        end
      end
    end
  end
  return groups
end

return M
