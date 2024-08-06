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
  FindFiles = {"n", "<leader>ff" },

  LookupDeclaration = { "n", "gD" },
  LookupDefinition = { "n", "gd" },
  LookupImplementation = { "n", "gi" },
  LookupTypeDefinition = { "n", "gt" },
  LookupReferences = { "n", "gr" },

  InfoHover = { "n", "K" },
  InfoSignature = { "n", "<C-k>" },

  Rename = { "n", "<space>cr" },
  CodeAction = { "n", "<space>ca" },
  Format = { "n", "<space>cf" },

  ShowDiagnosticsLine = { "n", "<space>e" },
  ShowDiagnosticsBuffer = { "n", "<space>q" },
  ShowDiagnosticsAll = { "n", "<space>Q" },
  -- vim.keymap.set('n', '[d', vim.diagnostic.goto_prev)
  -- vim.keymap.set('n', ']d', vim.diagnostic.goto_next)
}

require("cfg.lazy").setup({
  {"folke/todo-comments.nvim", opts = {}},
  {
    'nvim-telescope/telescope.nvim', tag = '0.1.8', dependencies = { 'nvim-lua/plenary.nvim' }
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
  }
})
