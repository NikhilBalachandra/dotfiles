-- Set <space> as the leader key
-- See `:help mapleader`
-- NOTE: Make sure to set `mapleader` before lazy so your mappings are correct
vim.g.mapleader = ' '
vim.g.maplocalleader = '\\'

vim.opt.number = true -- Show line numbers
vim.opt.wrap = false  -- Disable line wrap
-- always display sign column with fixed space for up to the 3 columns
vim.opt.signcolumn = "yes:1"
vim.opt.termguicolors = true

local keymaps = {
  FindFiles = {"n", "<leader>ff", {desc = "Find files", group = "File"}},
  FindFilesVC = {"n", "<leader>fv", {desc = "Find version controlled files", group = "File"}},
  FindBuffers = {"n", "<leader>fb" },

  SearchText = {"n", "<leader>st", {desc = "Find text", group = "Search"}},
  SearchTextVC = {"n", "<leader>sv", {desc = "Find version controlled text"}},
  SearchTextVCHist = {"n", "<leader>sh", {desc = "Find version controlled text in history"}},

  LookupDeclaration = {"n", "gD", {desc = "Lookup declaration", group = "Lookup"}},
  LookupDefinition = {"n", "gd", {desc = "Lookup definition"}},
  LookupImplementation = {"n", "gi", {desc = "Lookup implementation"}},
  LookupTypeDefinition = {"n", "gt", {desc = "Lookup type definition"}},
  LookupReferences = {"n", "gr", {desc = "Lookup references"}},

  InfoHover = {"n", "K"},
  InfoSignature = {"n", "<C-k>"},

  Rename = {"n", "<space>cr"},
  CodeAction = {"n", "<space>ca"},
  Format = {"n", "<space>cf"},

  ShowDiagnosticsLine = {"n", "<space>e"},
  ShowDiagnosticsBuffer = {"n", "<space>q"},
  ShowDiagnosticsAll = {"n", "<space>Q"},
  -- vim.keymap.set('n', '[d', vim.diagnostic.goto_prev)
  -- vim.keymap.set('n', ']d', vim.diagnostic.goto_next)
}

require('cfg.lazy').setup({
  {"folke/todo-comments.nvim", opts = {}},

  -- the colorscheme should be available when starting Neovim
  {
    "folke/tokyonight.nvim",
    lazy = false, -- make sure we load this during startup if it is your main colorscheme
    priority = 1000, -- make sure to load this before all the other start plugins
    config = function()
      -- load the colorscheme here
      vim.cmd([[colorscheme tokyonight]])
    end,
  },

  {
    'nvim-telescope/telescope.nvim',
    tag = '0.1.8',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      local builtin = require('telescope.builtin')
      local cfg_keymaps = require('cfg.keymaps')
      cfg_keymaps.set(keymaps.FindFiles, builtin.find_files, {})
      cfg_keymaps.set(keymaps.FindBuffers, builtin.buffers, {})
      cfg_keymaps.set(keymaps.SearchText, builtin.live_grep, {})
    end,
  },

  {
    'neovim/nvim-lspconfig',
    tag = 'v0.1.8',
    config = function()
      require'lspconfig'.terraformls.setup{}
      vim.api.nvim_create_autocmd({"BufWritePre"}, {
        pattern = {"*.tf", "*.tfvars"},
        callback = function()
          vim.lsp.buf.format()
        end,
      })
    end,
  },

  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {
      -- your configuration comes here
      -- or leave it empty to use the default settings
      -- refer to the configuration section below
    },
    keys = {
      {
        "<leader>?",
        function()
          require("which-key").show({ global = false })
        end,
        desc = "Buffer Local Keymaps (which-key)",
      },
    },
    config = function()
      local wk = require("which-key")
      local cfg_keymaps = require('cfg.keymaps')
      local groups = cfg_keymaps.groups(keymaps)
      for k, v in pairs(groups) do
        wk.add({
          { k, group = v }
        })
      end
    end
  },
})
